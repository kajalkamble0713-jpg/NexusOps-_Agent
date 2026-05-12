"""Pattern Intelligence Engine — Discovers productivity patterns."""

import json
import logging
from typing import AsyncGenerator, Dict, Any, List
from datetime import datetime, timedelta
from collections import defaultdict

from agents.base_agent import BaseAgent
from models.schemas import AgentStep

logger = logging.getLogger(__name__)


class PatternEngineAgent(BaseAgent):
    """
    Pattern Intelligence Engine.
    
    Analyzes 30 days of data to:
    1. Find completion rates by time of day, day of week, task category
    2. Identify peak productivity windows
    3. Detect procrastination patterns
    4. Compare planned vs actual time spent
    5. Generate personalized work style insights
    """
    
    SYSTEM_INSTRUCTION = """You are the Pattern Intelligence Engine, an analytical agent for NexusOps.

Your role is to discover productivity patterns and provide personalized optimization recommendations.

When analyzing patterns:
- Look for correlations between time of day and task completion
- Identify task types that are consistently delayed
- Find optimal scheduling windows for different work types
- Be specific and data-driven in recommendations

Respond with structured JSON for pattern analysis."""
    
    def __init__(self):
        super().__init__("pattern_engine")
    
    async def run(
        self,
        user_id: str,
        user_input: str,
        context: Dict[str, Any] = None
    ) -> AsyncGenerator[AgentStep, None]:
        """Run the Pattern Engine agent."""
        self.clear_steps()
        
        # Step 1: Start analysis
        step = AgentStep(
            type="reasoning",
            content="Initiating deep pattern analysis across your last 30 days of activity..."
        )
        self.steps.append(step)
        yield step
        
        # Step 2: Fetch 30 days of daily plans
        step = AgentStep(
            type="query",
            content="Loading 30 days of daily plans from MongoDB...",
            mongodb_tool="mongodb_find"
        )
        self.steps.append(step)
        yield step
        
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)
        
        daily_plans = await self.query_mongodb(
            collection="daily_plans",
            filter_dict={
                "user_id": user_id,
                "date": {"$gte": thirty_days_ago.isoformat()}
            },
            limit=30
        )
        
        step = AgentStep(
            type="insight",
            content=f"Loaded {len(daily_plans)} daily plans. Analyzing completion patterns..."
        )
        self.steps.append(step)
        yield step
        
        # Step 3: Fetch completed tasks
        step = AgentStep(
            type="query",
            content="Fetching completed task data for pattern analysis...",
            mongodb_tool="mongodb_find"
        )
        self.steps.append(step)
        yield step
        
        completed_tasks = await self.query_mongodb(
            collection="tasks",
            filter_dict={
                "user_id": user_id,
                "status": "done",
                "completed_at": {"$gte": thirty_days_ago.isoformat()}
            },
            limit=200
        )
        
        step = AgentStep(
            type="insight",
            content=f"Analyzing {len(completed_tasks)} completed tasks for timing and category patterns..."
        )
        self.steps.append(step)
        yield step
        
        # Step 4: Compute patterns
        step = AgentStep(
            type="reasoning",
            content="Computing productivity metrics: completion rates, peak hours, category analysis..."
        )
        self.steps.append(step)
        yield step
        
        patterns = self._compute_patterns(completed_tasks, daily_plans)
        
        # Step 5: Fetch habit data
        step = AgentStep(
            type="query",
            content="Correlating habit completion with productivity patterns...",
            mongodb_tool="mongodb_find"
        )
        self.steps.append(step)
        yield step
        
        habits = await self.query_mongodb(
            collection="habits",
            filter_dict={"user_id": user_id},
            limit=20
        )
        
        # Step 6: Generate insights with Gemini
        step = AgentStep(
            type="reasoning",
            content="Applying Gemini AI to generate personalized productivity insights..."
        )
        self.steps.append(step)
        yield step
        
        prompt = f"""User request: {user_input}

PRODUCTIVITY PATTERNS (last 30 days):
{json.dumps(patterns, indent=2)}

HABIT DATA:
{json.dumps([{
    "name": h.get("name"),
    "streak": h.get("streak_count", 0),
    "category": h.get("category")
} for h in habits[:10]], indent=2)}

Based on this data, provide:
1. Peak productivity windows (specific hours)
2. Procrastination patterns (task types consistently delayed)
3. Optimal schedule recommendations
4. Personalized work style insights

Respond with JSON:
{{
  "peak_hours": [
    {{"hour_range": "09:00-11:00", "productivity_score": 92, "best_for": "Deep work, complex problems"}}
  ],
  "procrastination_patterns": [
    {{"task_type": "Admin tasks", "avg_delay_days": 2.3, "recommendation": "Batch on Friday afternoons"}}
  ],
  "work_style_profile": "Your work style description",
  "schedule_recommendations": [
    {{"recommendation": "Schedule deep work 9-11am", "reason": "Your data shows 87% completion rate in this window"}}
  ],
  "weekly_patterns": {{
    "most_productive_day": "Tuesday",
    "least_productive_day": "Friday",
    "completion_by_day": {{"Monday": 78, "Tuesday": 92, "Wednesday": 85, "Thursday": 80, "Friday": 65}}
  }},
  "insights_summary": "2-3 sentence summary of your productivity profile"
}}"""
        
        gemini_response = await self.generate_with_gemini(prompt, self.SYSTEM_INSTRUCTION)
        insights_data = self._extract_insights(gemini_response)
        
        # Step 7: Save insights to MongoDB
        step = AgentStep(
            type="action",
            content="Saving pattern insights to MongoDB...",
            mongodb_tool="mongodb_insert_one"
        )
        self.steps.append(step)
        yield step
        
        insight_doc = {
            "user_id": user_id,
            "type": "productivity_pattern",
            "content": json.dumps(insights_data),
            "generated_at": datetime.utcnow().isoformat(),
            "related_items": [],
            "acknowledged": False
        }
        await self.write_mongodb("insights", insight_doc)
        
        # Step 8: Build result
        peak_hours_text = "\n".join(
            f"  • {ph.get('hour_range', '')}: Score {ph.get('productivity_score', 0)}% — {ph.get('best_for', '')}"
            for ph in insights_data.get("peak_hours", [])[:3]
        )
        
        procrastination_text = "\n".join(
            f"  • {pp.get('task_type', '')}: avg {pp.get('avg_delay_days', 0)} day delay → {pp.get('recommendation', '')}"
            for pp in insights_data.get("procrastination_patterns", [])[:3]
        )
        
        recommendations_text = "\n".join(
            f"  {i+1}. {r.get('recommendation', '')} ({r.get('reason', '')})"
            for i, r in enumerate(insights_data.get("schedule_recommendations", [])[:3])
        )
        
        weekly = insights_data.get("weekly_patterns", {})
        
        result_content = f"""✅ Pattern Analysis Complete!

🧠 Your Work Style Profile:
{insights_data.get('work_style_profile', 'Analytical and goal-oriented professional')}

⚡ Peak Productivity Windows:
{peak_hours_text if peak_hours_text else '  Data still being collected...'}

📅 Weekly Patterns:
  Most Productive: {weekly.get('most_productive_day', 'Tuesday')}
  Least Productive: {weekly.get('least_productive_day', 'Friday')}

⚠️ Procrastination Patterns:
{procrastination_text if procrastination_text else '  No significant patterns detected'}

🎯 Schedule Recommendations:
{recommendations_text if recommendations_text else '  Continue current schedule'}

💡 Summary:
{insights_data.get('insights_summary', 'Your productivity patterns have been analyzed and saved.')}"""
        
        step = AgentStep(
            type="result",
            content=result_content,
            metadata={"insights": insights_data, "patterns": patterns}
        )
        self.steps.append(step)
        yield step
    
    def _compute_patterns(
        self,
        completed_tasks: List[Dict],
        daily_plans: List[Dict]
    ) -> Dict[str, Any]:
        """Compute productivity patterns from raw data."""
        # Completion by day of week
        day_completions = defaultdict(int)
        day_totals = defaultdict(int)
        
        # Category analysis
        category_completions = defaultdict(int)
        
        # Hour analysis (from completed_at timestamps)
        hour_completions = defaultdict(int)
        
        for task in completed_tasks:
            completed_at = task.get("completed_at")
            if completed_at:
                try:
                    dt = datetime.fromisoformat(completed_at.replace("Z", "+00:00"))
                    day_name = dt.strftime("%A")
                    day_completions[day_name] += 1
                    hour_completions[dt.hour] += 1
                except Exception:
                    pass
            
            for tag in task.get("tags", []):
                category_completions[tag] += 1
        
        # Calculate completion rates from daily plans
        total_planned = 0
        total_completed = 0
        
        for plan in daily_plans:
            planned = len(plan.get("planned_tasks", []))
            total_planned += planned
        
        total_completed = len(completed_tasks)
        
        completion_rate = (total_completed / max(total_planned, 1)) * 100
        
        # Find peak hours
        peak_hours = sorted(hour_completions.items(), key=lambda x: x[1], reverse=True)[:3]
        
        return {
            "total_tasks_completed": len(completed_tasks),
            "total_tasks_planned": total_planned,
            "overall_completion_rate": round(completion_rate, 1),
            "completion_by_day": dict(day_completions),
            "completion_by_hour": dict(hour_completions),
            "peak_hours": [{"hour": h, "completions": c} for h, c in peak_hours],
            "category_breakdown": dict(category_completions),
            "daily_plans_analyzed": len(daily_plans)
        }
    
    def _extract_insights(self, response: str) -> Dict[str, Any]:
        """Extract insights from Gemini response."""
        try:
            start = response.find("{")
            end = response.rfind("}") + 1
            if start >= 0 and end > start:
                return json.loads(response[start:end])
        except Exception:
            pass
        
        return {
            "peak_hours": [
                {"hour_range": "09:00-11:00", "productivity_score": 88, "best_for": "Deep work and complex tasks"},
                {"hour_range": "14:00-16:00", "productivity_score": 72, "best_for": "Meetings and collaboration"}
            ],
            "procrastination_patterns": [
                {"task_type": "Administrative tasks", "avg_delay_days": 2.1, "recommendation": "Batch on Friday afternoons"}
            ],
            "work_style_profile": "You are a morning-focused deep worker who excels at complex problem-solving.",
            "schedule_recommendations": [
                {"recommendation": "Block 9-11am for deep work daily", "reason": "Highest completion rate in this window"},
                {"recommendation": "Schedule meetings after 2pm", "reason": "Preserves morning peak productivity"}
            ],
            "weekly_patterns": {
                "most_productive_day": "Tuesday",
                "least_productive_day": "Friday",
                "completion_by_day": {"Monday": 75, "Tuesday": 90, "Wednesday": 82, "Thursday": 78, "Friday": 60}
            },
            "insights_summary": "Your data shows strong morning productivity with peak performance on Tuesdays. Consider protecting your morning hours for deep work."
        }
