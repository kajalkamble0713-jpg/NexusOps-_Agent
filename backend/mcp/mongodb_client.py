"""
MongoDB MCP Client — with in-memory fallback for demo mode.
Falls back gracefully when MongoDB is not available.
"""

import json
import logging
from typing import Any, Dict, List, Optional
from datetime import datetime
from bson import ObjectId

from config import settings

logger = logging.getLogger(__name__)

# ─── In-memory demo store ────────────────────────────────────────────────────

_DEMO_USER_ID = "507f1f77bcf86cd799439011"

_STORE: Dict[str, List[Dict]] = {
    "users": [
        {
            "_id": _DEMO_USER_ID,
            "name": "Alex Chen",
            "email": "demo@nexusops.ai",
            "preferences": {
                "theme": "dark",
                "notifications_enabled": True,
                "work_hours_start": 9,
                "work_hours_end": 17,
                "deep_work_duration": 90
            },
            "timezone": "America/New_York",
            "created_at": "2026-01-01T00:00:00"
        }
    ],
    "tasks": [
        {
            "_id": "task001", "user_id": _DEMO_USER_ID,
            "title": "Finalize Q2 product roadmap",
            "description": "Review and finalize the product roadmap for Q2 with stakeholder input",
            "priority": "critical", "status": "in_progress",
            "estimated_minutes": 120, "tags": ["product", "strategy"],
            "ai_score": 95, "due_date": "2026-05-13T17:00:00",
            "created_at": "2026-05-01T09:00:00", "metadata": {}
        },
        {
            "_id": "task002", "user_id": _DEMO_USER_ID,
            "title": "Client presentation for Acme Corp",
            "description": "Prepare and deliver the quarterly review presentation",
            "priority": "critical", "status": "today",
            "estimated_minutes": 90, "tags": ["client", "presentation"],
            "ai_score": 92, "due_date": "2026-05-12T14:00:00",
            "created_at": "2026-05-05T09:00:00", "metadata": {}
        },
        {
            "_id": "task003", "user_id": _DEMO_USER_ID,
            "title": "Code review: authentication module",
            "description": "Review PR #247 for the new OAuth implementation",
            "priority": "high", "status": "today",
            "estimated_minutes": 45, "tags": ["engineering", "security"],
            "ai_score": 78, "due_date": "2026-05-13T12:00:00",
            "created_at": "2026-05-08T09:00:00", "metadata": {}
        },
        {
            "_id": "task004", "user_id": _DEMO_USER_ID,
            "title": "Write technical blog post",
            "description": "Draft blog post about our microservices migration journey",
            "priority": "normal", "status": "backlog",
            "estimated_minutes": 180, "tags": ["writing", "marketing"],
            "ai_score": 45, "due_date": "2026-05-19T17:00:00",
            "created_at": "2026-05-02T09:00:00", "metadata": {}
        },
        {
            "_id": "task005", "user_id": _DEMO_USER_ID,
            "title": "Update team OKRs in Notion",
            "description": "Sync Q2 OKRs with the latest progress updates",
            "priority": "high", "status": "backlog",
            "estimated_minutes": 30, "tags": ["admin", "planning"],
            "ai_score": 65, "due_date": "2026-05-14T17:00:00",
            "created_at": "2026-05-03T09:00:00", "metadata": {}
        },
        {
            "_id": "task006", "user_id": _DEMO_USER_ID,
            "title": "Interview candidate for senior engineer role",
            "description": "Technical interview with Sarah Johnson",
            "priority": "high", "status": "today",
            "estimated_minutes": 60, "tags": ["hiring", "engineering"],
            "ai_score": 80, "due_date": "2026-05-12T15:00:00",
            "created_at": "2026-05-06T09:00:00", "metadata": {}
        },
        {
            "_id": "task007", "user_id": _DEMO_USER_ID,
            "title": "Review and respond to investor emails",
            "description": "Respond to Series A investor inquiries",
            "priority": "high", "status": "backlog",
            "estimated_minutes": 45, "tags": ["fundraising", "admin"],
            "ai_score": 70, "due_date": "2026-05-10T17:00:00",
            "created_at": "2026-05-04T09:00:00", "metadata": {}
        },
        {
            "_id": "task008", "user_id": _DEMO_USER_ID,
            "title": "Set up monitoring dashboards",
            "description": "Configure Datadog dashboards for production services",
            "priority": "normal", "status": "backlog",
            "estimated_minutes": 120, "tags": ["engineering", "devops"],
            "ai_score": 55, "due_date": "2026-05-17T17:00:00",
            "created_at": "2026-05-07T09:00:00", "metadata": {}
        },
        {
            "_id": "task009", "user_id": _DEMO_USER_ID,
            "title": "Quarterly team retrospective",
            "description": "Facilitate Q1 retrospective with the engineering team",
            "priority": "normal", "status": "backlog",
            "estimated_minutes": 90, "tags": ["team", "process"],
            "ai_score": 50, "due_date": "2026-05-09T17:00:00",
            "created_at": "2026-05-01T09:00:00", "metadata": {}
        },
        {
            "_id": "task010", "user_id": _DEMO_USER_ID,
            "title": "Analyze user churn data",
            "description": "Deep dive into March churn metrics and identify patterns",
            "priority": "high", "status": "in_progress",
            "estimated_minutes": 90, "tags": ["analytics", "product"],
            "ai_score": 82, "due_date": "2026-05-13T17:00:00",
            "created_at": "2026-05-09T09:00:00", "metadata": {}
        },
        {
            "_id": "task011", "user_id": _DEMO_USER_ID,
            "title": "1:1 with direct reports",
            "description": "Weekly 1:1 meetings with team leads",
            "priority": "high", "status": "today",
            "estimated_minutes": 120, "tags": ["management", "team"],
            "ai_score": 75, "due_date": "2026-05-12T16:00:00",
            "created_at": "2026-05-10T09:00:00", "metadata": {}
        },
        {
            "_id": "task012", "user_id": _DEMO_USER_ID,
            "title": "Launch v2.3 release",
            "priority": "critical", "status": "done",
            "estimated_minutes": 180, "tags": ["engineering", "release"],
            "ai_score": 98, "completed_at": "2026-05-10T10:00:00",
            "created_at": "2026-05-08T09:00:00", "metadata": {}
        },
        {
            "_id": "task013", "user_id": _DEMO_USER_ID,
            "title": "Investor pitch deck v3",
            "priority": "critical", "status": "done",
            "estimated_minutes": 240, "tags": ["fundraising", "strategy"],
            "ai_score": 96, "completed_at": "2026-05-07T09:00:00",
            "created_at": "2026-05-05T09:00:00", "metadata": {}
        },
        {
            "_id": "task014", "user_id": _DEMO_USER_ID,
            "title": "Update API documentation",
            "priority": "low", "status": "backlog",
            "estimated_minutes": 60, "tags": ["documentation", "engineering"],
            "ai_score": 30, "due_date": "2026-05-22T17:00:00",
            "created_at": "2026-05-01T09:00:00", "metadata": {}
        },
    ],
    "goals": [
        {
            "_id": "goal001", "user_id": _DEMO_USER_ID,
            "title": "Launch NexusOps v2.0",
            "category": "career",
            "target_date": "2026-06-26T17:00:00",
            "current_progress": 68,
            "weekly_target": 5,
            "milestones": [
                {"title": "Complete backend API", "target_date": "2026-05-02T17:00:00", "completed": True},
                {"title": "Frontend MVP", "target_date": "2026-05-19T17:00:00", "completed": False},
                {"title": "Beta testing", "target_date": "2026-06-02T17:00:00", "completed": False},
                {"title": "Public launch", "target_date": "2026-06-26T17:00:00", "completed": False}
            ],
            "insights": ["Backend is ahead of schedule", "Frontend needs acceleration"],
            "ai_suggestions": ["Allocate 3 extra hours per week to frontend", "Consider hiring a contractor for UI work"],
            "created_at": "2026-02-01T09:00:00"
        },
        {
            "_id": "goal002", "user_id": _DEMO_USER_ID,
            "title": "Close Series A funding round",
            "category": "financial",
            "target_date": "2026-07-11T17:00:00",
            "current_progress": 35,
            "weekly_target": 3,
            "milestones": [
                {"title": "Finalize pitch deck", "target_date": "2026-05-07T17:00:00", "completed": True},
                {"title": "First 10 investor meetings", "target_date": "2026-05-26T17:00:00", "completed": False},
                {"title": "Term sheet received", "target_date": "2026-06-26T17:00:00", "completed": False},
                {"title": "Round closed", "target_date": "2026-07-11T17:00:00", "completed": False}
            ],
            "insights": ["Investor outreach is behind schedule"],
            "ai_suggestions": ["Increase investor outreach to 5 meetings per week", "Leverage warm introductions from advisors"],
            "created_at": "2026-02-15T09:00:00"
        },
        {
            "_id": "goal003", "user_id": _DEMO_USER_ID,
            "title": "Run a half marathon",
            "category": "health",
            "target_date": "2026-08-10T09:00:00",
            "current_progress": 42,
            "weekly_target": 4,
            "milestones": [
                {"title": "Run 5K without stopping", "target_date": "2026-04-22T09:00:00", "completed": True},
                {"title": "Complete 10K run", "target_date": "2026-05-27T09:00:00", "completed": False},
                {"title": "15K training run", "target_date": "2026-06-26T09:00:00", "completed": False},
                {"title": "Half marathon race day", "target_date": "2026-08-10T09:00:00", "completed": False}
            ],
            "insights": ["Training consistency is good", "Need to increase long run distance"],
            "ai_suggestions": ["Add one long run per week (10K+)", "Include interval training on Tuesdays"],
            "created_at": "2026-02-01T09:00:00"
        },
        {
            "_id": "goal004", "user_id": _DEMO_USER_ID,
            "title": "Complete AWS Solutions Architect certification",
            "category": "learning",
            "target_date": "2026-06-11T17:00:00",
            "current_progress": 15,
            "weekly_target": 8,
            "milestones": [
                {"title": "Complete study materials", "target_date": "2026-05-26T17:00:00", "completed": False},
                {"title": "Practice exams (score 80%+)", "target_date": "2026-06-06T17:00:00", "completed": False},
                {"title": "Pass certification exam", "target_date": "2026-06-11T17:00:00", "completed": False}
            ],
            "insights": ["At current pace, will miss deadline by 2 weeks"],
            "ai_suggestions": ["Study 2 hours daily instead of 1", "Focus on weak areas: networking and security"],
            "created_at": "2026-04-01T09:00:00"
        }
    ],
    "habits": [
        {
            "_id": "habit001", "user_id": _DEMO_USER_ID,
            "name": "Morning workout",
            "frequency": "daily", "category": "health",
            "streak_count": 12, "best_streak": 21,
            "completion_log": [
                f"2026-05-{str(12-i).zfill(2)}T07:00:00" for i in range(12)
            ],
            "reminder_time": "07:00", "created_at": "2026-01-01T00:00:00"
        },
        {
            "_id": "habit002", "user_id": _DEMO_USER_ID,
            "name": "Read for 30 minutes",
            "frequency": "daily", "category": "learning",
            "streak_count": 5, "best_streak": 14,
            "completion_log": [
                f"2026-05-{str(12-i).zfill(2)}T21:00:00" for i in range(5)
            ],
            "reminder_time": "21:00", "created_at": "2026-01-15T00:00:00"
        },
        {
            "_id": "habit003", "user_id": _DEMO_USER_ID,
            "name": "Meditate",
            "frequency": "daily", "category": "wellness",
            "streak_count": 3, "best_streak": 30,
            "completion_log": [
                f"2026-05-{str(12-i).zfill(2)}T07:30:00" for i in range(3)
            ],
            "reminder_time": "07:30", "created_at": "2026-01-01T00:00:00"
        },
        {
            "_id": "habit004", "user_id": _DEMO_USER_ID,
            "name": "Weekly team standup notes",
            "frequency": "weekly", "category": "productivity",
            "streak_count": 8, "best_streak": 12,
            "completion_log": [],
            "reminder_time": "09:00", "created_at": "2026-01-01T00:00:00"
        },
        {
            "_id": "habit005", "user_id": _DEMO_USER_ID,
            "name": "Evening journal",
            "frequency": "daily", "category": "wellness",
            "streak_count": 7, "best_streak": 15,
            "completion_log": [
                f"2026-05-{str(12-i).zfill(2)}T22:00:00" for i in range(7)
            ],
            "reminder_time": "22:00", "created_at": "2026-01-01T00:00:00"
        }
    ],
    "daily_plans": [
        {
            "_id": "plan001", "user_id": _DEMO_USER_ID,
            "date": "2026-05-12T00:00:00",
            "planned_tasks": ["task001", "task002", "task003", "task006", "task011"],
            "actual_schedule": [
                {"time": "09:00-10:30", "task": "Deep work: Q2 Product Roadmap", "type": "deep_work"},
                {"time": "10:30-11:00", "task": "Email & Slack catchup", "type": "admin"},
                {"time": "11:00-12:30", "task": "Client presentation prep", "type": "deep_work"},
                {"time": "12:30-13:30", "task": "Lunch break", "type": "break"},
                {"time": "13:30-15:00", "task": "Team meeting (2pm)", "type": "meeting"},
                {"time": "15:00-16:00", "task": "Interview: Senior Engineer candidate", "type": "meeting"},
                {"time": "16:00-17:00", "task": "1:1 with direct reports", "type": "meeting"}
            ],
            "morning_brief": "Today's focus: Client delivery and strategic planning. 2 critical tasks due today.",
            "agent_insights": [
                "Scheduled demanding tasks in your peak morning hours (9-11am)",
                "2 overdue tasks flagged — recommend addressing investor emails today"
            ],
            "mood": "energized",
            "created_at": "2026-05-12T08:00:00"
        }
    ],
    "insights": [
        {
            "_id": "insight001", "user_id": _DEMO_USER_ID,
            "type": "productivity_pattern",
            "content": "Your peak productivity window is 9-11am on Tuesdays and Wednesdays. Schedule your most demanding tasks during this time.",
            "generated_at": "2026-05-09T08:00:00",
            "related_items": [],
            "acknowledged": False
        },
        {
            "_id": "insight002", "user_id": _DEMO_USER_ID,
            "type": "goal_health",
            "content": "⚠️ AWS Certification goal is at risk. At current pace, you'll miss the deadline by 2 weeks. Consider increasing daily study time to 2 hours.",
            "generated_at": "2026-05-11T08:00:00",
            "related_items": ["goal004"],
            "acknowledged": False
        },
        {
            "_id": "insight003", "user_id": _DEMO_USER_ID,
            "type": "pattern",
            "content": "You consistently defer administrative tasks by an average of 2.3 days. Consider batching them on Friday afternoons to protect your deep work time.",
            "generated_at": "2026-05-05T08:00:00",
            "related_items": [],
            "acknowledged": True
        },
        {
            "_id": "insight004", "user_id": _DEMO_USER_ID,
            "type": "achievement",
            "content": "🎉 12-day workout streak! Your morning exercise habit is positively correlated with higher task completion rates (+23%).",
            "generated_at": "2026-05-12T07:00:00",
            "related_items": ["habit001"],
            "acknowledged": False
        }
    ],
    "agent_sessions": []
}

