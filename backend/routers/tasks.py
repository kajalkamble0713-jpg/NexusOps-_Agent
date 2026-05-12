"""Task CRUD API routes."""

import logging
from typing import List, Optional
from datetime import datetime

from fastapi import APIRouter, HTTPException, Query
from bson import ObjectId

from mcp.mongodb_client import mongodb_mcp
from config import settings

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("")
async def get_tasks(
    user_id: str,
    status: Optional[str] = None,
    priority: Optional[str] = None,
    limit: int = Query(default=50, le=200)
):
    """Get tasks for a user."""
    filter_dict = {"user_id": user_id}
    
    if status:
        filter_dict["status"] = status
    if priority:
        filter_dict["priority"] = priority
    
    tasks = await mongodb_mcp.call_tool(
        tool_name="mongodb_find",
        arguments={
            "collection": "tasks",
            "filter": filter_dict,
            "limit": limit,
            "sort": [["created_at", -1]],
            "database": settings.mongodb_database
        }
    )
    
    return {"tasks": tasks, "count": len(tasks)}


@router.post("")
async def create_task(task_data: dict):
    """Create a new task."""
    task_data["created_at"] = datetime.utcnow().isoformat()
    
    if "status" not in task_data:
        task_data["status"] = "backlog"
    if "priority" not in task_data:
        task_data["priority"] = "normal"
    
    result = await mongodb_mcp.call_tool(
        tool_name="mongodb_insert_one",
        arguments={
            "collection": "tasks",
            "document": task_data,
            "database": settings.mongodb_database
        }
    )
    
    return {"task_id": result.get("inserted_id"), "message": "Task created successfully"}


@router.put("/{task_id}")
async def update_task(task_id: str, update_data: dict):
    """Update a task."""
    update_data.pop("_id", None)
    update_data["updated_at"] = datetime.utcnow().isoformat()
    
    # If marking as done, set completed_at
    if update_data.get("status") == "done" and "completed_at" not in update_data:
        update_data["completed_at"] = datetime.utcnow().isoformat()
    
    result = await mongodb_mcp.call_tool(
        tool_name="mongodb_update_one",
        arguments={
            "collection": "tasks",
            "filter": {"_id": task_id},
            "update": {"$set": update_data},
            "database": settings.mongodb_database
        }
    )
    
    if result.get("matched_count", 0) == 0:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return {"message": "Task updated successfully", "modified": result.get("modified_count", 0)}


@router.delete("/{task_id}")
async def delete_task(task_id: str):
    """Delete a task."""
    result = await mongodb_mcp.call_tool(
        tool_name="mongodb_delete_one",
        arguments={
            "collection": "tasks",
            "filter": {"_id": task_id},
            "database": settings.mongodb_database
        }
    )
    
    if result.get("deleted_count", 0) == 0:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return {"message": "Task deleted successfully"}


@router.get("/stats/{user_id}")
async def get_task_stats(user_id: str):
    """Get task statistics for a user."""
    statuses = ["backlog", "today", "in_progress", "done"]
    stats = {}
    
    for status in statuses:
        result = await mongodb_mcp.call_tool(
            tool_name="mongodb_count",
            arguments={
                "collection": "tasks",
                "filter": {"user_id": user_id, "status": status},
                "database": settings.mongodb_database
            }
        )
        stats[status] = result.get("count", 0)
    
    return {"stats": stats, "total": sum(stats.values())}
