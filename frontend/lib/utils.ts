import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function formatDate(date: string | Date): string {
  const d = typeof date === "string" ? new Date(date) : date;
  return d.toLocaleDateString("en-US", {
    month: "short",
    day: "numeric",
    year: "numeric",
  });
}

export function formatTime(date: string | Date): string {
  const d = typeof date === "string" ? new Date(date) : date;
  return d.toLocaleTimeString("en-US", {
    hour: "2-digit",
    minute: "2-digit",
  });
}

export function formatRelativeDate(date: string | Date): string {
  const d = typeof date === "string" ? new Date(date) : date;
  const now = new Date();
  const diffMs = d.getTime() - now.getTime();
  const diffDays = Math.round(diffMs / (1000 * 60 * 60 * 24));

  if (diffDays === 0) return "Today";
  if (diffDays === 1) return "Tomorrow";
  if (diffDays === -1) return "Yesterday";
  if (diffDays > 0) return `In ${diffDays} days`;
  return `${Math.abs(diffDays)} days ago`;
}

export function getDayOfWeek(): string {
  return new Date().toLocaleDateString("en-US", { weekday: "long" });
}

export function getGreeting(): string {
  const hour = new Date().getHours();
  if (hour < 12) return "Good morning";
  if (hour < 17) return "Good afternoon";
  return "Good evening";
}

export function getPriorityColor(priority: string): string {
  switch (priority) {
    case "critical":
      return "priority-critical";
    case "high":
      return "priority-high";
    case "normal":
      return "priority-normal";
    case "low":
      return "priority-low";
    default:
      return "priority-normal";
  }
}

export function getGoalStatusColor(status: string): string {
  switch (status) {
    case "on_track":
      return "#10B981";
    case "at_risk":
      return "#F59E0B";
    case "critical":
    case "overdue":
      return "#F43F5E";
    default:
      return "#94A3B8";
  }
}

export function truncate(str: string, maxLength: number): string {
  if (str.length <= maxLength) return str;
  return str.slice(0, maxLength) + "...";
}

export function getUserId(): string {
  if (typeof window === "undefined") return "demo_user_001";
  return localStorage.getItem("nexusops_user_id") || "demo_user_001";
}

export function getUserName(): string {
  if (typeof window === "undefined") return "Alex";
  return localStorage.getItem("nexusops_user_name") || "Alex";
}
