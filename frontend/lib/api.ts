/**
 * API client for NexusOps Agent backend
 */

import { Task, Goal, Habit, Insight, AgentRequest, AgentStep, TaskStats } from "./types";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

class APIError extends Error {
  constructor(
    message: string,
    public status: number,
    public data?: unknown
  ) {
    super(message);
    this.name = "APIError";
  }
}

async function fetchAPI<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const url = `${API_BASE}/api${endpoint}`;

  const response = await fetch(url, {
    headers: {
      "Content-Type": "application/json",
      ...options.headers,
    },
    ...options,
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new APIError(
      errorData.detail || `HTTP ${response.status}`,
      response.status,
      errorData
    );
  }

  return response.json();
}

// ─── Tasks ────────────────────────────────────────────────────────────────────

export const tasksAPI = {
  getAll: (userId: string, status?: string, priority?: string) =>
    fetchAPI<{ tasks: Task[]; count: number }>(
      `/tasks?user_id=${userId}${status ? `&status=${status}` : ""}${priority ? `&priority=${priority}` : ""}`
    ),

  create: (task: Partial<Task>) =>
    fetchAPI<{ task_id: string; message: string }>("/tasks", {
      method: "POST",
      body: JSON.stringify(task),
    }),

  update: (taskId: string, data: Partial<Task>) =>
    fetchAPI<{ message: string; modified: number }>(`/tasks/${taskId}`, {
      method: "PUT",
      body: JSON.stringify(data),
    }),

  delete: (taskId: string) =>
    fetchAPI<{ message: string }>(`/tasks/${taskId}`, {
      method: "DELETE",
    }),

  getStats: (userId: string) =>
    fetchAPI<{ stats: TaskStats; total: number }>(`/tasks/stats/${userId}`),
};

// ─── Goals ────────────────────────────────────────────────────────────────────

export const goalsAPI = {
  getAll: (userId: string, category?: string) =>
    fetchAPI<{ goals: Goal[]; count: number }>(
      `/goals?user_id=${userId}${category ? `&category=${category}` : ""}`
    ),

  create: (goal: Partial<Goal>) =>
    fetchAPI<{ goal_id: string; message: string }>("/goals", {
      method: "POST",
      body: JSON.stringify(goal),
    }),

  update: (goalId: string, data: Partial<Goal>) =>
    fetchAPI<{ message: string }>(`/goals/${goalId}`, {
      method: "PUT",
      body: JSON.stringify(data),
    }),

  updateProgress: (goalId: string, progress: number) =>
    fetchAPI<{ message: string; progress: number }>(
      `/goals/${goalId}/progress?progress=${progress}`,
      { method: "PUT" }
    ),

  delete: (goalId: string) =>
    fetchAPI<{ message: string }>(`/goals/${goalId}`, {
      method: "DELETE",
    }),
};

// ─── Habits ───────────────────────────────────────────────────────────────────

export const habitsAPI = {
  getAll: (userId: string) =>
    fetchAPI<{ habits: Habit[]; count: number }>(`/habits?user_id=${userId}`),

  create: (habit: Partial<Habit>) =>
    fetchAPI<{ habit_id: string; message: string }>("/habits", {
      method: "POST",
      body: JSON.stringify(habit),
    }),

  complete: (habitId: string) =>
    fetchAPI<{ message: string; streak: number; best_streak: number }>(
      `/habits/${habitId}/complete`,
      { method: "POST" }
    ),

  delete: (habitId: string) =>
    fetchAPI<{ message: string }>(`/habits/${habitId}`, {
      method: "DELETE",
    }),
};

// ─── Insights ─────────────────────────────────────────────────────────────────

export const insightsAPI = {
  getAll: (userId: string, type?: string, acknowledged?: boolean) =>
    fetchAPI<{ insights: Insight[]; count: number }>(
      `/insights?user_id=${userId}${type ? `&insight_type=${type}` : ""}${acknowledged !== undefined ? `&acknowledged=${acknowledged}` : ""}`
    ),

  acknowledge: (insightId: string) =>
    fetchAPI<{ message: string }>(`/insights/${insightId}/acknowledge`, {
      method: "PUT",
    }),

  getDailyPlan: (userId: string, date?: string) =>
    fetchAPI<{ plan: unknown }>(
      `/insights/daily-plan/${userId}${date ? `?date=${date}` : ""}`
    ),
};

// ─── Agent ────────────────────────────────────────────────────────────────────

export const agentAPI = {
  getTypes: () =>
    fetchAPI<{ agents: unknown[] }>("/agent/types"),

  /**
   * Invoke an agent with SSE streaming.
   * Returns a ReadableStream of AgentStep events.
   */
  invoke: async (
    request: AgentRequest,
    onStep: (step: AgentStep) => void,
    onDone: () => void,
    onError: (error: Error) => void
  ): Promise<void> => {
    try {
      const response = await fetch(`${API_BASE}/api/agent/invoke`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(request),
      });

      if (!response.ok) {
        throw new APIError(`HTTP ${response.status}`, response.status);
      }

      const reader = response.body!.getReader();
      const decoder = new TextDecoder();

      while (true) {
        const { done, value } = await reader.read();
        if (done) break;

        const text = decoder.decode(value, { stream: true });
        const lines = text.split("\n");

        for (const line of lines) {
          if (line.startsWith("data: ")) {
            const data = line.slice(6).trim();

            if (data === "[DONE]") {
              onDone();
              return;
            }

            try {
              const step = JSON.parse(data) as AgentStep;
              onStep(step);
            } catch {
              // Skip malformed lines
            }
          }
        }
      }

      onDone();
    } catch (error) {
      onError(error instanceof Error ? error : new Error(String(error)));
    }
  },
};

// ─── User ─────────────────────────────────────────────────────────────────────

export const userAPI = {
  getDemoUser: () =>
    fetchAPI<{ user: { _id: string; name: string; email: string } }>("/users/demo"),
};
