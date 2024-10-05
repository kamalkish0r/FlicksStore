from fastapi import APIRouter, Depends, File, UploadFile, BackgroundTasks, Query
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import Optional, List

from database import get_db
from services.movie_service import MovieService
from schemas.movie_schema import MovieSchema
from services.task_manager_service import TaskManagerService, get_task_manager_service
from repositories.movie_repository import MovieRepository

router = APIRouter()

@router.post("/upload-csv/")
async def upload_csv(
    background_tasks: BackgroundTasks, 
    file: UploadFile = File(...), 
    db: Session = Depends(get_db),
    task_manager: TaskManagerService = Depends(get_task_manager_service)
):
    task_id = task_manager.create_task() 
    movie_service = MovieService(db, task_manager)
    try:
        file_path = movie_service.save_file(file)

        background_tasks.add_task(movie_service.process_file, file_path, task_id)
        return JSONResponse(content={
            "message": "File uploaded successfully, processing started",
            "task_id": task_id
        }, status_code=202)
    except Exception as e:
        task_manager.update_status(task_id, "failed")
        return JSONResponse(content={"error": str(e)}, status_code=500)
    

@router.get("/upload-status/{task_id}")
async def get_upload_status(
    task_id: str, 
    task_manager: TaskManagerService = Depends(get_task_manager_service)
):
    status_info = task_manager.get_status(task_id) 
    return {"task_id": task_id, "status_info": status_info}


@router.get("/movies", response_model=List[MovieSchema]) 
def get_movies(
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100),
    year: Optional[int] = Query(None),
    language: Optional[str] = Query(None),
    sort_by: Optional[str] = Query('release_date', regex="^(release_date|vote_average)$"),
    sort_order: Optional[str] = Query('asc', regex="^(asc|desc)$"),
):
    movie_repo = MovieRepository(db)
    movies = movie_repo.get_movies(
        page=page,
        per_page=per_page,
        year=year,
        language=language,
        sort_by=sort_by,
        sort_order=sort_order
    )
    return movies