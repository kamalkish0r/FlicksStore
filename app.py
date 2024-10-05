from fastapi import FastAPI, File, UploadFile, BackgroundTasks
from fastapi.responses import JSONResponse
import csv
import tempfile
import os
from typing import Dict, Literal
from datetime import datetime

app = FastAPI()

# Define the possible status types
StatusType = Literal["uploading", "processing", "completed", "failed", "not found"]

# In-memory storage for task status (TODO : replace with a database in production)
task_status: Dict[str, Dict[str, str]] = {}

@app.post("/upload-csv/")
async def upload_csv(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    task_id = f"task_{len(task_status) + 1}"  
    start_time = datetime.now().isoformat()  
    task_status[task_id] = {
        "status": "uploading",
        "start_time": start_time,
        "completed_time": None  
    }

    try:
        with tempfile.NamedTemporaryFile(delete=False, mode='wb') as temp_file:
            # Stream the file to a temporary location
            for chunk in iter(lambda: file.file.read(10000), b""):
                temp_file.write(chunk)
        
        # Trigger background task to process the file
        background_tasks.add_task(process_csv, temp_file.name, task_id)
        
        return JSONResponse(content={
            "message": "File uploaded successfully, processing started",
            "task_id": task_id
        }, status_code=202)
    except Exception as e:
        task_status[task_id]["status"] = "failed"
        return JSONResponse(content={"error": str(e)}, status_code=500)

def process_csv(file_path: str, task_id: str):
    task_status[task_id]["status"] = "processing"
    try:
        with open(file_path, 'r') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                # TODO : Process each row and insert into database
                print(f'Processing {task_id} : {row}')
        
        task_status[task_id]["status"] = "completed"
        task_status[task_id]["completed_time"] = datetime.now().isoformat()
    except Exception as e:
        task_status[task_id]["status"] = "failed"
        print(f"Error processing CSV: {str(e)}")
    finally:
        # Clean up the temporary file
        os.unlink(file_path)

@app.get("/upload-status/{task_id}")
async def get_upload_status(task_id: str):
    status_info = task_status.get(task_id, {"status": "not found"})
    return {"task_id": task_id, "status_info": status_info}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port=8000)
