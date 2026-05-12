"""
NexusOps Agent — Demo Data Seeder
Seeds MongoDB with realistic demo data for the hackathon demo.
"""

import asyncio
import os
import sys
import random
from datetime import datetime, timedelta

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '..', 'backend', '.env'))

MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
DB_NAME = "nexusops"

# Demo user
DEMO_USER = {
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
    "created_at": datetime.utcnow()
}

# Demo tasks
DEMO_TASKS = [
    {
        "title": "Finalize Q2 product roadmap",
        "description": "Review and finalize the product roadmap for Q2 with stakeholder input",
        "priority": "critical",
        "status": "in_progress",
        "estimated_minutes": 120,
        "tags": ["product", "strategy", "planning"],
        "ai_score": 95,
        "due_date": datetime.utcnow() + timedelta(days=1)
    },
    {
        "title": "Client presentation for Acme Corp",
        "description": "Prepare and deliver the quarterly review presentation",
        "priority": "critical",
        "status": "today",
        "estimated_minutes": 90,
        "tags": ["client", "presentation"],
        "ai_score": 92,
        "due_date": datetime.utcnow() + timedelta(hours=6)
    },
    {
        "title": "Code review: authentication module",
        "description": "Review PR #247 for the new OAuth implementation",
        "priority": "high",
        "status": "today",
        "estimated_minutes": 45,
        "tags": ["engineering", "security"],
        "ai_score": 78,
        "due_date": datetime.utcnow() + timedelta(days=1)
    },
    {
        "title": "Write technical blog post",
        "description": "Draft blog post about our microservices migration journey",
        "priority": "normal",
        "status": "backlog",
        "estimated_minutes": 180,
        "tags": ["writing", "marketing"],
        "ai_score": 45,
        "due_date": datetime.utcnow() + timedelta(days=7)
    },
    {
        "title": "Update team OKRs in Notion",
        "description": "Sync Q2 OKRs with the latest progress updates",
        "priority": "high",
        "status": "backlog",
        "estimated_minutes": 30,
        "tags": ["admin", "planning"],
        "ai_score": 65,
        "due_date": datetime.utcnow() + timedelta(days=2)
    },
    {
        "title": "Interview candidate for senior engineer role",
        "description": "Technical interview with Sarah Johnson",
        "priority": "high",
        "status": "today",
        "estimated_minutes": 60,
        "tags": ["hiring", "engineering"],
        "ai_score": 80,
        "due_date": datetime.utcnow() + timedelta(hours=4)
    },
    {
        "title": "Review and respond to investor emails",
        "description": "Respond to Series A investor inquiries",
        "priority": "high",
        "status": "backlog",
        "estimated_minutes": 45,
        "tags": ["fundraising", "admin"],
        "ai_score": 70,
        "due_date": datetime.utcnow() - timedelta(days=2)  # Overdue!
    },
    {
        "title": "Set up monitoring dashboards",
        "description": "Configure Datadog dashboards for production services",
        "priority": "normal",
        "status": "backlog",
        "estimated_minutes": 120,
        "tags": ["engineering", "devops"],
        "ai_score": 55,
        "due_date": datetime.utcnow() + timedelta(days=5)
    },
    {
        "title": "Quarterly team retrospective",
        "description": "Facilitate Q1 retrospective with the engineering team",
        "priority": "normal",
        "status": "backlog",
        "estimated_minutes": 90,
        "tags": ["team", "process"],
        "ai_score": 50,
        "due_date": datetime.utcnow() - timedelta(days=3)  # Overdue!
    },
    {
        "title": "Update API documentation",
        "description": "Document new endpoints added in v2.3 release",
        "priority": "low",
        "status": "backlog",
        "estimated_minutes": 60,
        "tags": ["documentation", "engineering"],
        "ai_score": 30,
        "due_date": datetime.utcnow() + timedelta(days=10)
    },
    {
        "title": "Analyze user churn data",
        "description": "Deep dive into March churn metrics and identify patterns",
        "priority": "high",
        "status": "in_progress",
        "estimated_minutes": 90,
        "tags": ["analytics", "product"],
        "ai_score": 82,
        "due_date": datetime.utcnow() + timedelta(days=1)
    },
    {
        "title": "1:1 with direct reports",
        "description": "Weekly 1:1 meetings with team leads",
        "priority": "high",
        "status": "today",
        "estimated_minutes": 120,
        "tags": ["management", "team"],
        "ai_score": 75,
        "due_date": datetime.utcnow() + timedelta(hours=8)
    },
    # Completed tasks for pattern analysis
    {
        "title": "Launch v2.3 release",
        "priority": "critical",
        "status": "done",
        "estimated_minutes": 180,
        "tags": ["engineering", "release"],
        "ai_score": 98,
        "completed_at": datetime.utcnow() - timedelta(days=2, hours=10)
    },
    {
        "title": "Investor pitch deck v3",
        "priority": "critical",
        "status": "done",
        "estimated_minutes": 240,
        "tags": ["fundraising", "strategy"],
        "ai_score": 96,
        "completed_at": datetime.utcnow() - timedelta(days=5, hours=9)
    },
    {
        "title": "Database optimization sprint",
        "priority": "high",
        "status": "done",
        "estimated_minutes": 360,
        "tags": ["engineering", "performance"],
        "ai_score": 85,
        "completed_at": datetime.utcnow() - timedelta(days=7, hours=11)
    },
]

