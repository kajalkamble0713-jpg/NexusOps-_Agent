"""NexusOps Agent — FastAPI Backend."""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from mcp.mongodb_client import mongodb_mcp
from routers import agent, tasks, goals, habits, insights

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan — startup and shutdown."""
    # Startup
    logger.info("Starting NexusOps Agent backend...")
    await mongodb_mcp.initialize()
    logger.info("MongoDB connection established")
    
    yield
    
    # Shutdown
    logger.info("Shutting down NexusOps Agent backend...")
    await mongodb_mcp.close()


app = FastAPI(
    title="NexusOps Agent API",
    description="AI-powered personal and professional operations hub",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(agent.router, prefix=settings.api_prefix)
app.include_router(tasks.router, prefix=settings.api_prefix)
app.include_router(goals.router, prefix=settings.api_prefix)
app.include_router(habits.router, prefix=settings.api_prefix)
app.include_router(insights.router, prefix=settings.api_prefix)


@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "name": "NexusOps Agent API",
        "version": "1.0.0",
        "status": "operational",
        "tagline": "Your life's operations center — intelligently automated."
    }


@app.get("/health")
async def health_check():
    """Detailed health check."""
    return {
        "status": "healthy",
        "mongodb": "connected",
        "agents": ["morning_commander", "priority_rebalancer", "goal_analyst", "pattern_engine", "weekly_planner"]
    }


@app.get(f"{settings.api_prefix}/users/demo")
async def get_demo_user():
    """Get demo user for testing."""
    users = await mongodb_mcp.call_tool(
        tool_name="mongodb_find",
        arguments={
            "collection": "users",
            "filter": {"email": "demo@nexusops.ai"},
            "limit": 1,
            "database": settings.mongodb_database
        }
    )
    
    if users:
        return {"user": users[0]}
    
    # Create demo user if not exists
    demo_user = {
        "name": "Alex Chen",
        "email": "demo@nexusops.ai",
        "preferences": {
            "theme": "dark",
            "notifications_enabled": True,
            "work_hours_start": 9,
            "work_hours_end": 17,
            "deep_work_duration": 90
        },
        "timezone": "America/New_York"
    }
    
    result = await mongodb_mcp.call_tool(
        tool_name="mongodb_insert_one",
        arguments={
            "collection": "users",
            "document": demo_user,
            "database": settings.mongodb_database
        }
    )
    
    demo_user["_id"] = result.get("inserted_id")
    return {"user": demo_user}
