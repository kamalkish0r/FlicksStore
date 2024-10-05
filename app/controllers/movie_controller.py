from fastapi import APIRouter, Depends, File, UploadFile, BackgroundTasks
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from datetime import datetime
import tempfile
import csv
import os

from database import get_db
from services.movie_service import MovieService
from services.task_manager_service import TaskManagerService 
from repositories.movie_repository import MovieRepository

router = APIRouter()

# Initialize the Task Manager
task_manager = TaskManagerService()

@router.post("/upload-csv/")
async def upload_csv(background_tasks: BackgroundTasks, file: UploadFile = File(...), db: Session = Depends(get_db)):
    task_id = task_manager.create_task()  # Create a new task
    try:
        with tempfile.NamedTemporaryFile(delete=False, mode='wb') as temp_file:
            # Stream the file to a temporary location
            for chunk in iter(lambda: file.file.read(10000), b""):
                temp_file.write(chunk)
        
        # movie_service = MovieService(db, task_manager)
        # Trigger background task to process the file
        background_tasks.add_task(process_csv, temp_file.name, task_id, db)
        
        return JSONResponse(content={
            "message": "File uploaded successfully, processing started",
            "task_id": task_id
        }, status_code=202)
    except Exception as e:
        task_manager.update_status(task_id, "failed")
        return JSONResponse(content={"error": str(e)}, status_code=500)

@router.get("/upload-status/{task_id}")
async def get_upload_status(task_id: str):
    status_info = task_manager.get_status(task_id)  # Use the task manager to get status
    return {"task_id": task_id, "status_info": status_info}


def process_csv(file_path: str, task_id: str, db: Session):
    repository = MovieRepository(db)
    task_manager.update_status(task_id, "processing")
        
    try:
        count = 0
        with open(file_path, 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                # print(row)
                count += 1
                repository.create_movie(row)

            print(f'Processed {count} rows')
        task_manager.update_status(task_id, "completed", datetime.now().isoformat())
    except Exception as e:
        task_manager.update_status(task_id, "failed")
        print(f"Error processing CSV: {str(e)}")
    finally:
        # Clean up the temporary file
        os.unlink(file_path)
    