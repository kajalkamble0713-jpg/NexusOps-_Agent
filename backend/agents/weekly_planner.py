"""Autonomous Weekly Planner Agent — Generates balanced 5-day schedules."""

import json
import logging
from typing import AsyncGenerator, Dict, Any
from datetime import datetime, timedelta

from agents.base_agent import BaseAgent
from models.schemas import AgentStep

logger = logging.getLogger(__name__)


class WeeklyPlannerAgent(BaseAgent):
    """
    Autonomous Weekly Planner Agent.
    
    Generates a full 5-day schedule by:
    1. Fetching all pending tasks + upcoming deadlines
    2. Reviewing goal milestones due next week
    3. Considering habit targets
    4. Generating a balanced time-blocked schedule
    5. Saving plan to MongoDB
    """
    
    SYSTEM_INSTRUCTION = """You are the Autonomous Weekly Planner, an intelligent scheduling agent for NexusOps.

Your role is to create balanced, realistic 5-day work schedules.

When planning a week:
- Balance deep work, meetings, and administrative tasks
- Protect morning hours for high-priority work
- Include buffer time for unexpected tasks
- Align tasks with goal milestones
- Consider energy levels throughout the week

Respond with structured JSON for the weekly plan."""
    
    def __init__(self):
        super().__init__("weekly_planner")
    
    async def run(
        self,
        user_id: str,
        user_input: str,
        context: Dict[str, Any] = None
    ) -> AsyncGenerator[AgentStep, None]:
        """Run the Weekly Planner agent."""
        self.clear_steps()
        
        # Step 1: Start planning
        step = AgentStep(
            type="reasoning",
            content="Starting autonomous weekly planning session. Gathering all relevant data..."
        )
        self.steps.append(step)
        yield step
        
        # Calculate next week dates
        today = datetime.utcnow()
        days_until_monday = (7 - today.weekday()) % 7
        if days_until_monday == 0:
            days_until_monday = 7
        next_monday = today + timedelta(days=days_until_monday)
        next_friday = next_monday + timedelta(days=4)
        
        # Step 2: Fetch pending tasks
        step = AgentStep(
            type="query",
            content="Loading all pending tasks and upcoming deadlines from MongoDB...",
            mongodb_tool="mongodb_find"
        )
        self.steps.append(step)
        yield step
        
        pending_tasks = await self.query_mongodb(
            collection="tasks",
            filter_dict={
                "user_id": user_id,
                "status": {"$in": ["backlog", "today", "in_progress"]},
            },
            limit=50
        )
        
        step = AgentStep(
            type="insight",
            content=f"Found {len(pending_tasks)} pending tasks to schedule across next week."
        )
        self.steps.append(step)
        yield step
        
        # Step 3: Fetch goal milestones
        step = AgentStep(
            type="query",
            content="Checking goal milestones due next week...",
            mongodb_tool="mongodb_find"
        )
        self.steps.append(step)
        yield step
        
        goals = await self.query_mongodb(
            collection="goals",
            filter_dict={
                "user_id": user_id,
                "current_progress": {"$lt": 100}
            },
            limit=10
        )
        
        # Filter milestones due next week
        upcoming_milestones = []
        for goal in goals:
            for milestone in goal.get("milestones", []):
                if not milestone.get("completed"):
                    target = milestone.get("target_date", "")
                    if target:
                        try:
                            target_dt = datetime.fromisoformat(target.replace("Z", "+00:00"))
                            if next_monday <= target_dt <= next_friday + timedelta(days=1):
                                upcoming_milestones.append({
                                    "goal_title": goal.get("title"),
                                    "milestone": milestone.get("title"),
                                    "due": target
                                })
                        except Exception:
                            pass
        
        step = AgentStep(
            type="insight",
            content=f"Found {len(upcoming_milestones)} goal milestones due next week."
        )
        self.steps.append(step)
        yield step
        
        # Step 4: Fetch habits
        step = AgentStep(
            type="query",
            content="Loading habit targets for the week...",
            mongodb_tool="mongodb_find"
        )
        self.steps.append(step)
        yield step
        
        habits = await self.query_mongodb(
            collection="habits",
            filter_dict={"user_id": user_id},
            limit=15
        )
        
        # Step 5: Generate weekly plan with Gemini
        step = AgentStep(
            type="reasoning",
            content="Applying Gemini AI to generate your optimized 5-day schedule..."
        )
        self.steps.append(step)
        yield step
        
        tasks_summary = json.dumps([{
            "title": t.get("title"),
            "priority": t.get("priority", "normal"),
            "estimated_minutes": t.get("estimated_minutes", 30),
            "due_date": t.get("due_date"),
            "tags": t.get("tags", [])
        } for t in pending_tasks[:20]], indent=2)
        
        milestones_summary = json.dumps(upcoming_milestones, indent=2)
        
        habits_summary = json.dumps([{
            "name": h.get("name"),
            "frequency": h.get("frequency"),
            "category": h.get("category")
        } for h in habits[:8]], indent=2)
        
        prompt = f"""User request: {user_input}

WEEK: {next_monday.strftime("%B %d")} - {next_friday.strftime("%B %d, %Y")}

PENDING TASKS:
{tasks_summary}

GOAL MILESTONES DUE THIS WEEK:
{milestones_summary}

HABITS TO MAINTAIN:
{habits_summary}

Create a balanced 5-day schedule. For each day include:
- 2-3 deep work blocks (90 min each)
- Administrative time
- Habit time
- Buffer for unexpected tasks

Respond with JSON:
{{
  "week_theme": "This week's focus theme",
  "schedule": {{
    "Monday": [
      {{"time": "09:00-10:30", "task": "title", "type": "deep_work|meeting|admin|habit|buffer", "priority": "high"}}
    ],
    "Tuesday": [...],
    "Wednesday": [...],
    "Thursday": [...],
    "Friday": [...]
  }},
  "key_deliverables": ["What must be done by Friday"],
  "habit_schedule": {{"habit_name": "days to complete"}},
  "planning_notes": "Any important notes about the week"
}}"""
        
        gemini_response = await self.generate_with_gemini(prompt, self.SYSTEM_INSTRUCTION)
        weekly_plan = self._extract_weekly_plan(gemini_response)
        
        # Step 6: Save weekly plan to MongoDB
        step = AgentStep(
            type="action",
            content="Saving 5-day weekly plan to MongoDB...",
            mongodb_tool="mongodb_insert_one"
        )
        self.steps.append(step)
        yield step
        
        # Save a daily plan for each day of the week
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        schedule = weekly_plan.get("schedule", {})
        
        for i, day_name in enumerate(days):
            day_date = next_monday + timedelta(days=i)
            day_schedule = schedule.get(day_name, [])
            
            await self.write_mongodb("daily_plans", {
                "user_id": user_id,
                "date": day_date.isoformat(),
                "planned_tasks": [],
                "actual_schedule": day_schedule,
                "morning_brief": f"Week plan: {weekly_plan.get('week_theme', '')}",
                "agent_insights": weekly_plan.get("key_deliverables", []),
                "created_at": datetime.utcnow().isoformat()
            })
        
        # Step 7: Build result
        schedule_preview = ""
        for day in days[:5]:
            day_blocks = schedule.get(day, [])
            if day_blocks:
                schedule_preview += f"\n📅 {day}:\n"
                for block in day_blocks[:3]:
                    schedule_preview += f"  {block.get('time', '')} — {block.get('task', '')} ({block.get('type', '')})\n"
        
        deliverables = "\n".join(
            f"  {i+1}. {d}"
            for i, d in enumerate(weekly_plan.get("key_deliverables", [])[:5])
        )
        
        result_content = f"""✅ Your 5-Day Weekly Plan is Ready!

🎯 Week Theme: {weekly_plan.get('week_theme', 'Focused execution week')}

{schedule_preview}

📋 Key Deliverables by Friday:
{deliverables if deliverables else '  Complete all high-priority tasks'}

📝 Planning Notes:
{weekly_plan.get('planning_notes', 'Have a productive week!')}

All 5 daily plans have been saved to MongoDB."""
        
        step = AgentStep(
            type="result",
            content=result_content,
            metadata={"weekly_plan": weekly_plan}
        )
        self.steps.append(step)
        yield step
    
    def _extract_weekly_plan(self, response: str) -> Dict[str, Any]:
        """Extract weekly plan from Gemini response."""
        try:
            start = response.find("{")
            end = response.rfind("}") + 1
            if start >= 0 and end > start:
                return json.loads(response[start:end])
        except Exception:
            pass
        
        # Default weekly plan
        default_day = [
            {"time": "09:00-10:30", "task": "Deep work block", "type": "deep_work", "priority": "high"},
            {"time": "10:30-11:00", "task": "Email & communications", "type": "admin", "priority": "normal"},
            {"time": "11:00-12:30", "task": "Priority tasks", "type": "deep_work", "priority": "high"},
            {"time": "12:30-13:30", "task": "Lunch break", "type": "break", "priority": "low"},
            {"time": "13:30-15:00", "task": "Meetings & collaboration", "type": "meeting", "priority": "normal"},
            {"time": "15:00-16:30", "task": "Administrative tasks", "type": "admin", "priority": "normal"},
            {"time": "16:30-17:00", "task": "Review & planning", "type": "admin", "priority": "low"}
        ]
        
        return {
            "week_theme": "Focused execution and goal progress",
            "schedule": {
                "Monday": default_day,
                "Tuesday": default_day,
                "Wednesday": default_day,
                "Thursday": default_day,
                "Friday": default_day
            },
            "key_deliverables": [
                "Complete all critical priority tasks",
                "Make progress on active goals",
                "Maintain daily habits"
            ],
            "habit_schedule": {},
            "planning_notes": "Stay focused on your top priorities. Protect deep work time."
        }
