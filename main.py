from fastapi import FastAPI, Request, Form, BackgroundTasks
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import os
import shutil
from dotenv import load_dotenv

from services.auth import get_drive_service
from services.drive_service import list_files_in_folder, download_file, get_folder_name
from services.extractor import extract_content
from services.summarizer import summarize_text
from services.report_gen import generate_csv_report, generate_pdf_report
from services.database import save_folder_results, get_folder_results, list_processed_folders, delete_folder

load_dotenv()

app = FastAPI(title="DocSummarizer")
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
    process_status["status"] = "processing"
    process_status["processed_count"] = 0
    process_results = []
    
    try:
        service = get_drive_service()
        files = list_files_in_folder(service, folder_id)
        process_status["total_files"] = len(files)
        
        if not files:
            process_status["status"] = "completed"
            process_status["message"] = "No files found in the folder."
            return

        for file in files:
            file_id = file['id']
            file_name = file['name']
            process_status["current_file"] = file_name
            
            # Download
            temp_path = download_file(service, file_id, file_name)
            
            # Extract
            content = extract_content(temp_path)
            
            # Summarize
            summary = await summarize_text(content)
            
            process_results.append({
                "filename": file_name,
                "summary": summary
            })
            
            # Clean up temp file
            if os.path.exists(temp_path):
                os.remove(temp_path)
            
            process_status["processed_count"] += 1
            
        process_status["status"] = "completed"
        process_status["message"] = f"Successfully summarized {len(files)} documents."
        process_status["current_file"] = ""
        
        # Persist results
        folder_name = get_folder_name(service, folder_id)
        await save_folder_results(folder_id, folder_name, process_results)
        
    except Exception as e:
        process_status["status"] = "error"
        process_status["message"] = str(e)

@app.post("/summarize")
async def process_folder(background_tasks: BackgroundTasks, folder_id: str = Form(...)):
    if process_status["status"] == "processing":
        return {"error": "A folder is already being processed."}
    
    background_tasks.add_task(background_summarize, folder_id)
    return {"message": "Processing started in the background.", "folder_id": folder_id}

@app.get("/status")
async def get_status():
    return {
        "process_status": process_status,
        "results": process_results
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
async def export_report(format: str):
    if not process_results:
        return {"error": "No results to export."}
    
    output_dir = "exports"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    if format == "csv":
        file_path = os.path.join(output_dir, "summary_report.csv")
        generate_csv_report(process_results, file_path)
        return FileResponse(file_path, media_type='text/csv', filename="summary_report.csv")
    
    elif format == "pdf":
        file_path = os.path.join(output_dir, "summary_report.pdf")
        generate_pdf_report(process_results, file_path)
        return FileResponse(file_path, media_type='application/pdf', filename="summary_report.pdf")
    
    return {"error": "Invalid format."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
