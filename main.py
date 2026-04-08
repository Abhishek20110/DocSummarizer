from fastapi import FastAPI, Request, Form, BackgroundTasks, Query, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from datetime import timedelta
import os
import shutil
import logging
from dotenv import load_dotenv

from services.auth import get_drive_service
from services.drive_service import list_files_in_folder, download_file_to_memory, get_folder_name
from services.extractor import extract_content, extract_content_from_stream
from services.summarizer import summarize_text
from services.report_gen import generate_csv_report, generate_pdf_report
from services.database import (save_folder_results, get_folder_results, list_processed_folders, delete_folder, 
                                client as mongo_client, create_user, get_user_by_username)
from services.user_auth import (get_current_user, get_current_active_user, get_current_user_optional, create_access_token, verify_password, 
                                get_password_hash, ACCESS_TOKEN_EXPIRE_MINUTES)
from services.sample_data import SAMPLE_FOLDER, SAMPLE_RESULTS

load_dotenv()

logger = logging.getLogger("uvicorn.error")

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await mongo_client.server_info()
        logger.info("✅ MongoDB connected successfully.")
    except Exception as e:
        logger.error(f"❌ MongoDB connection failed: {e}")
    yield
    mongo_client.close()
    logger.info("🔌 MongoDB connection closed.")

app = FastAPI(title="DocSummarizer", lifespan=lifespan)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Status tracking explicitly separated by username
user_process_status = {}
user_process_results = {}

def get_user_status(username: str):
    if username not in user_process_status:
        user_process_status[username] = {
            "status": "idle",
            "message": "",
            "current_file": "",
            "total_files": 0,
            "processed_count": 0
        }
    return user_process_status[username]

def get_user_results(username: str):
    if username not in user_process_results:
        user_process_results[username] = []
    return user_process_results[username]

@app.exception_handler(status.HTTP_401_UNAUTHORIZED)
async def unauthorized_exception_handler(request: Request, exc: HTTPException):
    if request.url.path.startswith("/api") or request.url.path in ["/summarize", "/status"]:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"error": exc.detail},
        )
    return RedirectResponse(url="/login")

@app.exception_handler(status.HTTP_403_FORBIDDEN)
async def forbidden_exception_handler(request: Request, exc: HTTPException):
    if request.url.path.startswith("/api") or request.url.path in ["/summarize", "/status"]:
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={"error": exc.detail},
        )
    return RedirectResponse(url="/login")

# --- AUTH ROUTES ---

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse(request=request, name="login.html", context={"request": request})

@app.post("/login")
async def login_post(request: Request, username: str = Form(...), password: str = Form(...)):
    logger.info(f"Login attempt for user: {username}")
    user = await get_user_by_username(username)
    if not user or not verify_password(password, user["password_hash"]):
        logger.warning(f"Failed login attempt for user: {username}")
        return templates.TemplateResponse(request=request, name="login.html", context={"request": request, "error": "Invalid username or password"})

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": username}, expires_delta=access_token_expires
    )
    
    logger.info(f"User logged in successfully: {username}")
    response = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    response.set_cookie(key="access_token", value=f"Bearer {access_token}", httponly=True, max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60)
    return response

@app.get("/signup", response_class=HTMLResponse)
async def signup_page(request: Request):
    return templates.TemplateResponse(request=request, name="signup.html", context={"request": request})

@app.post("/signup")
async def signup_post(request: Request, username: str = Form(...), password: str = Form(...), confirm_password: str = Form(...)):
    logger.info(f"Signup attempt for username: {username}")
    if password != confirm_password:
        logger.warning(f"Signup failed: Passwords do not match for {username}")
        return templates.TemplateResponse(request=request, name="signup.html", context={"request": request, "error": "Passwords do not match"})
    
    existing_user = await get_user_by_username(username)
    if existing_user:
        logger.warning(f"Signup failed: Username {username} already taken")
        return templates.TemplateResponse(request=request, name="signup.html", context={"request": request, "error": "Username already taken"})
    
    hashed_password = get_password_hash(password)
    await create_user(username, hashed_password)
    logger.info(f"User registered successfully: {username}")
    
    return RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)