# Demo goals
DEMO_GOALS = [
    {
        "title": "Launch NexusOps v2.0",
        "category": "career",
        "target_date": datetime.utcnow() + timedelta(days=45),
        "current_progress": 68,
        "weekly_target": 5,
        "milestones": [
            {"title": "Complete backend API", "target_date": (datetime.utcnow() - timedelta(days=10)).isoformat(), "completed": True},
            {"title": "Frontend MVP", "target_date": (datetime.utcnow() + timedelta(days=7)).isoformat(), "completed": False},
            {"title": "Beta testing", "target_date": (datetime.utcnow() + timedelta(days=21)).isoformat(), "completed": False},
            {"title": "Public launch", "target_date": (datetime.utcnow() + timedelta(days=45)).isoformat(), "completed": False}
        ],
        "insights": ["Backend is ahead of schedule", "Frontend needs acceleration"],
        "ai_suggestions": ["Allocate 3 extra hours per week to frontend", "Consider hiring a contractor for UI work"]
    },
    {
        "title": "Close Series A funding round",
        "category": "financial",
        "target_date": datetime.utcnow() + timedelta(days=60),
        "current_progress": 35,
        "weekly_target": 3,
        "milestones": [
            {"title": "Finalize pitch deck", "target_date": (datetime.utcnow() - timedelta(days=5)).isoformat(), "completed": True},
            {"title": "First 10 investor meetings", "target_date": (datetime.utcnow() + timedelta(days=14)).isoformat(), "completed": False},
            {"title": "Term sheet received", "target_date": (datetime.utcnow() + timedelta(days=45)).isoformat(), "completed": False},
            {"title": "Round closed", "target_date": (datetime.utcnow() + timedelta(days=60)).isoformat(), "completed": False}
        ],
        "insights": ["Investor outreach is behind schedule"],
        "ai_suggestions": ["Increase investor outreach to 5 meetings per week", "Leverage warm introductions from advisors"]
    },
    {
        "title": "Run a half marathon",
        "category": "health",
        "target_date": datetime.utcnow() + timedelta(days=90),
        "current_progress": 42,
        "weekly_target": 4,
        "milestones": [
            {"title": "Run 5K without stopping", "target_date": (datetime.utcnow() - timedelta(days=20)).isoformat(), "completed": True},
            {"title": "Complete 10K run", "target_date": (datetime.utcnow() + timedelta(days=15)).isoformat(), "completed": False},
            {"title": "15K training run", "target_date": (datetime.utcnow() + timedelta(days=45)).isoformat(), "completed": False},
            {"title": "Half marathon race day", "target_date": (datetime.utcnow() + timedelta(days=90)).isoformat(), "completed": False}
        ],
        "insights": ["Training consistency is good", "Need to increase long run distance"],
        "ai_suggestions": ["Add one long run per week (10K+)", "Include interval training on Tuesdays"]
    },
    {
        "title": "Complete AWS Solutions Architect certification",
        "category": "learning",
        "target_date": datetime.utcnow() + timedelta(days=30),
        "current_progress": 15,
        "weekly_target": 8,
        "milestones": [
            {"title": "Complete study materials", "target_date": (datetime.utcnow() + timedelta(days=14)).isoformat(), "completed": False},
            {"title": "Practice exams (score 80%+)", "target_date": (datetime.utcnow() + timedelta(days=25)).isoformat(), "completed": False},
            {"title": "Pass certification exam", "target_date": (datetime.utcnow() + timedelta(days=30)).isoformat(), "completed": False}
        ],
        "insights": ["At current pace, will miss deadline by 2 weeks"],
        "ai_suggestions": ["Study 2 hours daily instead of 1", "Focus on weak areas: networking and security"]
    }
]

