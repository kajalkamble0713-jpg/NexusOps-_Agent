"""Insights API routes."""

import logging
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Query

from mcp.mongodb_client import mongodb_mcp
from config import settings

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/insights", tags=["insights"])


@router.get("")
async def get_insights(
    user_id: str,
    insight_type: Optional[str] = None,
    acknowledged: Optional[bool] = None,
    limit: int = Query(default=20, le=100)
):
    """Get insights for a user."""
    filter_dict = {"user_id": user_id}
    
    if insight_type:
        filter_dict["type"] = insight_type
    if acknowledged is not None:
        filter_dict["acknowledged"] = acknowledged
    
    insights = await mongodb_mcp.call_tool(
        tool_name="mongodb_find",
        arguments={
            "collection": "insights",
            "filter": filter_dict,
            "limit": limit,
            "sort": [["generated_at", -1]],
            "database": settings.mongodb_database
        }
    )
    
    return {"insights": insights, "count": len(insights)}


@router.put("/{insight_id}/acknowledge")
async def acknowledge_insight(insight_id: str):
    """Mark an insight as acknowledged."""
    result = await mongodb_mcp.call_tool(
        tool_name="mongodb_update_one",
        arguments={
            "collection": "insights",
            "filter": {"_id": insight_id},
            "update": {
                "$set": {
                    "acknowledged": True,
                    "acknowledged_at": datetime.utcnow().isoformat()
                }
            },
            "database": settings.mongodb_database
        }
    )
    
    return {"message": "Insight acknowledged"}


@router.get("/daily-plan/{user_id}")
async def get_daily_plan(user_id: str, date: Optional[str] = None):
    """Get daily plan for a user."""
    if not date:
        date = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0).isoformat()
    
    plans = await mongodb_mcp.call_tool(
        tool_name="mongodb_find",
        arguments={
            "collection": "daily_plans",
            "filter": {
                "user_id": user_id,
                "date": {"$gte": date}
            },
            "limit": 1,
            "sort": [["date", -1]],
            "database": settings.mongodb_database
        }
    )
    
    return {"plan": plans[0] if plans else None}