@app.get("/logout")
async def logout(request: Request):
    user_token = request.cookies.get("access_token")
    if user_token:
        logger.info("User logged out")
    response = RedirectResponse(url="/login", status_code=status.HTTP_302_FOUND)
    response.delete_cookie("access_token")
    return response

# --- APP ROUTES ---

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request, user: dict = Depends(get_current_user_optional)):
    if not user or not user.get("is_active", True):
        return templates.TemplateResponse(request=request, name="index.html", context={
            "request": request,
            "results": SAMPLE_RESULTS,
            "process_status": {"status": "idle", "message": "View Only Mode - Login as active user to summarize"},
            "processed_folders": [SAMPLE_FOLDER],
            "user": user or {"username": "Guest (View Only)"},
            "can_summarize": False
        })
        
    username = user["username"]
    folders = await list_processed_folders(username)
    ustatus = get_user_status(username)
    uresults = get_user_results(username)
    return templates.TemplateResponse(request=request, name="index.html", context={
        "request": request, 
        "results": uresults,
        "process_status": ustatus,
        "processed_folders": folders,
        "user": user,
        "can_summarize": True
    })

async def background_summarize(folder_id: str, username: str):
    logger.info(f"Background summarize started for folder_id: {folder_id} by user: {username}")
    ustatus = get_user_status(username)
    uresults = get_user_results(username)

    ustatus.update({
        "status": "processing",
        "processed_count": 0,
        "total_files": 0,
        "current_file": "",
        "message": ""
    })

    uresults.clear()

    try:
        service = get_drive_service()
        files = list_files_in_folder(service, folder_id)

        ustatus["total_files"] = len(files)

        if not files:
            logger.warning(f"No supported files found in folder: {folder_id}. Possibly a permissions issue.")
            ustatus.update({
                "status": "error",
                "message": "No files were found in this folder. This usually means the service account doesn't have access. Please make the folder public or share it with: drive-backend-service@intrepid-snow-436313-i4.iam.gserviceaccount.com"
            })
            return

        for file in files:
            file_id = file["id"]
            file_name = file["name"]
            mime_type = file["mimeType"]

            logger.info(f"Processing file: {file_name} from folder {folder_id}")
            ustatus["current_file"] = file_name

            try:
                # 🔹 Download to memory (auto-skips >10MB)
                file_stream = download_file_to_memory(service, file)

                if file_stream is None:
                    # Skipped due to size or error
                    uresults.append({
                        "filename": file_name,
                        "summary": "Skipped (file too large or download failed).",
                        "evaluation": None
                    })
                    ustatus["processed_count"] += 1
                    continue

                # 🔹 Extract content (in-memory)
                content = extract_content_from_stream(file_stream, mime_type)

                if not content.strip():
                    uresults.append({
                        "filename": file_name,
                        "summary": "No readable content found.",
                        "evaluation": None
                    })
                    ustatus["processed_count"] += 1
                    continue

                # 🔹 Summarize
                sh_result = await summarize_text(content)

                summary = sh_result.get("summary", "Error generating summary.")
                evaluation = sh_result.get("evaluation")

                uresults.append({
                    "filename": file_name,
                    "summary": summary,
                    "evaluation": evaluation
                })

            except Exception as file_error:
                logger.error(f"Processing failed for file {file_name}: {file_error}")
                uresults.append({
                    "filename": file_name,
                    "summary": f"Processing failed: {str(file_error)}",
                    "evaluation": None
                })

            ustatus["processed_count"] += 1

        ustatus.update({
            "status": "completed",
            "message": f"Successfully processed {ustatus['processed_count']} documents.",
            "current_file": ""
        })
        logger.info(f"Background processing complete. Successfully processed {ustatus['processed_count']} documents for folder {folder_id}.")

        # 🔹 Persist results
        folder_name = get_folder_name(service, folder_id)
        await save_folder_results(folder_id, folder_name, list(uresults), username)

    except Exception as e:
        logger.error(f"Error in background summarization for {folder_id}: {e}", exc_info=True)
        ustatus.update({
            "status": "error",
            "message": str(e)
        })