_ID_COUNTER = 1000


def _new_id() -> str:
    global _ID_COUNTER
    _ID_COUNTER += 1
    return f"demo_{_ID_COUNTER}"


class MongoDBMCPClient:
    """
    MongoDB MCP Client with in-memory fallback for demo mode.
    Tries real MongoDB first, falls back to in-memory store.
    """
    
    def __init__(self):
        self.mcp_url = settings.mongodb_mcp_url
        self.mongodb_uri = settings.mongodb_uri
        self.database_name = settings.mongodb_database
        self._motor_client = None
        self._use_memory = True  # Default to memory store
    
    async def initialize(self):
        """Try to connect to MongoDB, fall back to in-memory."""
        try:
            from motor.motor_asyncio import AsyncIOMotorClient
            client = AsyncIOMotorClient(
                self.mongodb_uri,
                serverSelectionTimeoutMS=3000
            )
            # Test connection
            await client.admin.command('ping')
            self._motor_client = client
            self._use_memory = False
            logger.info("✅ Connected to MongoDB")
        except Exception as e:
            logger.info(f"MongoDB not available ({e}) — using in-memory demo store")
            self._use_memory = True
    
    async def call_tool(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """Route to real MongoDB or in-memory store."""
        if not self._use_memory and self._motor_client:
            try:
                return await self._call_motor(tool_name, arguments)
            except Exception as e:
                logger.warning(f"MongoDB call failed, using memory: {e}")
        
        return self._call_memory(tool_name, arguments)
    
    def _call_memory(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """Execute against in-memory store."""
        collection_name = arguments.get("collection", "")
        collection = _STORE.get(collection_name, [])
        
        if tool_name == "mongodb_find":
            filter_dict = arguments.get("filter", {})
            limit = arguments.get("limit", 50)
            results = [doc for doc in collection if self._matches(doc, filter_dict)]
            return results[:limit]
        
        elif tool_name == "mongodb_find_one":
            filter_dict = arguments.get("filter", {})
            for doc in collection:
                if self._matches(doc, filter_dict):
                    return doc
            return None
        
        elif tool_name == "mongodb_insert_one":
            document = arguments.get("document", {}).copy()
            if "_id" not in document:
                document["_id"] = _new_id()
            if collection_name not in _STORE:
                _STORE[collection_name] = []
            _STORE[collection_name].append(document)
            return {"inserted_id": document["_id"]}
        
        elif tool_name == "mongodb_insert_many":
            documents = arguments.get("documents", [])
            ids = []
            if collection_name not in _STORE:
                _STORE[collection_name] = []
            for doc in documents:
                doc = doc.copy()
                if "_id" not in doc:
                    doc["_id"] = _new_id()
                _STORE[collection_name].append(doc)
                ids.append(doc["_id"])
            return {"inserted_ids": ids}
        
        elif tool_name == "mongodb_update_one":
            filter_dict = arguments.get("filter", {})
            update = arguments.get("update", {})
            for i, doc in enumerate(collection):
                if self._matches(doc, filter_dict):
                    if "$set" in update:
                        collection[i].update(update["$set"])
                    if "$push" in update:
                        for k, v in update["$push"].items():
                            if k not in collection[i]:
                                collection[i][k] = []
                            collection[i][k].append(v)
                    return {"matched_count": 1, "modified_count": 1}
            return {"matched_count": 0, "modified_count": 0}
        
        elif tool_name == "mongodb_delete_one":
            filter_dict = arguments.get("filter", {})
            for i, doc in enumerate(collection):
                if self._matches(doc, filter_dict):
                    collection.pop(i)
                    return {"deleted_count": 1}
            return {"deleted_count": 0}
        
        elif tool_name == "mongodb_count":
            filter_dict = arguments.get("filter", {})
            count = sum(1 for doc in collection if self._matches(doc, filter_dict))
            return {"count": count}
        
        elif tool_name == "mongodb_aggregate":
            return collection[:50]
        
        return []
    
    def _matches(self, doc: Dict, filter_dict: Dict) -> bool:
        """Simple filter matching for in-memory store."""
        for key, value in filter_dict.items():
            if key == "$or":
                if not any(self._matches(doc, sub) for sub in value):
                    return False
            elif key == "$and":
                if not all(self._matches(doc, sub) for sub in value):
                    return False
            elif isinstance(value, dict):
                doc_val = doc.get(key)
                for op, op_val in value.items():
                    if op == "$in":
                        if doc_val not in op_val:
                            return False
                    elif op == "$nin":
                        if doc_val in op_val:
                            return False
                    elif op == "$lt":
                        if doc_val is None or str(doc_val) >= str(op_val):
                            return False
                    elif op == "$lte":
                        if doc_val is None or str(doc_val) > str(op_val):
                            return False
                    elif op == "$gt":
                        if doc_val is None or str(doc_val) <= str(op_val):
                            return False
                    elif op == "$gte":
                        if doc_val is None or str(doc_val) < str(op_val):
                            return False
                    elif op == "$ne":
                        if doc_val == op_val:
                            return False
            else:
                if doc.get(key) != value:
                    return False
        return True
    
    async def _call_motor(self, tool_name: str, arguments: Dict[str, Any]) -> Any:
        """Execute against real MongoDB via Motor."""
        db = self._motor_client[arguments.get("database", self.database_name)]
        collection = db[arguments.get("collection", "")]
        
        if tool_name == "mongodb_find":
            filter_dict = self._convert_ids(arguments.get("filter", {}))
            limit = arguments.get("limit", 50)
            cursor = collection.find(filter_dict).limit(limit)
            docs = await cursor.to_list(length=limit)
            return self._serialize(docs)
        
        elif tool_name == "mongodb_find_one":
            filter_dict = self._convert_ids(arguments.get("filter", {}))
            doc = await collection.find_one(filter_dict)
            return self._serialize(doc)
        
        elif tool_name == "mongodb_insert_one":
            document = arguments.get("document", {})
            result = await collection.insert_one(document)
            return {"inserted_id": str(result.inserted_id)}
        
        elif tool_name == "mongodb_update_one":
            filter_dict = self._convert_ids(arguments.get("filter", {}))
            update = arguments.get("update", {})
            result = await collection.update_one(filter_dict, update, upsert=arguments.get("upsert", False))
            return {"matched_count": result.matched_count, "modified_count": result.modified_count}
        
        elif tool_name == "mongodb_delete_one":
            filter_dict = self._convert_ids(arguments.get("filter", {}))
            result = await collection.delete_one(filter_dict)
            return {"deleted_count": result.deleted_count}
        
        elif tool_name == "mongodb_count":
            filter_dict = self._convert_ids(arguments.get("filter", {}))
            count = await collection.count_documents(filter_dict)
            return {"count": count}
        
        return []
    
    def _serialize(self, obj: Any) -> Any:
        if isinstance(obj, dict):
            return {k: self._serialize(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self._serialize(i) for i in obj]
        elif isinstance(obj, ObjectId):
            return str(obj)
        elif isinstance(obj, datetime):
            return obj.isoformat()
        return obj
    
    def _convert_ids(self, obj: Any) -> Any:
        if isinstance(obj, dict):
            result = {}
            for k, v in obj.items():
                if k in ("_id", "user_id") and isinstance(v, str):
                    try:
                        result[k] = ObjectId(v)
                    except Exception:
                        result[k] = v
                else:
                    result[k] = self._convert_ids(v)
            return result
        elif isinstance(obj, list):
            return [self._convert_ids(i) for i in obj]
        return obj
    
    async def close(self):
        if self._motor_client:
            self._motor_client.close()


# Global instance
mongodb_mcp = MongoDBMCPClient()