# Demo habits
DEMO_HABITS = [
    {
        "name": "Morning workout",
        "frequency": "daily",
        "category": "health",
        "streak_count": 12,
        "best_streak": 21,
        "reminder_time": "07:00"
    },
    {
        "name": "Read for 30 minutes",
        "frequency": "daily",
        "category": "learning",
        "streak_count": 5,
        "best_streak": 14,
        "reminder_time": "21:00"
    },
    {
        "name": "Meditate",
        "frequency": "daily",
        "category": "wellness",
        "streak_count": 3,
        "best_streak": 30,
        "reminder_time": "07:30"
    },
    {
        "name": "Weekly team standup notes",
        "frequency": "weekly",
        "category": "productivity",
        "streak_count": 8,
        "best_streak": 12,
        "reminder_time": "09:00"
    },
    {
        "name": "Evening journal",
        "frequency": "daily",
        "category": "wellness",
        "streak_count": 7,
        "best_streak": 15,
        "reminder_time": "22:00"
    }
]


def generate_completion_log(streak: int, frequency: str = "daily") -> list:
    """Generate realistic completion log."""
    log = []
    today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    
    # Add streak days
    for i in range(streak):
        log.append((today - timedelta(days=i)).isoformat())
    
    # Add some historical completions with gaps
    for i in range(streak + 2, 30):
        if random.random() > 0.3:  # 70% completion rate
            log.append((today - timedelta(days=i)).isoformat())
    
    return log


def generate_daily_plans(user_id: str, days: int = 30) -> list:
    """Generate 30 days of daily plans."""
    plans = []
    today = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    
    schedule_templates = [
        [
            {"time": "09:00-10:30", "task": "Deep work: Product development", "type": "deep_work"},
            {"time": "10:30-11:00", "task": "Email & Slack", "type": "admin"},
            {"time": "11:00-12:30", "task": "Engineering review", "type": "deep_work"},
            {"time": "13:30-15:00", "task": "Team meetings", "type": "meeting"},
            {"time": "15:00-16:30", "task": "Administrative tasks", "type": "admin"},
        ],
        [
            {"time": "09:00-11:00", "task": "Strategic planning", "type": "deep_work"},
            {"time": "11:00-12:00", "task": "Investor calls", "type": "meeting"},
            {"time": "13:30-14:30", "task": "1:1 meetings", "type": "meeting"},
            {"time": "14:30-16:30", "task": "Product roadmap", "type": "deep_work"},
        ]
    ]
    
    insights_pool = [
        "High energy morning — completed 3 deep work sessions",
        "Afternoon slump affected productivity after 3pm",
        "Back-to-back meetings disrupted flow state",
        "Best day this week — 92% task completion",
        "Overcommitted — need to defer 2 tasks to tomorrow",
        "Morning workout boosted focus significantly",
        "Completed all critical tasks before noon"
    ]
    
    for i in range(days):
        date = today - timedelta(days=i)
        
        # Skip weekends
        if date.weekday() >= 5:
            continue
        
        completion_rate = random.uniform(0.5, 1.0)
        
        plans.append({
            "user_id": user_id,
            "date": date.isoformat(),
            "planned_tasks": [],
            "actual_schedule": random.choice(schedule_templates),
            "morning_brief": f"Today's focus: {random.choice(['Product', 'Engineering', 'Strategy', 'Sales'])} priorities",
            "agent_insights": [random.choice(insights_pool)],
            "mood": random.choice(["energized", "focused", "tired", "motivated", "stressed"]),
            "completion_rate": round(completion_rate * 100),
            "created_at": date.isoformat()
        })
    
    return plans