@app.post("/summarize")
async def process_folder(background_tasks: BackgroundTasks, folder_id: str = Form(...), user: dict = Depends(get_current_active_user)):
    username = user["username"]
    logger.info(f"Summarize requested for folder_id: {folder_id} by user: {username}")
    ustatus = get_user_status(username)
    if ustatus["status"] == "processing":
        return {"error": "A folder is already being processed."}
    
    background_tasks.add_task(background_summarize, folder_id, username)
    return {"message": "Processing started in the background.", "folder_id": folder_id}

@app.get("/status")
async def get_status(user: dict = Depends(get_current_user)):
    username = user["username"]
    ustatus = get_user_status(username)
    uresults = get_user_results(username)
    
    # Check MongoDB connection
    try:
        await mongo_client.server_info()
        mongo_status = "connected"
    except Exception as e:
        mongo_status = f"disconnected ({str(e)})"

    return {
        "process_status": ustatus,
        "results": uresults,
        "mongodb": {
            "status": mongo_status
        }
    }

@app.get("/api/folders")
async def get_folders(user: dict = Depends(get_current_user)):
    username = user["username"]
    return await list_processed_folders(username)

@app.get("/api/folders/{folder_id}")
async def get_folder(folder_id: str, user: dict = Depends(get_current_user_optional)):
    if folder_id == SAMPLE_FOLDER["folder_id"] and (not user or not user.get("is_active", True)):
        return {"folder_name": SAMPLE_FOLDER["folder_name"], "results": SAMPLE_RESULTS}
    if not user:
        return {"error": "Not authenticated"}

    username = user["username"]
    data = await get_folder_results(folder_id, username)
    if not data:
        return {"error": "Folder not found"}
    return data

@app.delete("/api/folders/{folder_id}")
async def remove_folder(folder_id: str, user: dict = Depends(get_current_user)):
    username = user["username"]
    await delete_folder(folder_id, username)
    return {"message": "Folder deleted"}

# --- PUBLIC SAMPLE EXPORT (no auth required) ---

@app.get("/sample/export/{format}")
async def export_sample_report(format: str):
    """Public endpoint to download sample/demo results as CSV or PDF. No login required."""
    output_dir = "exports"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    if format == "csv":
        file_path = os.path.join(output_dir, "summary_report_sample.csv")
        generate_csv_report(SAMPLE_RESULTS, file_path)
        return FileResponse(file_path, media_type='text/csv', filename="summary_report_sample.csv")

    elif format == "pdf":
        file_path = os.path.join(output_dir, "summary_report_sample.pdf")
        generate_pdf_report(SAMPLE_RESULTS, file_path)
        return FileResponse(file_path, media_type='application/pdf', filename="summary_report_sample.pdf")

    return JSONResponse(status_code=400, content={"error": "Invalid format. Use 'csv' or 'pdf'."})

@app.get("/export/{format}")
async def export_report(format: str, folder_id: str = Query(default=None), user: dict = Depends(get_current_user_optional)):
    results = []

    # Allow export for the sample folder without auth
    if folder_id == SAMPLE_FOLDER["folder_id"]:
        results = SAMPLE_RESULTS
        username = "sample"
    elif user:
        username = user["username"]
        results = get_user_results(username)

        # If in-memory is empty, try folder_id from DB
        if not results and folder_id:
            data = await get_folder_results(folder_id, username)
            if data:
                results = data.get("results", [])
    else:
        return JSONResponse(status_code=401, content={"error": "Login required to export your folder results."})

    if not results:
        return {"error": "No results to export. Please open or process a folder first."}
    
    output_dir = "exports"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        
    if format == "csv":
        file_path = os.path.join(output_dir, f"summary_report_{username}.csv")
        generate_csv_report(results, file_path)
        return FileResponse(file_path, media_type='text/csv', filename=f"summary_report_{username}.csv")
    
    elif format == "pdf":
        file_path = os.path.join(output_dir, f"summary_report_{username}.pdf")
        generate_pdf_report(results, file_path)
        return FileResponse(file_path, media_type='application/pdf', filename=f"summary_report_{username}.pdf")
    
    return {"error": "Invalid format. Use 'csv' or 'pdf'."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
