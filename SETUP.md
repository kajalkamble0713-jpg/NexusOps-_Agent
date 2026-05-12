# NexusOps Agent — Complete Setup Guide

## 🚀 Quick Start (Local Development)

### Prerequisites

- **Node.js** 18+ and npm
- **Python** 3.11+
- **MongoDB** (local or Atlas)
- **Google Cloud** account with Vertex AI enabled

### 1. Clone and Install

```bash
git clone https://github.com/yourusername/nexusops-agent.git
cd nexusops-agent
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Linux/Mac)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env .env.local
# Edit .env.local with your MongoDB URI and Google Cloud credentials
```

**Required Environment Variables:**

```env
MONGODB_URI=mongodb+srv://username:password@cluster.mongodb.net/nexusops
GOOGLE_CLOUD_PROJECT=your-project-id
VERTEX_AI_LOCATION=us-central1
GOOGLE_APPLICATION_CREDENTIALS=path/to/service-account-key.json
```

### 3. Seed Demo Data

```bash
python demo/sample_data_seed.py
```

This creates:
- 1 demo user
- 15+ tasks (including overdue ones)
- 4 goals with milestones
- 5 habits with completion logs
- 30 days of daily plans
- Sample insights

### 4. Start Backend

```bash
uvicorn main:app --reload --port 8000
```

Backend will be available at `http://localhost:8000`

### 5. Frontend Setup

```bash
cd ../frontend

# Install dependencies
npm install

# Configure environment
cp .env.local.example .env.local
# Edit .env.local if needed (defaults should work)

# Start development server
npm run dev
```

Frontend will be available at `http://localhost:3000`

### 6. Access the App

1. Open `http://localhost:3000`
2. Click "Launch Demo"
3. You'll be logged in as the demo user (Alex Chen)

---

## 🔧 MongoDB Setup

### Option 1: MongoDB Atlas (Recommended)

1. Create a free cluster at [mongodb.com/cloud/atlas](https://www.mongodb.com/cloud/atlas)
2. Create a database named `nexusops`
3. Get your connection string
4. Whitelist your IP (or use `0.0.0.0/0` for development)
5. Update `MONGODB_URI` in `backend/.env`

### Option 2: Local MongoDB

```bash
# Install MongoDB locally
# Windows: Download from mongodb.com
# Mac: brew install mongodb-community
# Linux: apt-get install mongodb

# Start MongoDB
mongod --dbpath /path/to/data

# Use local connection string
MONGODB_URI=mongodb://localhost:27017/nexusops
```

---

## ☁️ Google Cloud Setup

### 1. Create Project

```bash
gcloud projects create nexusops-agent
gcloud config set project nexusops-agent
```

### 2. Enable APIs

```bash
gcloud services enable aiplatform.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable cloudbuild.googleapis.com
```

### 3. Create Service Account

```bash
gcloud iam service-accounts create nexusops-agent \
    --display-name="NexusOps Agent Service Account"

gcloud projects add-iam-policy-binding nexusops-agent \
    --member="serviceAccount:nexusops-agent@nexusops-agent.iam.gserviceaccount.com" \
    --role="roles/aiplatform.user"

gcloud iam service-accounts keys create service-account-key.json \
    --iam-account=nexusops-agent@nexusops-agent.iam.gserviceaccount.com
```

### 4. Set Environment Variable

```bash
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account-key.json
```

---

## 🧪 Testing the Agents

### Morning Commander

```
Plan my day. I have a team meeting at 2pm and low energy this morning.
```

### Priority Rebalancer

```
My client just moved their deadline to tomorrow. Reprioritize everything.
```

### Goal Health Analyst

```
Which of my goals are in danger?
```

### Pattern Intelligence Engine

```
When should I schedule my deep work blocks?
```

### Weekly Planner

```
Plan my next week.
```

---

## 🚢 Production Deployment

### Backend to Google Cloud Run

```bash
cd infrastructure
gcloud builds submit --config=cloudbuild.yaml ../backend
```

### Frontend to Vercel

```bash
cd frontend
vercel --prod
```

Update environment variables in both platforms:

**Cloud Run:**
- `MONGODB_URI`
- `GOOGLE_CLOUD_PROJECT`
- `VERTEX_AI_LOCATION`
- `CORS_ORIGINS` (set to your Vercel URL)

**Vercel:**
- `NEXT_PUBLIC_API_URL` (set to your Cloud Run URL)

---

## 📊 MongoDB Collections

The app uses these collections:

- `users` — User profiles and preferences
- `tasks` — All tasks with status, priority, AI scores
- `goals` — Goals with milestones and progress tracking
- `habits` — Habits with completion logs and streaks
- `daily_plans` — Agent-generated daily schedules
- `insights` — AI-generated insights and recommendations
- `agent_sessions` — Agent execution history

---

## 🐛 Troubleshooting

### Backend won't start

**Error:** `ModuleNotFoundError: No module named 'fastapi'`

**Solution:** Make sure you activated the virtual environment and installed dependencies:
```bash
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### MongoDB connection fails

**Error:** `ServerSelectionTimeoutError`

**Solution:** 
1. Check your `MONGODB_URI` is correct
2. Whitelist your IP in MongoDB Atlas
3. Verify MongoDB is running (if local)

### Gemini API errors

**Error:** `google.api_core.exceptions.PermissionDenied`

**Solution:**
1. Verify Vertex AI API is enabled
2. Check service account has `roles/aiplatform.user`
3. Verify `GOOGLE_APPLICATION_CREDENTIALS` path is correct

### Frontend build fails

**Error:** Type errors in TypeScript

**Solution:**
```bash
cd frontend
rm -rf .next node_modules
npm install
npm run build
```

### Agent not responding

**Check:**
1. Backend is running on port 8000
2. Check browser console for errors
3. Verify `NEXT_PUBLIC_API_URL` is set correctly
4. Check backend logs for errors

---

## 📝 Development Tips

### Hot Reload

Both frontend and backend support hot reload:
- **Backend:** `uvicorn main:app --reload`
- **Frontend:** `npm run dev`

### Database Inspection

Use MongoDB Compass or the Atlas UI to inspect data:
```bash
# Connect to local MongoDB
mongodb://localhost:27017/nexusops

# Or use Atlas connection string
```

### API Testing

Backend API docs available at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Logs

**Backend logs:**
```bash
# In backend directory
uvicorn main:app --reload --log-level debug
```

**Frontend logs:**
Check browser console (F12)

---

## 🎯 Next Steps

1. **Customize agents** — Edit agent prompts in `backend/agents/`
2. **Add more collections** — Extend MongoDB schema
3. **Improve UI** — Customize components in `frontend/components/`
4. **Add authentication** — Implement NextAuth.js with Google OAuth
5. **Deploy to production** — Follow deployment guide above

---

## 📚 Resources

- [MongoDB Atlas Docs](https://docs.atlas.mongodb.com/)
- [Google Cloud Vertex AI](https://cloud.google.com/vertex-ai/docs)
- [Next.js Documentation](https://nextjs.org/docs)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Gemini API](https://ai.google.dev/docs)

---

## 🤝 Support

For issues or questions:
1. Check the troubleshooting section above
2. Review backend logs
3. Open an issue on GitHub

---

**Built for Google Cloud Rapid Agent Hackathon | MongoDB Partner Track**
