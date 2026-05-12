"""Habits CRUD API routes."""

import logging
from datetime import datetime, timedelta
from typing import Optional

from fastapi import APIRouter, HTTPException, Query

from mcp.mongodb_client import mongodb_mcp
from config import settings

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/habits", tags=["habits"])


@router.get("")
async def get_habits(
    user_id: str,
    limit: int = Query(default=20, le=100)
):
    """Get habits for a user."""
    habits = await mongodb_mcp.call_tool(
        tool_name="mongodb_find",
        arguments={
            "collection": "habits",
            "filter": {"user_id": user_id},
            "limit": limit,
            "database": settings.mongodb_database
        }
    )
    
    return {"habits": habits, "count": len(habits)}


@router.post("")
async def create_habit(habit_data: dict):
    """Create a new habit."""
    habit_data["created_at"] = datetime.utcnow().isoformat()
    habit_data["completion_log"] = []
    habit_data["streak_count"] = 0
    habit_data["best_streak"] = 0
    
    result = await mongodb_mcp.call_tool(
        tool_name="mongodb_insert_one",
        arguments={
            "collection": "habits",
            "document": habit_data,
            "database": settings.mongodb_database
        }
    )
    
    return {"habit_id": result.get("inserted_id"), "message": "Habit created successfully"}


@router.post("/{habit_id}/complete")
async def complete_habit(habit_id: str):
    """Mark a habit as completed for today."""
    today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    
    # Get current habit
    habits = await mongodb_mcp.call_tool(
        tool_name="mongodb_find",
        arguments={
            "collection": "habits",
            "filter": {"_id": habit_id},
            "limit": 1,
            "database": settings.mongodb_database
        }
    )
    
    if not habits:
        raise HTTPException(status_code=404, detail="Habit not found")
    
    habit = habits[0]
    completion_log = habit.get("completion_log", [])
    
    # Check if already completed today
    today_str = today.isoformat()
    if today_str in completion_log:
        return {"message": "Habit already completed today", "streak": habit.get("streak_count", 0)}
    
    # Add today's completion
    completion_log.append(today_str)
    
    # Calculate streak
    streak = _calculate_streak(completion_log)
    best_streak = max(streak, habit.get("best_streak", 0))
    
    result = await mongodb_mcp.call_tool(
        tool_name="mongodb_update_one",
        arguments={
            "collection": "habits",
            "filter": {"_id": habit_id},
            "update": {
                "$set": {
                    "completion_log": completion_log,
                    "streak_count": streak,
                    "best_streak": best_streak,
                    "updated_at": datetime.utcnow().isoformat()
                }
            },
            "database": settings.mongodb_database
        }
    )
    
    return {
        "message": "Habit completed!",
        "streak": streak,
        "best_streak": best_streak
    }


@router.delete("/{habit_id}")
async def delete_habit(habit_id: str):
    """Delete a habit."""
    result = await mongodb_mcp.call_tool(
        tool_name="mongodb_delete_one",
        arguments={
            "collection": "habits",
            "filter": {"_id": habit_id},
            "database": settings.mongodb_database
        }
    )
    
    if result.get("deleted_count", 0) == 0:
        raise HTTPException(status_code=404, detail="Habit not found")
    
    return {"message": "Habit deleted successfully"}


def _calculate_streak(completion_log: list) -> int:
    """Calculate current streak from completion log."""
    if not completion_log:
        return 0
    
    today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    streak = 0
    current_date = today
    
    # Sort completions
    sorted_completions = sorted(completion_log, reverse=True)
    
    for completion in sorted_completions:
        try:
            completion_date = datetime.fromisoformat(completion.replace("Z", "+00:00"))
            completion_date = completion_date.replace(hour=0, minute=0, second=0, microsecond=0)
            
            if completion_date == current_date:
                streak += 1
                current_date -= timedelta(days=1)
            elif completion_date < current_date:
                break
        except Exception:
            continue
    
    return streak
