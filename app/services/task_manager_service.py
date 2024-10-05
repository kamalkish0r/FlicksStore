from typing import Dict, Optional
from datetime import datetime

class TaskManagerService:
    def __init__(self):
        # In-memory storage for task status (TODO: replace with a database in production)
        self.task_status: Dict[str, Dict[str, str]] = {}

    def create_task(self) -> str:
        task_id = f"task_{len(self.task_status) + 1}"
        start_time = datetime.now().isoformat()
        self.task_status[task_id] = {
            "status": "uploading",
            "start_time": start_time,
            "completed_time": None
        }
        return task_id

    def get_status(self, task_id: str) -> Dict[str, str]:
        return self.task_status.get(task_id, {"status": "not found"})

    def update_status(self, task_id: str, status: str, completed_time: Optional[str] = None):
        if task_id in self.task_status:
            self.task_status[task_id]["status"] = status
            if completed_time:
                self.task_status[task_id]["completed_time"] = completed_time
        else:
            raise ValueError(f"Task ID {task_id} not found")

task_manager_service = TaskManagerService()

def get_task_manager_service():
    return task_manager_service