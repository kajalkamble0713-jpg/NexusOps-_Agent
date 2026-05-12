# NexusOps Agent

**Your life's operations center — intelligently automated.**

[![MongoDB Partner Track](https://img.shields.io/badge/MongoDB-Partner%20Track-00ED64?logo=mongodb)](https://mongodb.com)
[![Google Cloud](https://img.shields.io/badge/Google%20Cloud-Agent%20Builder-4285F4?logo=google-cloud)](https://cloud.google.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🎯 Overview

NexusOps Agent is an AI-powered personal and professional operations hub that goes beyond task management. Using Gemini's reasoning engine and MongoDB's flexible document store via MCP, it autonomously plans your day, reroutes priorities when disruptions hit, surfaces hidden patterns in how you work, and generates structured action plans — all while keeping you firmly in control.

**It is not a chatbot. It is an agent that thinks, decides, and acts on your behalf.**

## 🏆 Built For

**Google Cloud Rapid Agent Hackathon | MongoDB Partner Track**  
Target: MongoDB 1st Place ($5,000)

## ✨ Key Features

### 5 Intelligent Agents

1. **Morning Commander** - Autonomously plans your day based on tasks, goals, habits, and energy levels
2. **Priority Rebalancer** - Intelligently rearranges your schedule when urgent tasks appear
3. **Goal Health Analyst** - Tracks goal progress and proactively suggests recovery actions
4. **Pattern Intelligence Engine** - Discovers your productivity patterns and optimizes scheduling
5. **Autonomous Weekly Planner** - Generates balanced 5-day schedules with deep work blocks

### What Makes It Unique

- **Agent Chain Visualization** - See the agent's thought process in real-time
- **Bidirectional MongoDB MCP** - Agent reads AND writes back to MongoDB
- **Conflict-Aware Scheduling** - Reasons about downstream impact across dependent tasks
- **Pattern-Based Personalization** - Adapts suggestions based on your productivity patterns
- **No Vendor Lock-In** - All data lives in your MongoDB Atlas instance

## 🏗️ Architecture

```
User Input (Natural Language)
         ↓
   Next.js Frontend
         ↓
   FastAPI Backend (Cloud Run)
         ↓
   Google Cloud Agent Builder
         ↓ (Tool calls via MCP)
   MongoDB Atlas MCP Server ←→ MongoDB Atlas Cluster
         ↓
   Gemini 2.0 Reasoning Layer
         ↓
   Agent Response + Actions Streamed back to UI
```

### Tech Stack

- **Frontend**: Next.js 14 (App Router) + Tailwind CSS + Framer Motion
- **Backend**: Python FastAPI (Google Cloud Run)
- **Database**: MongoDB Atlas (via MongoDB MCP Server)
- **AI**: Google Cloud Agent Builder + Gemini 2.0 Flash / 1.5 Pro
- **MCP**: MongoDB Atlas MCP Server (official)
- **Auth**: Google OAuth 2.0
- **Real-time**: Server-Sent Events (SSE)

## 📋 Prerequisites

- Node.js 18+ and npm/yarn
- Python 3.11+
- MongoDB Atlas account (free tier works)
- Google Cloud account with Vertex AI enabled
- Google Cloud Agent Builder project

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/kajalkamble0713-jpg/NexusOps-_Agent.git
cd NexusOps-_Agent
```

### 2. Set Up MongoDB Atlas

1. Create a free MongoDB Atlas cluster at [mongodb.com/cloud/atlas](https://www.mongodb.com/cloud/atlas)
2. Create a database named `nexusops`
3. Get your connection string
4. Whitelist your IP address (or use 0.0.0.0/0 for development)

### 3. Set Up Google Cloud

1. Create a new Google Cloud project
2. Enable Vertex AI API
3. Create a service account with Vertex AI permissions
4. Download the service account key JSON
5. Set up Google Cloud Agent Builder project

### 4. Configure MongoDB MCP Server

Install the MongoDB MCP Server:

```bash
npm install -g @modelcontextprotocol/server-mongodb
```

### 5. Backend Setup

```bash
cd backend
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate

pip install -r requirements.txt
```

Create `backend/.env`:

```env
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/nexusops?retryWrites=true&w=majority
MONGODB_MCP_URL=http://localhost:3100
GOOGLE_CLOUD_PROJECT=your-project-id
VERTEX_AI_LOCATION=us-central1
GOOGLE_APPLICATION_CREDENTIALS=path/to/service-account-key.json
CORS_ORIGINS=http://localhost:3000
```

Seed demo data:

```bash
python demo/sample_data_seed.py
```

Run the backend:

```bash
uvicorn main:app --reload --port 8000
```

### 6. Frontend Setup

```bash
cd frontend
npm install
```

Create `frontend/.env.local`:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXTAUTH_SECRET=your-secret-key-here
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
NEXTAUTH_URL=http://localhost:3000
```

Run the frontend:

```bash
npm run dev
```

Visit [http://localhost:3000](http://localhost:3000)

## 📊 MongoDB Collections Schema

### users
```javascript
{
  _id: ObjectId,
  name: String,
  email: String,
  preferences: Object,
  timezone: String,
  createdAt: Date
}
```

### tasks
```javascript
{
  _id: ObjectId,
  userId: ObjectId,
  title: String,
  description: String,
  priority: String, // "critical", "high", "normal", "low"
  status: String, // "backlog", "today", "in_progress", "done"
  dueDate: Date,
  estimatedMinutes: Number,
  tags: [String],
  projectId: ObjectId,
  dependencies: [ObjectId],
  aiScore: Number, // 1-100
  completedAt: Date,
  metadata: Object
}
```

### goals
```javascript
{
  _id: ObjectId,
  userId: ObjectId,
  title: String,
  category: String,
  targetDate: Date,
  milestones: [Object],
  currentProgress: Number,
  weeklyTarget: Number,
  insights: [String],
  aiSuggestions: [String]
}
```

### daily_plans
```javascript
{
  _id: ObjectId,
  userId: ObjectId,
  date: Date,
  plannedTasks: [Object],
  actualSchedule: [Object],
  morningBrief: String,
  eveningReview: String,
  agentInsights: [String],
  mood: String
}
```

## 🎬 Demo Script

### 1. Morning Commander (0:20 - 1:00)
Type: "Plan my day. I have a team meeting at 2pm and low energy this morning."

Watch the agent:
- Query MongoDB for pending tasks
- Analyze priorities with Gemini
- Generate time-blocked schedule
- Write plan back to MongoDB

### 2. Priority Rebalancer (1:00 - 1:40)
Type: "My client just moved their deadline to tomorrow. Reprioritize everything."

Watch the agent:
- Read existing plan
- Intelligently defer low-impact tasks
- Insert critical task
- Update MongoDB

### 3. Goal Health Analyst (1:40 - 2:10)
Navigate to Goals screen.
Type: "Which of my goals are in danger?"

See:
- Goal health analysis
- Specific % behind calculation
- Recovery suggestions

### 4. Pattern Insights (2:10 - 2:40)
Navigate to Insights screen.
Type: "When should I schedule my deep work blocks?"

See:
- Heatmap of completion rates
- Peak hour analysis
- Personalized recommendations

## 🚀 Deployment

### Backend to Google Cloud Run

```bash
cd backend
gcloud builds submit --config=../infrastructure/cloudbuild.yaml
```

### Frontend to Vercel

```bash
cd frontend
vercel --prod
```

Update environment variables in both platforms.

## 🎨 Design System

### Color Palette

- **Background**: Midnight Navy (#0F172A)
- **Surface**: Slate (#1E293B)
- **Primary Accent**: Violet (#8B5CF6)
- **Secondary Accent**: Cyan (#06B6D4)
- **Success**: Emerald (#10B981)
- **Warning**: Amber (#F59E0B)
- **Danger**: Rose (#F43F5E)

### Typography

- **Font**: Inter (Google Fonts)
- **Heading Large**: 28px, weight 600
- **Body**: 14px, weight 400
- **Code**: JetBrains Mono, 13px

## 📝 License

MIT License - see [LICENSE](LICENSE) file for details

## 🤝 Contributing

This project was built for the Google Cloud Rapid Agent Hackathon. Contributions are welcome after the hackathon period.

## 📧 Contact

For questions or feedback, please open an issue on GitHub.

---

**Built with ❤️ using Gemini, Google Cloud Agent Builder, and MongoDB**
