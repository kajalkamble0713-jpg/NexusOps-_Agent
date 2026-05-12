/**
 * TypeScript interfaces for NexusOps Agent
 */

export interface User {
  _id: string;
  name: string;
  email: string;
  preferences: UserPreferences;
  timezone: string;
  created_at: string;
}

export interface UserPreferences {
  theme: string;
  notifications_enabled: boolean;
  work_hours_start: number;
  work_hours_end: number;
  deep_work_duration: number;
}

export type TaskPriority = "critical" | "high" | "normal" | "low";
export type TaskStatus = "backlog" | "today" | "in_progress" | "done";

export interface Task {
  _id: string;
  user_id: string;
  title: string;
  description?: string;
  priority: TaskPriority;
  status: TaskStatus;
  due_date?: string;
  estimated_minutes?: number;
  tags: string[];
  project_id?: string;
  dependencies: string[];
  ai_score?: number;
  completed_at?: string;
  created_at: string;
  metadata: Record<string, unknown>;
}

export interface Milestone {
  title: string;
  target_date: string;
  completed: boolean;
  completed_at?: string;
}

export type GoalCategory = "career" | "health" | "learning" | "personal" | "financial";
export type GoalStatus = "on_track" | "at_risk" | "critical" | "overdue";

export interface Goal {
  _id: string;
  user_id: string;
  title: string;
  category: GoalCategory;
  target_date: string;
  milestones: Milestone[];
  current_progress: number;
  weekly_target?: number;
  insights: string[];
  ai_suggestions: string[];
  created_at: string;
  // Computed by agent
  status?: GoalStatus;
  days_remaining?: number;
}

export interface Habit {
  _id: string;
  user_id: string;
  name: string;
  frequency: "daily" | "weekly" | "custom";
  completion_log: string[];
  streak_count: number;
  best_streak: number;
  category: "health" | "productivity" | "learning" | "wellness";
  reminder_time?: string;
  created_at: string;
}

export interface ScheduleBlock {
  start_time?: string;
  end_time?: string;
  time?: string; // Combined "HH:MM-HH:MM" format
  task_id?: string;
  title?: string;
  task?: string;
  type: "task" | "meeting" | "break" | "deep_work" | "admin" | "habit" | "buffer";
  energy_level?: "high" | "medium" | "low";
  priority?: string;
  reason?: string;
}

export interface DailyPlan {
  _id: string;
  user_id: string;
  date: string;
  planned_tasks: string[];
  actual_schedule: ScheduleBlock[];
  morning_brief?: string;
  evening_review?: string;
  agent_insights: string[];
  mood?: string;
  created_at: string;
}

export type AgentStepType = "query" | "reasoning" | "insight" | "action" | "result" | "error";

export interface AgentStep {
  type: AgentStepType;
  content: string;
  mongodb_tool?: string;
  timestamp: string;
  metadata: Record<string, unknown>;
}

export interface AgentSession {
  _id: string;
  user_id: string;
  session_type: string;
  input: string;
  steps: AgentStep[];
  output?: string;
  tokens_used?: number;
  timestamp: string;
  satisfaction_score?: number;
}

export type InsightType = "pattern" | "recommendation" | "warning" | "achievement" | "goal_health" | "productivity_pattern";

export interface Insight {
  _id: string;
  user_id: string;
  type: InsightType;
  content: string;
  generated_at: string;
  related_items: string[];
  acknowledged: boolean;
}

export interface AgentRequest {
  user_id: string;
  input: string;
  agent_type?: string;
  context?: Record<string, unknown>;
}

export type AgentType =
  | "morning_commander"
  | "priority_rebalancer"
  | "goal_analyst"
  | "pattern_engine"
  | "weekly_planner";

export interface AgentInfo {
  id: AgentType;
  name: string;
  description: string;
  trigger_phrases: string[];
}

export interface TaskStats {
  backlog: number;
  today: number;
  in_progress: number;
  done: number;
  total: number;
}
