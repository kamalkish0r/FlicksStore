import csv
from fastapi import UploadFile
from sqlalchemy.orm import Session
from datetime import datetime
from io import StringIO

from repositories.movie_repository import MovieRepository
from services.task_manager_service import TaskManagerService  # Import the task manager

class MovieService:
    def __init__(self, db: Session, task_manager: TaskManagerService):
        self.db = db
        self.repository = MovieRepository(db)
        self.task_manager = task_manager  # Use the task manager service

    async def process_csv(self, file: UploadFile, task_id: str):
        self.task_manager.update_status(task_id, "processing")

        try:
            contents = await file.read()
            contents_str = contents.decode('utf-8')  # Decode bytes to string
            
            csv_reader = csv.DictReader(StringIO(contents_str))
            for row in csv_reader:
                self.repository.create_movie(row)

            self.task_manager.update_status(task_id, "completed", datetime.now().isoformat())
        except Exception as e:
            self.task_manager.update_status(task_id, "failed")
            print(f"Error processing CSV: {str(e)}")
