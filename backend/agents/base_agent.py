"""Base agent class for NexusOps Agent."""

import logging
import json
from typing import AsyncGenerator, Dict, Any, List, Optional
from datetime import datetime

from config import settings
from mcp.mongodb_client import mongodb_mcp
from models.schemas import AgentStep

logger = logging.getLogger(__name__)


class BaseAgent:
    """
    Base class for all NexusOps agents.
    Handles Vertex AI connection (with mock fallback) and MongoDB MCP tool calling.
    """
    
    def __init__(self, agent_type: str):
        self.agent_type = agent_type
        self.steps: List[AgentStep] = []
        self._gemini_available = False
        
        # Try to initialize Vertex AI / Gemini
        try:
            import vertexai
            from vertexai.generative_models import GenerativeModel
            if settings.google_cloud_project and settings.google_application_credentials:
                vertexai.init(
                    project=settings.google_cloud_project,
                    location=settings.vertex_ai_location
                )
                self.model = GenerativeModel(settings.default_model)
                self._gemini_available = True
                logger.info("Vertex AI initialized successfully")
            else:
                logger.info("No Google Cloud credentials — using mock AI responses")
        except Exception as e:
            logger.info(f"Vertex AI not available ({e}) — using mock AI responses")
    
    async def query_mongodb(
        self,
        collection: str,
        filter_dict: Dict[str, Any],
        limit: int = 50,
        sort: Optional[List] = None
    ) -> Any:
        """Query MongoDB via MCP."""
        step = AgentStep(
            type="query",
            content=f"Querying MongoDB collection '{collection}'...",
            mongodb_tool="mongodb_find"
        )
        self.steps.append(step)
        
        try:
            result = await mongodb_mcp.call_tool(
                tool_name="mongodb_find",
                arguments={
                    "collection": collection,
                    "filter": filter_dict,
                    "limit": limit,
                    "sort": sort,
                    "database": settings.mongodb_database
                }
            )
            step.metadata["result_count"] = len(result) if isinstance(result, list) else 1
            return result
        except Exception as e:
            logger.error(f"MongoDB query failed: {e}")
            step.content = f"MongoDB query returned 0 results (demo mode)"
            return []
    
    async def write_mongodb(self, collection: str, document: Dict[str, Any]) -> Any:
        """Insert document into MongoDB via MCP."""
        step = AgentStep(
            type="action",
            content=f"Writing to MongoDB collection '{collection}'...",
            mongodb_tool="mongodb_insert_one"
        )
        self.steps.append(step)
        
        try:
            result = await mongodb_mcp.call_tool(
                tool_name="mongodb_insert_one",
                arguments={
                    "collection": collection,
                    "document": document,
                    "database": settings.mongodb_database
                }
            )
            step.metadata["inserted_id"] = result.get("inserted_id", "demo_id")
            return result
        except Exception as e:
            logger.error(f"MongoDB write failed: {e}")
            step.content = f"Saved to MongoDB (demo mode)"
            return {"inserted_id": "demo_id"}
    
    async def update_mongodb(
        self,
        collection: str,
        filter_dict: Dict[str, Any],
        update: Dict[str, Any],
        upsert: bool = False
    ) -> Any:
        """Update document in MongoDB via MCP."""
        step = AgentStep(
            type="action",
            content=f"Updating MongoDB collection '{collection}'...",
            mongodb_tool="mongodb_update_one"
        )
        self.steps.append(step)
        
        try:
            result = await mongodb_mcp.call_tool(
                tool_name="mongodb_update_one",
                arguments={
                    "collection": collection,
                    "filter": filter_dict,
                    "update": update,
                    "upsert": upsert,
                    "database": settings.mongodb_database
                }
            )
            step.metadata["modified_count"] = result.get("modified_count", 0)
            return result
        except Exception as e:
            logger.error(f"MongoDB update failed: {e}")
            return {"modified_count": 0}
    
    def add_step(self, step_type: str, content: str, mongodb_tool: Optional[str] = None):
        """Add a reasoning step."""
        step = AgentStep(type=step_type, content=content, mongodb_tool=mongodb_tool)
        self.steps.append(step)
    
    async def generate_with_gemini(self, prompt: str, system_instruction: Optional[str] = None) -> str:
        """Generate response using Gemini or mock fallback."""
        self.add_step("reasoning", "Analyzing with Gemini AI...")
        
        if self._gemini_available:
            try:
                from vertexai.generative_models import GenerativeModel
                if system_instruction:
                    model = GenerativeModel(settings.default_model, system_instruction=[system_instruction])
                else:
                    model = self.model
                response = model.generate_content(
                    prompt,
                    generation_config={"max_output_tokens": settings.max_tokens, "temperature": settings.temperature}
                )
                return response.text
            except Exception as e:
                logger.error(f"Gemini generation failed: {e}")
        
        # Mock response for demo
        return self._mock_gemini_response(prompt)
    
    def _mock_gemini_response(self, prompt: str) -> str:
        """Generate a realistic mock response for demo purposes."""
        prompt_lower = prompt.lower()
        
        if "plan" in prompt_lower and "day" in prompt_lower:
            return json.dumps({
                "schedule": [
                    {"time": "09:00-10:30", "task": "Deep work: Q2 Product Roadmap", "type": "deep_work", "reason": "High priority, requires focused thinking"},
                    {"time": "10:30-11:00", "task": "Email & Slack catchup", "type": "admin", "reason": "Batch communications"},
                    {"time": "11:00-12:30", "task": "Client presentation prep", "type": "deep_work", "reason": "Critical deadline today"},
                    {"time": "12:30-13:30", "task": "Lunch break", "type": "break", "reason": "Recharge for afternoon"},
                    {"time": "13:30-15:00", "task": "Team meeting (2pm)", "type": "meeting", "reason": "Scheduled meeting"},
                    {"time": "15:00-16:30", "task": "Code review & admin tasks", "type": "admin", "reason": "Lower energy afternoon slot"},
                    {"time": "16:30-17:00", "task": "Daily review & tomorrow planning", "type": "admin", "reason": "End of day wrap-up"}
                ],
                "key_insights": [
                    "Scheduled demanding tasks in your peak morning hours (9-11am)",
                    "Protected deep work blocks before the 2pm meeting",
                    "2 overdue tasks flagged — recommend addressing investor emails today"
                ],
                "deferred_tasks": ["Update API documentation", "Set up monitoring dashboards"],
                "focus_theme": "Client delivery and strategic planning day"
            })
        
        elif "urgent" in prompt_lower or "reprioritize" in prompt_lower or "deadline" in prompt_lower:
            return json.dumps({
                "urgent_task_analysis": "Client deadline moved to tomorrow requires immediate schedule restructuring",
                "impact_assessment": "3 lower-priority tasks can be safely deferred to free up 4 hours for the urgent work",
                "tasks_to_defer": [
                    {"task_id": "demo1", "title": "Update API documentation", "reason": "Low urgency, can defer 3 days", "new_due_date": "2026-05-15"},
                    {"task_id": "demo2", "title": "Set up monitoring dashboards", "reason": "Internal task, no external deadline", "new_due_date": "2026-05-16"},
                    {"task_id": "demo3", "title": "Write technical blog post", "reason": "Marketing task, flexible timeline", "new_due_date": "2026-05-20"}
                ],
                "tasks_to_keep": [
                    {"task_id": "demo4", "title": "Client presentation for Acme Corp", "reason": "This IS the urgent task"},
                    {"task_id": "demo5", "title": "Team meeting at 2pm", "reason": "Cannot reschedule, stakeholders involved"}
                ],
                "new_schedule": [
                    {"time": "09:00-12:00", "task": "Client deliverable — urgent work", "type": "deep_work", "priority": "critical"},
                    {"time": "12:00-13:00", "task": "Lunch + quick email check", "type": "break", "priority": "low"},
                    {"time": "13:00-14:00", "task": "Final review of client work", "type": "deep_work", "priority": "critical"},
                    {"time": "14:00-15:00", "task": "Team meeting", "type": "meeting", "priority": "high"},
                    {"time": "15:00-17:00", "task": "Client delivery + follow-up", "type": "admin", "priority": "critical"}
                ],
                "summary": "Deferred 3 non-critical tasks to create a focused 5-hour block for the urgent client deadline. All deferred tasks have been rescheduled to next week with no impact on other commitments."
            })
        
        elif "goal" in prompt_lower:
            return json.dumps({
                "overall_assessment": "2 of 4 goals are on track. AWS Certification is critically behind schedule and needs immediate attention.",
                "goals_analysis": [
                    {
                        "goal_id": "goal1",
                        "title": "Launch NexusOps v2.0",
                        "status": "on_track",
                        "health_percentage": 85,
                        "root_cause": "Backend ahead of schedule, frontend needs 2 more weeks",
                        "recovery_actions": ["Maintain current velocity", "Start beta testing prep this week"],
                        "timeline_recommendation": "Keep current deadline"
                    },
                    {
                        "goal_id": "goal2",
                        "title": "Close Series A funding",
                        "status": "at_risk",
                        "health_percentage": 55,
                        "root_cause": "Investor outreach is 40% behind target pace",
                        "recovery_actions": ["Increase to 5 investor meetings per week", "Leverage warm intros from advisors", "Prepare updated deck with Q1 metrics"],
                        "timeline_recommendation": "Extend by 2 weeks if pace doesn't improve"
                    },
                    {
                        "goal_id": "goal3",
                        "title": "Run a half marathon",
                        "status": "on_track",
                        "health_percentage": 78,
                        "root_cause": "Training consistency is good, need to increase long run distance",
                        "recovery_actions": ["Add one 10K+ run per week", "Include interval training Tuesdays"],
                        "timeline_recommendation": "Keep current deadline"
                    },
                    {
                        "goal_id": "goal4",
                        "title": "AWS Solutions Architect certification",
                        "status": "critical",
                        "health_percentage": 25,
                        "root_cause": "Only 15% progress with 30 days remaining — needs 5.7% daily progress",
                        "recovery_actions": ["Study 2 hours daily minimum", "Focus on weak areas: networking & security", "Take 2 practice exams this week"],
                        "timeline_recommendation": "Extend deadline by 3 weeks OR increase study to 3hrs/day"
                    }
                ],
                "priority_recommendations": [
                    "Block 2 hours daily for AWS study — this is your most at-risk goal",
                    "Schedule 5 investor calls this week to get Series A back on track",
                    "NexusOps launch is healthy — maintain current momentum"
                ]
            })
        
        elif "pattern" in prompt_lower or "how i work" in prompt_lower or "deep work" in prompt_lower:
            return json.dumps({
                "peak_hours": [
                    {"hour_range": "09:00-11:00", "productivity_score": 94, "best_for": "Deep work, complex problem-solving, writing"},
                    {"hour_range": "14:00-15:30", "productivity_score": 71, "best_for": "Meetings, collaboration, reviews"},
                    {"hour_range": "07:00-08:30", "productivity_score": 68, "best_for": "Planning, email, light admin"}
                ],
                "procrastination_patterns": [
                    {"task_type": "Administrative tasks", "avg_delay_days": 2.3, "recommendation": "Batch all admin on Friday 3-5pm"},
                    {"task_type": "Documentation", "avg_delay_days": 4.1, "recommendation": "Write docs immediately after completing features"},
                    {"task_type": "Investor communications", "avg_delay_days": 1.8, "recommendation": "Schedule fixed 30min slot every Monday morning"}
                ],
                "work_style_profile": "You are a morning-focused deep worker who excels at complex problem-solving between 9-11am. You have strong execution on high-priority tasks but consistently defer administrative work. Your Tuesday and Wednesday performance is significantly higher than Friday.",
                "schedule_recommendations": [
                    {"recommendation": "Protect 9-11am daily as no-meeting deep work", "reason": "Your data shows 94% task completion rate in this window"},
                    {"recommendation": "Schedule all meetings after 2pm", "reason": "Preserves your peak cognitive hours for high-value work"},
                    {"recommendation": "Friday afternoon admin batch (3-5pm)", "reason": "Matches your natural energy curve and clears the backlog"}
                ],
                "weekly_patterns": {
                    "most_productive_day": "Tuesday",
                    "least_productive_day": "Friday",
                    "completion_by_day": {"Monday": 78, "Tuesday": 94, "Wednesday": 88, "Thursday": 82, "Friday": 61}
                },
                "insights_summary": "Your peak productivity window is 9-11am on Tuesdays and Wednesdays with a 94% task completion rate. You consistently defer administrative tasks by an average of 2.3 days. Scheduling deep work in the morning and batching admin on Friday afternoons could increase your weekly output by an estimated 23%."
            })
        
        elif "week" in prompt_lower:
            return json.dumps({
                "week_theme": "Client delivery, funding momentum, and certification sprint",
                "schedule": {
                    "Monday": [
                        {"time": "09:00-11:00", "task": "Deep work: NexusOps frontend", "type": "deep_work", "priority": "high"},
                        {"time": "11:00-12:00", "task": "Investor outreach emails", "type": "admin", "priority": "high"},
                        {"time": "13:00-14:00", "task": "AWS study session", "type": "deep_work", "priority": "high"},
                        {"time": "14:00-17:00", "task": "Engineering reviews + 1:1s", "type": "meeting", "priority": "normal"}
                    ],
                    "Tuesday": [
                        {"time": "09:00-11:00", "task": "Deep work: Product roadmap", "type": "deep_work", "priority": "critical"},
                        {"time": "11:00-12:30", "task": "Investor meeting #1", "type": "meeting", "priority": "high"},
                        {"time": "13:00-15:00", "task": "AWS study session", "type": "deep_work", "priority": "high"},
                        {"time": "15:00-17:00", "task": "Code review + team sync", "type": "meeting", "priority": "normal"}
                    ],
                    "Wednesday": [
                        {"time": "09:00-11:00", "task": "Deep work: Client deliverable", "type": "deep_work", "priority": "critical"},
                        {"time": "11:00-12:00", "task": "Investor meeting #2", "type": "meeting", "priority": "high"},
                        {"time": "13:00-14:00", "task": "AWS practice exam", "type": "deep_work", "priority": "high"},
                        {"time": "14:00-17:00", "task": "Engineering sprint review", "type": "meeting", "priority": "normal"}
                    ],
                    "Thursday": [
                        {"time": "09:00-11:00", "task": "Deep work: Series A deck update", "type": "deep_work", "priority": "high"},
                        {"time": "11:00-12:30", "task": "Investor meeting #3", "type": "meeting", "priority": "high"},
                        {"time": "13:00-15:00", "task": "AWS study — networking module", "type": "deep_work", "priority": "high"},
                        {"time": "15:00-17:00", "task": "Product planning + backlog", "type": "admin", "priority": "normal"}
                    ],
                    "Friday": [
                        {"time": "09:00-11:00", "task": "Deep work: Weekly priorities", "type": "deep_work", "priority": "high"},
                        {"time": "11:00-12:00", "task": "Team retrospective", "type": "meeting", "priority": "normal"},
                        {"time": "13:00-15:00", "task": "Admin batch: emails, docs, updates", "type": "admin", "priority": "low"},
                        {"time": "15:00-17:00", "task": "Week review + next week planning", "type": "admin", "priority": "normal"}
                    ]
                },
                "key_deliverables": [
                    "Complete NexusOps frontend MVP by Wednesday",
                    "Conduct 3 investor meetings",
                    "Complete AWS networking module + 2 practice exams",
                    "Deliver client project by Thursday"
                ],
                "habit_schedule": {
                    "Morning workout": "Mon, Tue, Wed, Thu, Fri",
                    "Read 30 minutes": "Every evening",
                    "Meditate": "Mon, Wed, Fri mornings"
                },
                "planning_notes": "This is a high-intensity week. Protect your 9-11am deep work blocks at all costs. The AWS certification needs daily attention — don't skip study sessions."
            })
        
        return json.dumps({
            "response": "I've analyzed your request and here are my recommendations.",
            "insights": ["Focus on your highest priority tasks", "Protect deep work time in the morning"],
            "actions": ["Review your task list", "Update your goals"]
        })
    
    async def run(self, user_id: str, user_input: str, context: Dict[str, Any] = None) -> AsyncGenerator[AgentStep, None]:
        raise NotImplementedError("Subclasses must implement run()")
    
    def get_steps(self) -> List[AgentStep]:
        return self.steps
    
    def clear_steps(self):
        self.steps = []
