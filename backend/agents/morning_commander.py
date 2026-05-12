"""Morning Commander Agent — Plans your day intelligently."""

import json
import logging
from typing import AsyncGenerator, Dict, Any, List, Optional
from datetime import datetime, timedelta

from agents.base_agent import BaseAgent
from models.schemas import AgentStep

logger = logging.getLogger(__name__)


class MorningCommanderAgent(BaseAgent):
    """
    Morning Commander Agent.
    
    Autonomously plans your day by:
    1. Querying all pending tasks (due today + overdue)
    2. Checking active goals and weekly targets
    3. Reviewing habit completions for the past 7 days
    4. Reasoning with Gemini to rank tasks by urgency × impact × energy
    5. Generating a time-blocked daily plan
    6. Writing the plan back to MongoDB
    """
    
    SYSTEM_INSTRUCTION = """You are the Morning Commander, an intelligent daily planning agent for NexusOps.

Your role is to analyze a user's tasks, goals, and habits, then create an optimized time-blocked daily plan.

When creating plans:
- Consider task priority (critical > high > normal > low)
- Factor in energy levels (schedule demanding tasks during peak hours)
- Respect time constraints and meetings
- Balance deep work with administrative tasks
- Flag overdue items proactively
- Provide clear reasoning for scheduling decisions

Always respond with structured JSON when asked for a plan.
Be concise, actionable, and specific in your recommendations."""
    
    def __init__(self):
        super().__init__("morning_commander")
    
    async def run(
        self,
        user_id: str,
        user_input: str,
        context: Dict[str, Any] = None
    ) -> AsyncGenerator[AgentStep, None]:
        """Run the Morning Commander agent."""
        self.clear_steps()
        context = context or {}
        
        # Step 1: Greet and acknowledge
        step = AgentStep(
            type="reasoning",
            content="Good morning! Starting your daily planning session. Let me gather your operational data..."
        )
        self.steps.append(step)
        yield step
        
        # Step 2: Query pending tasks
        step = AgentStep(
            type="query",
            content="Querying MongoDB for pending and overdue tasks...",
            mongodb_tool="mongodb_find"
        )
        self.steps.append(step)
        yield step
        
        today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
        tomorrow = today + timedelta(days=1)
        
        tasks = await self.query_mongodb(
            collection="tasks",
            filter_dict={
                "user_id": user_id,
                "status": {"$in": ["backlog", "today", "in_progress"]},
                "$or": [
                    {"due_date": {"$lte": tomorrow.isoformat()}},
                    {"due_date": None},
                    {"status": "in_progress"}
                ]
            },
            limit=50
        )
        
        step = AgentStep(
            type="insight",
            content=f"Found {len(tasks)} pending tasks. Analyzing priorities and deadlines..."
        )
        self.steps.append(step)
        yield step
        
        # Step 3: Check for overdue tasks
        overdue_tasks = []
        for task in tasks:
            if task.get("due_date"):
                try:
                    due = datetime.fromisoformat(task["due_date"].replace("Z", "+00:00"))
                    if due < datetime.utcnow():
                        days_overdue = (datetime.utcnow() - due).days
                        task["days_overdue"] = days_overdue
                        overdue_tasks.append(task)
                except Exception:
                    pass
        
        if overdue_tasks:
            overdue_msg = f"⚠️ Detected {len(overdue_tasks)} overdue task(s):\n"
            for t in overdue_tasks[:3]:
                days = t.get("days_overdue", 0)
                overdue_msg += f"  • '{t['title']}' — {days} day(s) overdue\n"
            
            if len(overdue_tasks) > 3:
                overdue_msg += f"  ... and {len(overdue_tasks) - 3} more"
            
            step = AgentStep(
                type="insight",
                content=overdue_msg
            )
            self.steps.append(step)
            yield step
        
        # Step 4: Query active goals
        step = AgentStep(
            type="query",
            content="Checking active goals and weekly progress targets...",
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
        
        step = AgentStep(
            type="insight",
            content=f"Found {len(goals)} active goals. Checking alignment with today's tasks..."
        )
        self.steps.append(step)
        yield step
        
        # Step 5: Query habit completions
        step = AgentStep(
            type="query",
            content="Reviewing habit completion data for the past 7 days...",
            mongodb_tool="mongodb_find"
        )
        self.steps.append(step)
        yield step
        
        week_ago = today - timedelta(days=7)
        habits = await self.query_mongodb(
            collection="habits",
            filter_dict={"user_id": user_id},
            limit=20
        )
        
        # Calculate habit completion rates
        habit_summary = []
        for habit in habits:
            completions = habit.get("completion_log", [])
            recent_completions = sum(
                1 for c in completions
                if isinstance(c, str) and c >= week_ago.isoformat()
            )
            habit_summary.append({
                "name": habit["name"],
                "streak": habit.get("streak_count", 0),
                "recent_completions": recent_completions,
                "frequency": habit.get("frequency", "daily")
            })
        
        step = AgentStep(
            type="insight",
            content=f"Analyzed {len(habits)} habits. Current streak data loaded."
        )
        self.steps.append(step)
        yield step
        
        # Step 6: Generate plan with Gemini
        step = AgentStep(
            type="reasoning",
            content="Applying Gemini AI reasoning to optimize your schedule based on priorities, energy, and goals..."
        )
        self.steps.append(step)
        yield step
        
        # Build context for Gemini
        tasks_summary = json.dumps([{
            "title": t.get("title"),
            "priority": t.get("priority", "normal"),
            "estimated_minutes": t.get("estimated_minutes", 30),
            "status": t.get("status"),
            "days_overdue": t.get("days_overdue", 0),
            "tags": t.get("tags", [])
        } for t in tasks[:15]], indent=2)
        
        goals_summary = json.dumps([{
            "title": g.get("title"),
            "progress": g.get("current_progress", 0),
            "category": g.get("category"),
            "weekly_target": g.get("weekly_target")
        } for g in goals[:5]], indent=2)
        
        prompt = f"""User request: {user_input}

PENDING TASKS:
{tasks_summary}

ACTIVE GOALS:
{goals_summary}

HABIT SUMMARY:
{json.dumps(habit_summary[:5], indent=2)}

TODAY'S DATE: {today.strftime("%A, %B %d, %Y")}

Create an optimized time-blocked daily plan. Consider:
1. Task priorities and deadlines
2. Energy levels mentioned by user
3. Goal alignment
4. Habit completion needs

Respond with:
1. A brief analysis (2-3 sentences)
2. A time-blocked schedule in JSON format with this structure:
{{
  "schedule": [
    {{"time": "09:00-10:30", "task": "Task title", "type": "deep_work|meeting|admin|break", "reason": "Why this slot"}}
  ],
  "key_insights": ["insight1", "insight2"],
  "deferred_tasks": ["task titles that won't fit today"],
  "focus_theme": "Today's main focus in one sentence"
}}"""
        
        gemini_response = await self.generate_with_gemini(prompt, self.SYSTEM_INSTRUCTION)
        
        # Step 7: Parse and structure the plan
        step = AgentStep(
            type="action",
            content="Structuring your optimized daily plan..."
        )
        self.steps.append(step)
        yield step
        
        # Extract JSON from response
        plan_data = self._extract_plan(gemini_response)
        
        # Step 8: Write plan to MongoDB
        step = AgentStep(
            type="action",
            content="Saving your daily plan to MongoDB...",
            mongodb_tool="mongodb_insert_one"
        )
        self.steps.append(step)
        yield step
        
        daily_plan = {
            "user_id": user_id,
            "date": today.isoformat(),
            "planned_tasks": [t.get("_id") for t in tasks[:10] if t.get("_id")],
            "actual_schedule": plan_data.get("schedule", []),
            "morning_brief": gemini_response[:500],
            "agent_insights": plan_data.get("key_insights", []),
            "created_at": datetime.utcnow().isoformat()
        }
        
        await self.write_mongodb("daily_plans", daily_plan)
        
        # Step 9: Handle overdue task prompts
        if overdue_tasks:
            for task in overdue_tasks[:2]:
                if task.get("days_overdue", 0) >= 3:
                    step = AgentStep(
                        type="insight",
                        content=f"⚠️ '{task['title']}' has been delayed {task['days_overdue']} days. Should I reschedule, delegate, or drop it?"
                    )
                    self.steps.append(step)
                    yield step
        
        # Step 10: Final result
        schedule_text = ""
        for block in plan_data.get("schedule", [])[:8]:
            schedule_text += f"\n  {block.get('time', '')} — {block.get('task', '')} ({block.get('type', '')})"
        
        focus_theme = plan_data.get("focus_theme", "Focused execution day")
        key_insights = plan_data.get("key_insights", [])
        
        result_content = f"""✅ Your optimized day is ready!

🎯 Today's Focus: {focus_theme}

📅 Time-Blocked Schedule:{schedule_text}

💡 Key Insights:
{chr(10).join(f'  • {i}' for i in key_insights[:3])}

Your plan has been saved to MongoDB. Have a productive day!"""
        
        step = AgentStep(
            type="result",
            content=result_content,
            metadata={"plan": plan_data}
        )
        self.steps.append(step)
        yield step
    
    def _extract_plan(self, response: str) -> Dict[str, Any]:
        """Extract structured plan from Gemini response."""
        try:
            # Try to find JSON in the response
            start = response.find("{")
            end = response.rfind("}") + 1
            if start >= 0 and end > start:
                json_str = response[start:end]
                return json.loads(json_str)
        except Exception:
            pass
        
        # Return default structure if parsing fails
        return {
            "schedule": [
                {"time": "09:00-10:30", "task": "Deep work block", "type": "deep_work", "reason": "Peak morning energy"},
                {"time": "10:30-11:00", "task": "Email & communications", "type": "admin", "reason": "After deep work"},
                {"time": "11:00-12:30", "task": "Priority tasks", "type": "deep_work", "reason": "Still high energy"},
                {"time": "12:30-13:30", "task": "Lunch break", "type": "break", "reason": "Recharge"},
                {"time": "13:30-15:00", "task": "Meetings & collaboration", "type": "meeting", "reason": "Post-lunch social energy"},
                {"time": "15:00-16:30", "task": "Administrative tasks", "type": "admin", "reason": "Afternoon wind-down"},
                {"time": "16:30-17:00", "task": "Review & planning", "type": "admin", "reason": "End of day wrap-up"}
            ],
            "key_insights": [
                "Schedule demanding tasks in the morning when energy is highest",
                "Batch similar tasks together to minimize context switching",
                "Leave buffer time between meetings for preparation"
            ],
            "deferred_tasks": [],
            "focus_theme": "Focused execution and goal progress"
        }