async def seed_database():
    """Seed the MongoDB database with demo data."""
    print("🌱 Starting NexusOps demo data seeding...")
    
    client = AsyncIOMotorClient(MONGODB_URI)
    db = client[DB_NAME]
    
    try:
        # Clear existing demo data
        print("🗑️  Clearing existing demo data...")
        await db.users.delete_many({"email": "demo@nexusops.ai"})
        
        # Insert demo user
        print("👤 Creating demo user...")
        user_result = await db.users.insert_one(DEMO_USER)
        user_id = str(user_result.inserted_id)
        print(f"   ✅ User created: {user_id}")
        
        # Clear user's existing data
        for collection in ["tasks", "goals", "habits", "daily_plans", "insights", "agent_sessions"]:
            await db[collection].delete_many({"user_id": user_id})
        
        # Insert tasks
        print("📋 Seeding tasks...")
        tasks_with_user = []
        for task in DEMO_TASKS:
            task_copy = task.copy()
            task_copy["user_id"] = user_id
            task_copy["created_at"] = datetime.utcnow() - timedelta(days=random.randint(1, 14))
            tasks_with_user.append(task_copy)
        
        task_result = await db.tasks.insert_many(tasks_with_user)
        print(f"   ✅ {len(task_result.inserted_ids)} tasks created")
        
        # Insert goals
        print("🎯 Seeding goals...")
        goals_with_user = []
        for goal in DEMO_GOALS:
            goal_copy = goal.copy()
            goal_copy["user_id"] = user_id
            goal_copy["created_at"] = datetime.utcnow() - timedelta(days=random.randint(30, 90))
            goals_with_user.append(goal_copy)
        
        goal_result = await db.goals.insert_many(goals_with_user)
        print(f"   ✅ {len(goal_result.inserted_ids)} goals created")
        
        # Insert habits with completion logs
        print("🔄 Seeding habits...")
        habits_with_user = []
        for habit in DEMO_HABITS:
            habit_copy = habit.copy()
            habit_copy["user_id"] = user_id
            habit_copy["completion_log"] = generate_completion_log(
                habit["streak_count"],
                habit["frequency"]
            )
            habit_copy["created_at"] = datetime.utcnow() - timedelta(days=60)
            habits_with_user.append(habit_copy)
        
        habit_result = await db.habits.insert_many(habits_with_user)
        print(f"   ✅ {len(habit_result.inserted_ids)} habits created")
        
        # Insert 30 days of daily plans
        print("📅 Seeding 30 days of daily plans...")
        daily_plans = generate_daily_plans(user_id, 30)
        
        if daily_plans:
            plan_result = await db.daily_plans.insert_many(daily_plans)
            print(f"   ✅ {len(plan_result.inserted_ids)} daily plans created")
        
        # Insert sample insights
        print("💡 Seeding insights...")
        sample_insights = [
            {
                "user_id": user_id,
                "type": "productivity_pattern",
                "content": "Your peak productivity window is 9-11am on Tuesdays and Wednesdays. Schedule your most demanding tasks during this time.",
                "generated_at": (datetime.utcnow() - timedelta(days=3)).isoformat(),
                "related_items": [],
                "acknowledged": False
            },
            {
                "user_id": user_id,
                "type": "goal_health",
                "content": "AWS Certification goal is at risk. At current pace, you'll miss the deadline by 2 weeks. Consider increasing daily study time.",
                "generated_at": (datetime.utcnow() - timedelta(days=1)).isoformat(),
                "related_items": [],
                "acknowledged": False
            },
            {
                "user_id": user_id,
                "type": "pattern",
                "content": "You consistently defer administrative tasks. Consider batching them on Friday afternoons to protect your deep work time.",
                "generated_at": (datetime.utcnow() - timedelta(days=7)).isoformat(),
                "related_items": [],
                "acknowledged": True
            },
            {
                "user_id": user_id,
                "type": "achievement",
                "content": "🎉 12-day workout streak! Your morning exercise habit is positively correlated with higher task completion rates (+23%).",
                "generated_at": datetime.utcnow().isoformat(),
                "related_items": [],
                "acknowledged": False
            }
        ]
        
        insight_result = await db.insights.insert_many(sample_insights)
        print(f"   ✅ {len(insight_result.inserted_ids)} insights created")
        
        # Create indexes for performance
        print("📊 Creating database indexes...")
        await db.tasks.create_index([("user_id", 1), ("status", 1)])
        await db.tasks.create_index([("user_id", 1), ("due_date", 1)])
        await db.goals.create_index([("user_id", 1)])
        await db.habits.create_index([("user_id", 1)])
        await db.daily_plans.create_index([("user_id", 1), ("date", -1)])
        await db.insights.create_index([("user_id", 1), ("generated_at", -1)])
        print("   ✅ Indexes created")
        
        print("\n✨ Demo data seeding complete!")
        print(f"\n📊 Summary:")
        print(f"   User ID: {user_id}")
        print(f"   Email: demo@nexusops.ai")
        print(f"   Tasks: {len(tasks_with_user)}")
        print(f"   Goals: {len(goals_with_user)}")
        print(f"   Habits: {len(habits_with_user)}")
        print(f"   Daily Plans: {len(daily_plans)}")
        print(f"   Insights: {len(sample_insights)}")
        print(f"\n🚀 Ready for demo! User ID: {user_id}")
        
        return user_id
    
    finally:
        client.close()


if __name__ == "__main__":
    asyncio.run(seed_database())
