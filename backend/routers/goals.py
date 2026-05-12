"""Goals CRUD API routes."""

import logging
from typing import Optional
from datetime import datetime

from fastapi import APIRouter, HTTPException, Query

from mcp.mongodb_client import mongodb_mcp
from config import settings

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/goals", tags=["goals"])


@router.get("")
async def get_goals(
    user_id: str,
    category: Optional[str] = None,
    limit: int = Query(default=20, le=100)
):
    """Get goals for a user."""
    filter_dict = {"user_id": user_id}
    if category:
        filter_dict["category"] = category
    
    goals = await mongodb_mcp.call_tool(
        tool_name="mongodb_find",
        arguments={
            "collection": "goals",
            "filter": filter_dict,
            "limit": limit,
            "database": settings.mongodb_database
        }
    )
    
    return {"goals": goals, "count": len(goals)}


@router.post("")
async def create_goal(goal_data: dict):
    """Create a new goal."""
    goal_data["created_at"] = datetime.utcnow().isoformat()
    if "current_progress" not in goal_data:
        goal_data["current_progress"] = 0
    if "milestones" not in goal_data:
        goal_data["milestones"] = []
    
    result = await mongodb_mcp.call_tool(
        tool_name="mongodb_insert_one",
        arguments={
            "collection": "goals",
            "document": goal_data,
            "database": settings.mongodb_database
        }
    )
    
    return {"goal_id": result.get("inserted_id"), "message": "Goal created successfully"}


@router.put("/{goal_id}")
async def update_goal(goal_id: str, update_data: dict):
    """Update a goal."""
    update_data.pop("_id", None)
    update_data["updated_at"] = datetime.utcnow().isoformat()
    
    result = await mongodb_mcp.call_tool(
        tool_name="mongodb_update_one",
        arguments={
            "collection": "goals",
            "filter": {"_id": goal_id},
            "update": {"$set": update_data},
            "database": settings.mongodb_database
        }
    )
    
    if result.get("matched_count", 0) == 0:
        raise HTTPException(status_code=404, detail="Goal not found")
    
    return {"message": "Goal updated successfully"}


@router.put("/{goal_id}/progress")
async def update_goal_progress(goal_id: str, progress: int):
    """Update goal progress."""
    if not 0 <= progress <= 100:
        raise HTTPException(status_code=400, detail="Progress must be between 0 and 100")
    
    result = await mongodb_mcp.call_tool(
        tool_name="mongodb_update_one",
        arguments={
            "collection": "goals",
            "filter": {"_id": goal_id},
            "update": {
                "$set": {
                    "current_progress": progress,
                    "updated_at": datetime.utcnow().isoformat()
                }
            },
            "database": settings.mongodb_database
        }
    )
    
    return {"message": "Progress updated", "progress": progress}


@router.delete("/{goal_id}")
async def delete_goal(goal_id: str):
    """Delete a goal."""
    result = await mongodb_mcp.call_tool(
        tool_name="mongodb_delete_one",
        arguments={
            "collection": "goals",
            "filter": {"_id": goal_id},
            "database": settings.mongodb_database
        }
    )
    
    if result.get("deleted_count", 0) == 0:
        raise HTTPException(status_code=404, detail="Goal not found")
    
    return {"message": "Goal deleted successfully"}
