import csv
import os
from fastapi import UploadFile
from sqlalchemy.orm import Session
from datetime import datetime
import tempfile

from repositories.movie_repository import MovieRepository
from services.task_manager_service import TaskManagerService  

class MovieService:
    def __init__(self, db: Session, task_manager: TaskManagerService):
        self.db = db
        self.repository = MovieRepository(db)
        self.task_manager = task_manager  

    def save_file(self, file: UploadFile):
         try:
            with tempfile.NamedTemporaryFile(delete=False, mode='wb') as temp_file:
                # Stream the file to a temporary location
                for chunk in iter(lambda: file.file.read(10000), b""):
                    temp_file.write(chunk)
            return temp_file.name
         except Exception as e:
             raise Exception(f"Error saving file: {str(e)}")
        
    def process_file(self, file_path: str, task_id: str):
        self.task_manager.update_status(task_id, "processing")
        try:
            count = 0
            with open(file_path, 'r') as csv_file:
                csv_reader = csv.DictReader(csv_file)
                for row in csv_reader:
                    count += 1
                    self.repository.create_movie(row)
                    # if count > 10:
                    #     break

                print(f'Processed {count} rows')

            self.task_manager.update_status(task_id, "completed", datetime.now().isoformat())
        except Exception as e:
            self.task_manager.update_status(task_id, "failed")
            print(f"Error processing CSV: {str(e)}")
        finally:
            os.unlink(file_path)  # Clean up temp file
