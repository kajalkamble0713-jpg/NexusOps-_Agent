"""Agent invocation endpoints with SSE streaming."""

import json
import logging
from typing import AsyncGenerator
from datetime import datetime

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from sse_starlette.sse import EventSourceResponse

from models.schemas import AgentRequest, AgentStep
from agents.morning_commander import MorningCommanderAgent
from agents.priority_rebalancer import PriorityRebalancerAgent
from agents.goal_analyst import GoalAnalystAgent
from agents.pattern_engine import PatternEngineAgent
from agents.weekly_planner import WeeklyPlannerAgent

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/agent", tags=["agent"])

# Agent registry
AGENTS = {
    "morning_commander": MorningCommanderAgent,
    "priority_rebalancer": PriorityRebalancerAgent,
    "goal_analyst": GoalAnalystAgent,
    "pattern_engine": PatternEngineAgent,
    "weekly_planner": WeeklyPlannerAgent,
}


def detect_agent_type(user_input: str) -> str:
    """Auto-detect which agent to use based on user input."""
    input_lower = user_input.lower()
    
    if any(kw in input_lower for kw in ["plan my day", "morning", "today's plan", "daily plan"]):
        return "morning_commander"
    elif any(kw in input_lower for kw in ["urgent", "reprioritize", "deadline moved", "something came up", "rebalance"]):
        return "priority_rebalancer"
    elif any(kw in input_lower for kw in ["goal", "goals", "progress", "behind", "on track", "milestone"]):
        return "goal_analyst"
    elif any(kw in input_lower for kw in ["pattern", "how i work", "productivity", "insights", "when should i", "peak"]):
        return "pattern_engine"
    elif any(kw in input_lower for kw in ["next week", "weekly plan", "plan the week", "week ahead"]):
        return "weekly_planner"
    
    return "morning_commander"  # Default


@router.post("/invoke")
async def invoke_agent(request: AgentRequest):
    """
    Invoke an agent with SSE streaming.
    Each step is streamed as a JSON event.
    """
    # Auto-detect agent type if not specified
    agent_type = request.agent_type or detect_agent_type(request.input)
    
    if agent_type not in AGENTS:
        raise HTTPException(status_code=400, detail=f"Unknown agent type: {agent_type}")
    
    agent_class = AGENTS[agent_type]
    agent = agent_class()
    
    async def generate() -> AsyncGenerator[str, None]:
        try:
            async for step in agent.run(
                user_id=request.user_id,
                user_input=request.input,
                context=request.context
            ):
                step_data = {
                    "type": step.type,
                    "content": step.content,
                    "mongodb_tool": step.mongodb_tool,
                    "timestamp": step.timestamp.isoformat(),
                    "metadata": step.metadata
                }
                yield f"data: {json.dumps(step_data)}\n\n"
            
            yield "data: [DONE]\n\n"
        
        except Exception as e:
            logger.error(f"Agent error: {e}")
            error_step = {
                "type": "error",
                "content": f"Agent encountered an error: {str(e)}",
                "mongodb_tool": None,
                "timestamp": datetime.utcnow().isoformat(),
                "metadata": {}
            }
            yield f"data: {json.dumps(error_step)}\n\n"
            yield "data: [DONE]\n\n"
    
    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )


@router.get("/types")
async def get_agent_types():
    """Get available agent types."""
    return {
        "agents": [
            {
                "id": "morning_commander",
                "name": "Morning Commander",
                "description": "Plans your day intelligently based on tasks, goals, and energy",
                "trigger_phrases": ["Plan my day", "Morning briefing", "What should I do today?"]
            },
            {
                "id": "priority_rebalancer",
                "name": "Priority Rebalancer",
                "description": "Rearranges your schedule when urgent tasks appear",
                "trigger_phrases": ["Something urgent came up", "Reprioritize everything", "Deadline moved"]
            },
            {
                "id": "goal_analyst",
                "name": "Goal Health Analyst",
                "description": "Analyzes goal progress and suggests recovery actions",
                "trigger_phrases": ["Review my goals", "Which goals are in danger?", "Goal health check"]
            },
            {
                "id": "pattern_engine",
                "name": "Pattern Intelligence Engine",
                "description": "Discovers your productivity patterns and optimizes scheduling",
                "trigger_phrases": ["Show me how I work", "When am I most productive?", "Analyze my patterns"]
            },
            {
                "id": "weekly_planner",
                "name": "Autonomous Weekly Planner",
                "description": "Generates balanced 5-day schedules",
                "trigger_phrases": ["Plan next week", "Weekly schedule", "Plan the week ahead"]
            }
        ]
    }
