from fastapi import FastAPI, HTTPException, File, UploadFile
import os
from pydantic import BaseModel
# import aiohttp
from typing import List
from fastapi.responses import JSONResponse, FileResponse
from urllib.parse import unquote
from extraction import extract
from utils import get_files_from_directory
from query import run_query_and_theme_synthesis
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

class Query(BaseModel):
    query: str
    
FILE_DIRECTORY = "uploads"
os.makedirs(FILE_DIRECTORY, exist_ok=True)


@app.get("/file/{filename}")
async def get_file(filename: str) -> FileResponse:
    """
    Endpoint to retrieve and display a specific file.

    Args:
        filename (str): The name of the file to retrieve.

    Returns:
        FileResponse: The file to be displayed.
    """
    safe_filename = unquote(filename)
    file_path = os.path.join(FILE_DIRECTORY, safe_filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(file_path)


@app.get("/files")
async def list_files() -> JSONResponse:
    """
    Endpoint to get all files in the specified directory.

    Returns:
        JSONResponse: A JSON response containing the list of files.
    """
    files = get_files_from_directory(FILE_DIRECTORY)
    return JSONResponse(content={"files": files})

# Importing data from ALPHA_VANTAGE_API to our MYSQL database
@app.post('/upload/')
async def upload_file(files: List[UploadFile] = File(...)) -> JSONResponse:
    """
    Endpoint to upload multiple files to the server.

    Args:
        files (List[UploadFile]): The files to upload.

    Returns:
        JSONResponse: A JSON response indicating the status of the upload.
    """
    uploaded_files = []
    for file in files:
        try:
            file_path = os.path.join(FILE_DIRECTORY, file.filename)
            with open(file_path, "wb") as f:
                f.write(await file.read())
            uploaded_files.append({"filename": file.filename, "status": "success", "file_path": file_path})
            print(uploaded_files)
            await extract(uploaded_files)
        except Exception as e:
            uploaded_files.append({"filename": file.filename, "status": "error", "error": str(e)})

    return JSONResponse(content={"message": "Files uploaded", "files": uploaded_files})

# API to send user query to the agent
@app.post('/send/')
async def send(user_query: Query):
    try:
        response = run_query_and_theme_synthesis(user_query.query)
        return {
            'answer': response
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent failed to generate response: {str(e)}")


# For testing purpose
@app.get("/")
def health():
    return {"status": "ok"}