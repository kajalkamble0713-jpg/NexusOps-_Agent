# NexusOps Agent — 3-Minute Demo Script

## Setup (Before Recording)
1. Seed the database: `python demo/sample_data_seed.py`
2. Start backend: `cd backend && uvicorn main:app --reload`
3. Start frontend: `cd frontend && npm run dev`
4. Open browser to `http://localhost:3000`
5. Click "Launch Demo" to enter the dashboard

---

## [0:00 – 0:20] Hook — The Problem

**Screen:** Landing page

**Script:**
> "You have 23 tasks, 3 active goals, 5 habits to track — and a Monday morning. Most apps just show you a list. NexusOps Agent figures out your day for you."

**Action:** Click "Launch Demo" → Dashboard loads

---

## [0:20 – 1:00] Morning Commander Demo

**Screen:** Navigate to Agent Workspace (click "Agent" in sidebar)

**Script:**
> "Let's start with the Morning Commander. I'll ask it to plan my day."

**Action:** Type in the agent panel:
```
Plan my day. I have a team meeting at 2pm and low energy this morning.
```

**What to show:**
- Watch agent steps appear in real-time:
  - [Step 1] 🟢 MongoDB Query — "Querying MongoDB for pending tasks..."
  - [Step 2] 🟣 AI Reasoning — "Analyzing priorities with Gemini..."
  - [Step 3] 🟡 Insight — "Found 3 overdue items..."
  - [Step 4] 🔵 Action — "Generating time-blocked schedule..."
  - [Step 5] 🟢 MongoDB — "Writing plan to MongoDB..."
  - [Result] ✅ "Here's your optimized day →"

**Highlight:** Point out the green "M" MongoDB indicators on query/write steps

---

## [1:00 – 1:40] Priority Rebalancer Demo

**Screen:** Still in Agent Workspace

**Script:**
> "Now watch what happens when something urgent drops in."

**Action:** Type:
```
My client just moved their deadline to tomorrow. Reprioritize everything.
```

**What to show:**
- Agent reads existing plan from MongoDB
- Identifies 3 lower-priority tasks to defer
- Shows impact assessment
- Updates MongoDB with new schedule
- Confirms with summary of changes

**Highlight:** "The agent didn't just add a task — it reasoned about downstream impact and updated 4 documents in MongoDB."

---

## [1:40 – 2:10] Goal Health Analyst Demo

**Screen:** Navigate to Goals page (sidebar)

**Script:**
> "Let's check on my goals."

**Action:** Back in Agent panel, type:
```
Which of my goals are in danger?
```

**What to show:**
- Goal health cards with animated progress rings
- Agent identifies AWS Certification as "at risk"
- Shows specific % behind calculation
- Recovery suggestions written to MongoDB

**Highlight:** "At current pace, you'll miss this by 2 weeks — with specific actions to recover."

---

## [2:10 – 2:40] Pattern Insights Demo

**Screen:** Navigate to Insights page

**Script:**
> "Now let's look at how I actually work."

**What to show:**
- GitHub-style heatmap of task completions
- Peak hour bar chart (9-11am highlighted)
- Weekly pattern (Tuesday = best day)

**Action:** In agent panel, type:
```
When should I schedule my deep work blocks?
```

**What to show:**
- Pattern engine analyzes 30 days of data
- Personalized recommendation based on actual patterns
- Insight saved to MongoDB

---

## [2:40 – 3:00] Close

**Screen:** Show architecture diagram or dashboard overview

**Script:**
> "NexusOps Agent — built with Gemini 2.0, Google Cloud Agent Builder, and MongoDB Atlas MCP. All your data stays yours, in your Atlas cluster. The agent doesn't just display your data — it actively restructures it based on reasoning."

**Final shot:** Dashboard with all panels visible

---

## Key Talking Points

1. **Not a chatbot** — It's an agent that reads AND writes to MongoDB
2. **Bidirectional MCP** — Every agent step shows the MongoDB tool being called
3. **Real-time streaming** — Watch the agent think step by step
4. **Persistent memory** — Plans, insights, and changes are saved to Atlas
5. **5 specialized agents** — Each optimized for a specific operational task

---

## Technical Highlights for Judges

- **Google Cloud Agent Builder** orchestrates multi-step reasoning
- **Gemini 2.0 Flash** for fast, intelligent responses
- **MongoDB Atlas MCP Server** for all database operations
- **SSE streaming** for real-time agent step visualization
- **Next.js 14** with Framer Motion for smooth UI
- **FastAPI** on Cloud Run for scalable backend
