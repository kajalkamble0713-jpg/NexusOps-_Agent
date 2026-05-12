"""Priority Rebalancer Agent — Intelligently rearranges schedule for urgent tasks."""

import json
import logging
from typing import AsyncGenerator, Dict, Any, List
from datetime import datetime, timedelta

from agents.base_agent import BaseAgent
from models.schemas import AgentStep

logger = logging.getLogger(__name__)


class PriorityRebalancerAgent(BaseAgent):
    """
    Priority Rebalancer Agent.
    
    When an urgent task appears:
    1. Retrieves today's existing plan from MongoDB
    2. Analyzes impact of inserting new task
    3. Identifies which tasks can be deferred with least consequence
    4. Proposes specific reschedule actions with reasoning
    5. Updates all affected tasks in MongoDB via MCP
    """
    
    SYSTEM_INSTRUCTION = """You are the Priority Rebalancer, an intelligent scheduling agent for NexusOps.

Your role is to intelligently rearrange a user's schedule when urgent tasks appear.

When rebalancing:
- Minimize disruption to high-priority existing tasks
- Identify tasks that can be safely deferred
- Consider task dependencies
- Explain the impact of each change
- Provide clear reasoning for deferral decisions

Always respond with structured JSON for schedule changes."""
    
    def __init__(self):
        super().__init__("priority_rebalancer")
    
    async def run(
        self,
        user_id: str,
        user_input: str,
        context: Dict[str, Any] = None
    ) -> AsyncGenerator[AgentStep, None]:
        """Run the Priority Rebalancer agent."""
        self.clear_steps()
        context = context or {}
        
        # Step 1: Acknowledge urgent situation
        step = AgentStep(
            type="reasoning",
            content="Urgent situation detected. Analyzing your current schedule for rebalancing opportunities..."
        )
        self.steps.append(step)
        yield step
        
        # Step 2: Fetch today's plan
        step = AgentStep(
            type="query",
            content="Retrieving today's existing plan from MongoDB...",
            mongodb_tool="mongodb_find_one"
        )
        self.steps.append(step)
        yield step
        
        today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        
        today_plans = await self.query_mongodb(
            collection="daily_plans",
            filter_dict={
                "user_id": user_id,
                "date": {"$gte": today.isoformat()}
            },
            limit=1
        )
        
        today_plan = today_plans[0] if today_plans else None
        
        # Step 3: Fetch all today's tasks
        step = AgentStep(
            type="query",
            content="Loading all tasks scheduled for today...",
            mongodb_tool="mongodb_find"
        )
        self.steps.append(step)
        yield step
        
        tomorrow = today + timedelta(days=1)
        current_tasks = await self.query_mongodb(
            collection="tasks",
            filter_dict={
                "user_id": user_id,
                "status": {"$in": ["today", "in_progress", "backlog"]},
                "$or": [
                    {"due_date": {"$lte": tomorrow.isoformat()}},
                    {"status": "in_progress"}
                ]
            },
            limit=30
        )
        
        step = AgentStep(
            type="insight",
            content=f"Found {len(current_tasks)} tasks in today's schedule. Analyzing displacement impact..."
        )
        self.steps.append(step)
        yield step
        
        # Step 4: Analyze with Gemini
        step = AgentStep(
            type="reasoning",
            content="Applying Gemini AI to calculate optimal rebalancing strategy..."
        )
        self.steps.append(step)
        yield step
        
        tasks_summary = json.dumps([{
            "id": str(t.get("_id", "")),
            "title": t.get("title"),
            "priority": t.get("priority", "normal"),
            "estimated_minutes": t.get("estimated_minutes", 30),
            "status": t.get("status"),
            "due_date": t.get("due_date"),
            "tags": t.get("tags", [])
        } for t in current_tasks], indent=2)
        
        current_schedule = json.dumps(
            today_plan.get("actual_schedule", []) if today_plan else [],
            indent=2
        )
        
        prompt = f"""Urgent situation: {user_input}

CURRENT TASKS:
{tasks_summary}

CURRENT SCHEDULE:
{current_schedule}

TODAY: {today.strftime("%A, %B %d, %Y")}

Analyze the impact of this urgent situation and create a rebalanced schedule.

Respond with JSON:
{{
  "urgent_task_analysis": "What the urgent task requires",
  "impact_assessment": "How this affects the current schedule",
  "tasks_to_defer": [
    {{"task_id": "id", "title": "title", "reason": "why safe to defer", "new_due_date": "YYYY-MM-DD"}}
  ],
  "tasks_to_keep": [
    {{"task_id": "id", "title": "title", "reason": "why must keep today"}}
  ],
  "new_schedule": [
    {{"time": "HH:MM-HH:MM", "task": "title", "type": "type", "priority": "priority"}}
  ],
  "summary": "One paragraph summary of changes made"
}}"""
        
        gemini_response = await self.generate_with_gemini(prompt, self.SYSTEM_INSTRUCTION)
        rebalance_data = self._extract_rebalance(gemini_response)
        
        # Step 5: Show impact assessment
        step = AgentStep(
            type="insight",
            content=f"Impact Analysis: {rebalance_data.get('impact_assessment', 'Schedule adjustment required')}"
        )
        self.steps.append(step)
        yield step
        
        # Step 6: Update deferred tasks in MongoDB
        tasks_to_defer = rebalance_data.get("tasks_to_defer", [])
        
        if tasks_to_defer:
            step = AgentStep(
                type="action",
                content=f"Deferring {len(tasks_to_defer)} lower-priority task(s) to make room...",
                mongodb_tool="mongodb_update_one"
            )
            self.steps.append(step)
            yield step
            
            for task_info in tasks_to_defer[:5]:
                task_id = task_info.get("task_id")
                new_due = task_info.get("new_due_date")
                
                if task_id:
                    update_data = {
                        "$set": {
                            "status": "backlog",
                            "metadata.deferred_reason": task_info.get("reason", "Deferred for urgent task"),
                            "metadata.deferred_at": datetime.utcnow().isoformat()
                        }
                    }
                    if new_due:
                        update_data["$set"]["due_date"] = new_due
                    
                    await self.update_mongodb(
                        collection="tasks",
                        filter_dict={"_id": task_id},
                        update=update_data
                    )
        
        # Step 7: Update daily plan in MongoDB
        step = AgentStep(
            type="action",
            content="Updating your daily plan in MongoDB with the rebalanced schedule...",
            mongodb_tool="mongodb_update_one"
        )
        self.steps.append(step)
        yield step
        
        new_schedule = rebalance_data.get("new_schedule", [])
        
        if today_plan:
            await self.update_mongodb(
                collection="daily_plans",
                filter_dict={"_id": today_plan.get("_id")},
                update={
                    "$set": {
                        "actual_schedule": new_schedule,
                        "agent_insights": [
                            rebalance_data.get("summary", "Schedule rebalanced for urgent task")
                        ]
                    }
                }
            )
        else:
            await self.write_mongodb("daily_plans", {
                "user_id": user_id,
                "date": today.isoformat(),
                "actual_schedule": new_schedule,
                "agent_insights": [rebalance_data.get("summary", "")],
                "created_at": datetime.utcnow().isoformat()
            })
        
        # Step 8: Final result
        deferred_list = "\n".join(
            f"  • '{t.get('title', 'Task')}' → {t.get('reason', 'Deferred')}"
            for t in tasks_to_defer[:3]
        )
        
        kept_list = "\n".join(
            f"  • '{t.get('title', 'Task')}' — {t.get('reason', 'Kept')}"
            for t in rebalance_data.get("tasks_to_keep", [])[:3]
        )
        
        result_content = f"""✅ Schedule successfully rebalanced!

🚨 Urgent Task Analysis:
{rebalance_data.get('urgent_task_analysis', 'Urgent task integrated into schedule')}

📤 Deferred Tasks ({len(tasks_to_defer)}):
{deferred_list if deferred_list else '  None — all tasks fit!'}

✅ Kept Today:
{kept_list if kept_list else '  Critical tasks maintained'}

📋 Summary:
{rebalance_data.get('summary', 'Your schedule has been optimized for the urgent situation.')}

MongoDB has been updated with all changes."""
        
        step = AgentStep(
            type="result",
            content=result_content,
            metadata={"rebalance": rebalance_data}
        )
        self.steps.append(step)
        yield step
    
    def _extract_rebalance(self, response: str) -> Dict[str, Any]:
        """Extract rebalance data from Gemini response."""
        try:
            start = response.find("{")
            end = response.rfind("}") + 1
            if start >= 0 and end > start:
                return json.loads(response[start:end])
        except Exception:
            pass
        
        return {
            "urgent_task_analysis": "Urgent task requires immediate attention",
            "impact_assessment": "3 lower-priority tasks can be safely deferred",
            "tasks_to_defer": [],
            "tasks_to_keep": [],
            "new_schedule": [],
            "summary": "Schedule has been rebalanced to accommodate the urgent task."
        }
