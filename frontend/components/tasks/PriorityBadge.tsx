"use client";

import { TaskPriority } from "@/lib/types";
import { cn } from "@/lib/utils";

interface PriorityBadgeProps {
  priority: TaskPriority;
  size?: "sm" | "md";
}

const priorityConfig = {
  critical: {
    label: "Critical",
    emoji: "🔴",
    className: "priority-critical",
  },
  high: {
    label: "High",
    emoji: "🟡",
    className: "priority-high",
  },
  normal: {
    label: "Normal",
    emoji: "🟢",
    className: "priority-normal",
  },
  low: {
    label: "Low",
    emoji: "⬛",
    className: "priority-low",
  },
};

export function PriorityBadge({ priority, size = "sm" }: PriorityBadgeProps) {
  const config = priorityConfig[priority] || priorityConfig.normal;

  return (
    <span
      className={cn(
        "inline-flex items-center gap-1 rounded-full font-medium",
        config.className,
        size === "sm" ? "text-[11px] px-2 py-0.5" : "text-xs px-2.5 py-1"
      )}
    >
      <span>{config.emoji}</span>
      {config.label}
    </span>
  );
}
