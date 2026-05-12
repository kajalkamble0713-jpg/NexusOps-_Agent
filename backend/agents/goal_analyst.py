"""Goal Health Analyst Agent — Tracks goal progress and suggests recovery actions."""

import json
import logging
from typing import AsyncGenerator, Dict, Any
from datetime import datetime, timedelta

from agents.base_agent import BaseAgent
from models.schemas import AgentStep

logger = logging.getLogger(__name__)


class GoalAnalystAgent(BaseAgent):
    """
    Goal Health Analyst Agent.
    
    Analyzes goal health by:
    1. Fetching all active goals and milestone status
    2. Calculating trajectory (current pace vs required pace)
    3. Identifying at-risk goals (yellow/red status)
    4. Querying recent tasks tagged to each goal
    5. Generating specific, actionable recovery suggestions
    6. Writing insights back to MongoDB
    """
    
    SYSTEM_INSTRUCTION = """You are the Goal Health Analyst, an intelligent goal tracking agent for NexusOps.

Your role is to analyze goal progress and provide actionable recovery suggestions.

When analyzing goals:
- Calculate current pace vs required pace to hit deadlines
- Identify root causes of delays
- Provide specific, actionable recovery steps
- Be honest about at-risk goals
- Suggest realistic adjustments

Respond with structured JSON for goal analysis."""
    
    def __init__(self):
        super().__init__("goal_analyst")
    
    async def run(
        self,
        user_id: str,
        user_input: str,
        context: Dict[str, Any] = None
    ) -> AsyncGenerator[AgentStep, None]:
        """Run the Goal Analyst agent."""
        self.clear_steps()
        
        # Step 1: Start analysis
        step = AgentStep(
            type="reasoning",
            content="Starting comprehensive goal health analysis..."
        )
        self.steps.append(step)
        yield step
        
        # Step 2: Fetch all active goals
        step = AgentStep(
            type="query",
            content="Fetching all active goals and milestone data from MongoDB...",
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
            limit=20
        )
        
        step = AgentStep(
            type="insight",
            content=f"Found {len(goals)} active goals. Calculating progress trajectories..."
        )
        self.steps.append(step)
        yield step
        
        # Step 3: Calculate goal health for each
        goal_health = []
        now = datetime.utcnow()
        
        for goal in goals:
            target_date = goal.get("target_date")
            if not target_date:
                continue
            
            try:
                target = datetime.fromisoformat(target_date.replace("Z", "+00:00"))
                days_remaining = (target - now).days
                current_progress = goal.get("current_progress", 0)
                
                # Calculate required pace
                if days_remaining > 0:
                    required_daily_pace = (100 - current_progress) / days_remaining
                else:
                    required_daily_pace = 100  # Overdue
                
                # Determine health status
                if current_progress >= 90:
                    status = "on_track"
                    color = "green"
                elif days_remaining < 0:
                    status = "overdue"
                    color = "red"
                elif required_daily_pace > 5:  # More than 5% per day needed
                    status = "critical"
                    color = "red"
                elif required_daily_pace > 2:
                    status = "at_risk"
                    color = "yellow"
                else:
                    status = "on_track"
                    color = "green"
                
                goal_health.append({
                    "id": str(goal.get("_id", "")),
                    "title": goal.get("title", ""),
                    "category": goal.get("category", ""),
                    "current_progress": current_progress,
                    "target_date": target_date,
                    "days_remaining": days_remaining,
                    "required_daily_pace": round(required_daily_pace, 2),
                    "status": status,
                    "color": color,
                    "milestones": goal.get("milestones", [])
                })
            except Exception as e:
                logger.error(f"Error calculating goal health: {e}")
        
        # Step 4: Identify at-risk goals
        at_risk = [g for g in goal_health if g["status"] in ("at_risk", "critical", "overdue")]
        
        if at_risk:
            step = AgentStep(
                type="insight",
                content=f"⚠️ Identified {len(at_risk)} goal(s) requiring attention!"
            )
            self.steps.append(step)
            yield step
        
        # Step 5: Query recent tasks for goal context
        step = AgentStep(
            type="query",
            content="Analyzing recent task activity related to your goals...",
            mongodb_tool="mongodb_find"
        )
        self.steps.append(step)
        yield step
        
        thirty_days_ago = now - timedelta(days=30)
        recent_tasks = await self.query_mongodb(
            collection="tasks",
            filter_dict={
                "user_id": user_id,
                "created_at": {"$gte": thirty_days_ago.isoformat()}
            },
            limit=100
        )
        
        # Step 6: Generate recovery suggestions with Gemini
        step = AgentStep(
            type="reasoning",
            content="Applying Gemini AI to generate personalized recovery strategies..."
        )
        self.steps.append(step)
        yield step
        
        goals_summary = json.dumps(goal_health, indent=2)
        tasks_summary = json.dumps([{
            "title": t.get("title"),
            "status": t.get("status"),
            "tags": t.get("tags", []),
            "completed_at": t.get("completed_at")
        } for t in recent_tasks[:20]], indent=2)
        
        prompt = f"""User request: {user_input}

GOAL HEALTH DATA:
{goals_summary}

RECENT TASK ACTIVITY:
{tasks_summary}

Analyze each goal and provide:
1. Root cause analysis for at-risk goals
2. Specific, actionable recovery steps
3. Realistic timeline adjustments if needed

Respond with JSON:
{{
  "overall_assessment": "Brief summary of goal health",
  "goals_analysis": [
    {{
      "goal_id": "id",
      "title": "title",
      "status": "on_track|at_risk|critical|overdue",
      "health_percentage": 85,
      "root_cause": "Why behind/ahead",
      "recovery_actions": ["action1", "action2"],
      "timeline_recommendation": "Keep current deadline | Extend by X weeks"
    }}
  ],
  "priority_recommendations": ["Top 3 actions to take this week"]
}}"""
        
        gemini_response = await self.generate_with_gemini(prompt, self.SYSTEM_INSTRUCTION)
        analysis_data = self._extract_analysis(gemini_response)
        
        # Step 7: Write insights to MongoDB
        step = AgentStep(
            type="action",
            content="Saving goal insights to MongoDB...",
            mongodb_tool="mongodb_insert_one"
        )
        self.steps.append(step)
        yield step
        
        for goal_analysis in analysis_data.get("goals_analysis", []):
            insight_doc = {
                "user_id": user_id,
                "type": "goal_health",
                "content": json.dumps(goal_analysis),
                "generated_at": now.isoformat(),
                "related_items": [goal_analysis.get("goal_id")],
                "acknowledged": False
            }
            await self.write_mongodb("insights", insight_doc)
        
        # Step 8: Update goals with AI suggestions
        step = AgentStep(
            type="action",
            content="Updating goals with AI-generated suggestions...",
            mongodb_tool="mongodb_update_one"
        )
        self.steps.append(step)
        yield step
        
        for goal_analysis in analysis_data.get("goals_analysis", []):
            goal_id = goal_analysis.get("goal_id")
            if goal_id:
                await self.update_mongodb(
                    collection="goals",
                    filter_dict={"_id": goal_id},
                    update={
                        "$set": {
                            "ai_suggestions": goal_analysis.get("recovery_actions", []),
                            "insights": [goal_analysis.get("root_cause", "")]
                        }
                    }
                )
        
        # Step 9: Build result
        goals_breakdown = ""
        for ga in analysis_data.get("goals_analysis", [])[:5]:
            status_emoji = {"on_track": "✅", "at_risk": "⚠️", "critical": "🚨", "overdue": "❌"}.get(ga.get("status", ""), "📊")
            goals_breakdown += f"\n{status_emoji} {ga.get('title', 'Goal')} ({ga.get('health_percentage', 0)}%)\n"
            goals_breakdown += f"   Root Cause: {ga.get('root_cause', 'N/A')}\n"
            goals_breakdown += f"   Actions: {', '.join(ga.get('recovery_actions', [])[:2])}\n"
        
        priority_actions = "\n".join(
            f"  {i+1}. {action}"
            for i, action in enumerate(analysis_data.get("priority_recommendations", [])[:3])
        )
        
        result_content = f"""✅ Goal Health Analysis Complete!

📊 Overall Assessment:
{analysis_data.get('overall_assessment', 'Your goals are being tracked and analyzed.')}

🎯 Goal Breakdown:{goals_breakdown}

🚀 Priority Actions This Week:
{priority_actions if priority_actions else '  Continue current momentum!'}

All insights have been saved to MongoDB."""
        
        step = AgentStep(
            type="result",
            content=result_content,
            metadata={"analysis": analysis_data, "goal_health": goal_health}
        )
        self.steps.append(step)
        yield step
    
    def _extract_analysis(self, response: str) -> Dict[str, Any]:
        """Extract analysis data from Gemini response."""
        try:
            start = response.find("{")
            end = response.rfind("}") + 1
            if start >= 0 and end > start:
                return json.loads(response[start:end])
        except Exception:
            pass
        
        return {
            "overall_assessment": "Goals are being tracked. Continue making progress.",
            "goals_analysis": [],
            "priority_recommendations": [
                "Focus on your highest-priority goal this week",
                "Break down large milestones into smaller tasks",
                "Review progress daily to stay on track"
            ]
        }
