"""Pydantic models for NexusOps Agent."""

from datetime import datetime
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from bson import ObjectId


class PyObjectId(ObjectId):
    """Custom ObjectId type for Pydantic."""
    
    @classmethod
    def __get_validators__(cls):
        yield cls.validate
    
    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)
    
    @classmethod
    def __get_pydantic_json_schema__(cls, field_schema):
        field_schema.update(type="string")


class UserPreferences(BaseModel):
    """User preferences."""
    theme: str = "dark"
    notifications_enabled: bool = True
    work_hours_start: int = 9
    work_hours_end: int = 17
    deep_work_duration: int = 90  # minutes


class User(BaseModel):
    """User model."""
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    name: str
    email: str
    preferences: UserPreferences = Field(default_factory=UserPreferences)
    timezone: str = "UTC"
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class Task(BaseModel):
    """Task model."""
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    user_id: PyObjectId
    title: str
    description: Optional[str] = None
    priority: str = "normal"  # critical, high, normal, low
    status: str = "backlog"  # backlog, today, in_progress, done
    due_date: Optional[datetime] = None
    estimated_minutes: Optional[int] = None
    tags: List[str] = Field(default_factory=list)
    project_id: Optional[PyObjectId] = None
    dependencies: List[PyObjectId] = Field(default_factory=list)
    ai_score: Optional[int] = None  # 1-100
    completed_at: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = Field(default_factory=dict)
    
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class Milestone(BaseModel):
    """Milestone model."""
    title: str
    target_date: datetime
    completed: bool = False
    completed_at: Optional[datetime] = None


class Goal(BaseModel):
    """Goal model."""
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    user_id: PyObjectId
    title: str
    category: str  # career, health, learning, personal, financial
    target_date: datetime
    milestones: List[Milestone] = Field(default_factory=list)
    current_progress: int = 0  # 0-100
    weekly_target: Optional[int] = None
    insights: List[str] = Field(default_factory=list)
    ai_suggestions: List[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class Habit(BaseModel):
    """Habit model."""
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    user_id: PyObjectId
    name: str
    frequency: str  # daily, weekly, custom
    completion_log: List[datetime] = Field(default_factory=list)
    streak_count: int = 0
    best_streak: int = 0
    category: str  # health, productivity, learning, wellness
    reminder_time: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class ScheduleBlock(BaseModel):
    """Schedule block model."""
    start_time: str  # HH:MM format
    end_time: str
    task_id: Optional[PyObjectId] = None
    title: str
    type: str  # task, meeting, break, deep_work
    energy_level: Optional[str] = None  # high, medium, low


class DailyPlan(BaseModel):
    """Daily plan model."""
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    user_id: PyObjectId
    date: datetime
    planned_tasks: List[PyObjectId] = Field(default_factory=list)
    actual_schedule: List[ScheduleBlock] = Field(default_factory=list)
    morning_brief: Optional[str] = None
    evening_review: Optional[str] = None
    agent_insights: List[str] = Field(default_factory=list)
    mood: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class AgentStep(BaseModel):
    """Agent reasoning step."""
    type: str  # query, reasoning, insight, action, result
    content: str
    mongodb_tool: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = Field(default_factory=dict)


class AgentSession(BaseModel):
    """Agent session model."""
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    user_id: PyObjectId
    session_type: str  # morning_commander, priority_rebalancer, etc.
    input: str
    steps: List[AgentStep] = Field(default_factory=list)
    output: Optional[str] = None
    tokens_used: Optional[int] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    satisfaction_score: Optional[int] = None
    
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class Insight(BaseModel):
    """Insight model."""
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    user_id: PyObjectId
    type: str  # pattern, recommendation, warning, achievement
    content: str
    generated_at: datetime = Field(default_factory=datetime.utcnow)
    related_items: List[PyObjectId] = Field(default_factory=list)
    acknowledged: bool = False
    
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class AgentRequest(BaseModel):
    """Agent invocation request."""
    user_id: str
    input: str
    agent_type: Optional[str] = "morning_commander"
    context: Dict[str, Any] = Field(default_factory=dict)


class AgentResponse(BaseModel):
    """Agent invocation response."""
    session_id: str
    output: str
    steps: List[AgentStep]
    tokens_used: Optional[int] = None
