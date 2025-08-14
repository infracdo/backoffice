"""
Tasks API endpoints
"""

from typing import List, Optional, Dict, Any
from .base import BaseAPI
from ..models import TaskHandler


class TasksAPI(BaseAPI):
    """API endpoints for task management"""
    
    async def get_all(
        self,
        page: int = 1,
        page_size: int = 50,
        status: Optional[str] = None,
        task_name: Optional[str] = None
    ) -> List[TaskHandler]:
        """Get all tasks"""
        params = {"page": page, "size": page_size}
        if status:
            params["status"] = status
        if task_name:
            params["task_name"] = task_name
        
        response = await self.get("/api/tasks", params=params)
        
        if isinstance(response, dict) and "content" in response:
            return [TaskHandler(**task_data) for task_data in response["content"]]
        elif isinstance(response, list):
            return [TaskHandler(**task_data) for task_data in response]
        else:
            return []
    
    async def get_by_id(self, task_id: int) -> TaskHandler:
        """Get a specific task by ID"""
        response = await self.get(f"/api/tasks/{task_id}")
        return TaskHandler(**response)
    
    async def create(self, task_data: Dict[str, Any]) -> TaskHandler:
        """Create a new task"""
        response = await self.post("/api/tasks", data=task_data)
        return TaskHandler(**response)
    
    async def update(self, task_id: int, task_data: Dict[str, Any]) -> TaskHandler:
        """Update an existing task"""
        response = await self.put(f"/api/tasks/{task_id}", data=task_data)
        return TaskHandler(**response)
    
    async def delete(self, task_id: int) -> bool:
        """Delete a task"""
        await self.delete(f"/api/tasks/{task_id}")
        return True
    
    async def execute(self, task_id: int, parameters: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Execute a task"""
        data = {"parameters": parameters} if parameters else {}
        return await self.post(f"/api/tasks/{task_id}/execute", data=data)
    
    async def cancel(self, task_id: int) -> Dict[str, Any]:
        """Cancel a running task"""
        return await self.post(f"/api/tasks/{task_id}/cancel")
    
    async def get_result(self, task_id: int) -> Dict[str, Any]:
        """Get task execution result"""
        return await self.get(f"/api/tasks/{task_id}/result")
    
    async def get_logs(self, task_id: int) -> List[Dict[str, Any]]:
        """Get task execution logs"""
        response = await self.get(f"/api/tasks/{task_id}/logs")
        return response if isinstance(response, list) else []
    
    async def get_scheduled_tasks(self) -> List[TaskHandler]:
        """Get all scheduled tasks"""
        response = await self.get("/api/tasks/scheduled")
        
        if isinstance(response, list):
            return [TaskHandler(**task_data) for task_data in response]
        else:
            return []
    
    async def schedule_task(
        self,
        task_name: str,
        schedule_expression: str,
        parameters: Optional[Dict[str, Any]] = None
    ) -> TaskHandler:
        """Schedule a recurring task"""
        data = {
            "task_name": task_name,
            "schedule": schedule_expression,
            "parameters": parameters
        }
        response = await self.post("/api/tasks/schedule", data=data)
        return TaskHandler(**response)
    
    async def unschedule_task(self, task_id: int) -> bool:
        """Remove a scheduled task"""
        await self.delete(f"/api/tasks/scheduled/{task_id}")
        return True
