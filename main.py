from fastapi import FastAPI, Request, Form, BackgroundTasks, Query
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
import os
import shutil
import logging
from dotenv import load_dotenv

#if using oauth, import from authwithOAuth  instead of auth
#from services.authwithOAuth import get_drive_service 
from services.auth import get_drive_service # Updated to use the new auth module
from services.drive_service import list_files_in_folder, download_file_to_memory, get_folder_name
from services.extractor import extract_content , extract_content_from_stream
from services.summarizer import summarize_text
from services.report_gen import generate_csv_report, generate_pdf_report
from services.database import save_folder_results, get_folder_results, list_processed_folders, delete_folder, client as mongo_client

load_dotenv()

logger = logging.getLogger("uvicorn.error")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: verify MongoDB connection
    try:
        await mongo_client.server_info()
        logger.info("✅ MongoDB connected successfully.")
    except Exception as e:
        logger.error(f"❌ MongoDB connection failed: {e}")
    yield
    # Shutdown: close MongoDB connection gracefully
    mongo_client.close()
    logger.info("🔌 MongoDB connection closed.")

app = FastAPI(title="DocSummarizer", lifespan=lifespan)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Status tracking
process_status = {
    "status": "idle", # idle, processing, completed, error
    "message": "",
    "current_file": "",
    "total_files": 0,
    "processed_count": 0
}
process_results = []

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    folders = await list_processed_folders()
    return templates.TemplateResponse("index.html", {
        "request": request, 
        "results": process_results,
        "process_status": process_status,
        "processed_folders": folders
    })

async def background_summarize(folder_id: str):
    global process_results, process_status

    process_status.update({
        "status": "processing",
        "processed_count": 0,
        "total_files": 0,
        "current_file": "",
        "message": ""
    })

    process_results = []

    try:
        service = get_drive_service()
        files = list_files_in_folder(service, folder_id)

        process_status["total_files"] = len(files)

        if not files:
            process_status.update({
                "status": "completed",
                "message": "No supported files found in the folder."
            })
            return

        for file in files:
            file_id = file["id"]
            file_name = file["name"]
            mime_type = file["mimeType"]

            process_status["current_file"] = file_name

            try:
                # 🔹 Download to memory (auto-skips >10MB)
                file_stream = download_file_to_memory(service, file)

                if file_stream is None:
                    # Skipped due to size or error
                    process_results.append({
                        "filename": file_name,
                        "summary": "Skipped (file too large or download failed).",
                        "evaluation": None
                    })
                    process_status["processed_count"] += 1
                    continue

                # 🔹 Extract content (in-memory)
                content = extract_content_from_stream(file_stream, mime_type)

                if not content.strip():
                    process_results.append({
                        "filename": file_name,
                        "summary": "No readable content found.",
                        "evaluation": None
                    })
                    process_status["processed_count"] += 1
                    continue

                # 🔹 Summarize
                sh_result = await summarize_text(content)

                summary = sh_result.get("summary", "Error generating summary.")
                evaluation = sh_result.get("evaluation")

                process_results.append({
                    "filename": file_name,
                    "summary": summary,
                    "evaluation": evaluation
                })

            except Exception as file_error:
                process_results.append({
                    "filename": file_name,
                    "summary": f"Processing failed: {str(file_error)}",
                    "evaluation": None
                })

            process_status["processed_count"] += 1

        process_status.update({
            "status": "completed",
            "message": f"Successfully processed {process_status['processed_count']} documents.",
            "current_file": ""
        })

        # 🔹 Persist results
        folder_name = get_folder_name(service, folder_id)
        await save_folder_results(folder_id, folder_name, process_results)

    except Exception as e:
        process_status.update({
            "status": "error",
            "message": str(e)
        })
@app.post("/summarize")
async def process_folder(background_tasks: BackgroundTasks, folder_id: str = Form(...)):
    if process_status["status"] == "processing":
        return {"error": "A folder is already being processed."}
    
    background_tasks.add_task(background_summarize, folder_id)
    return {"message": "Processing started in the background.", "folder_id": folder_id}

@app.get("/status")
async def get_status():
    # Check MongoDB connection
    try:
        await mongo_client.server_info()
        mongo_status = "connected"
    except Exception as e:
        mongo_status = f"disconnected ({str(e)})"

    return {
        "process_status": process_status,
        "results": process_results,
        "mongodb": {
            "status": mongo_status
        }
    }

@app.get("/api/folders")
async def get_folders():
    return await list_processed_folders()

@app.get("/api/folders/{folder_id}")
async def get_folder(folder_id: str):
    data = await get_folder_results(folder_id)
    if not data:
        return {"error": "Folder not found"}
    return data

@app.delete("/api/folders/{folder_id}")
async def remove_folder(folder_id: str):
    await delete_folder(folder_id)
    return {"message": "Folder deleted"}

@app.get("/export/{format}")
async def export_report(format: str, folder_id: str = Query(default=None)):
    # Determine which results to export
    results = process_results

    # If in-memory is empty, try folder_id from DB
    if not results and folder_id:
        data = await get_folder_results(folder_id)
        if data:
            results = data.get("results", [])

    if not results:
        return {"error": "No results to export. Please open or process a folder first."}
    
    output_dir = "exports"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    if format == "csv":
        file_path = os.path.join(output_dir, "summary_report.csv")
        generate_csv_report(results, file_path)
        return FileResponse(file_path, media_type='text/csv', filename="summary_report.csv")
    
    elif format == "pdf":
        file_path = os.path.join(output_dir, "summary_report.pdf")
        generate_pdf_report(results, file_path)
        return FileResponse(file_path, media_type='application/pdf', filename="summary_report.pdf")
    
    return {"error": "Invalid format. Use 'csv' or 'pdf'."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
