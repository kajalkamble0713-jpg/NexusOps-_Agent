"use client";

import { motion } from "framer-motion";
import { Task } from "@/lib/types";
import { PriorityBadge } from "./PriorityBadge";
import { Clock, Calendar, Tag, Zap } from "lucide-react";
import { formatRelativeDate, cn } from "@/lib/utils";

interface TaskCardProps {
  task: Task;
  onStatusChange?: (taskId: string, status: Task["status"]) => void;
  onEdit?: (task: Task) => void;
  isDragging?: boolean;
}

export function TaskCard({ task, onStatusChange, onEdit, isDragging }: TaskCardProps) {
  const isOverdue =
    task.due_date &&
    new Date(task.due_date) < new Date() &&
    task.status !== "done";

  return (
    <motion.div
      layout
      initial={{ opacity: 0, y: 5 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, scale: 0.95 }}
      whileHover={{ y: -1 }}
      className={cn(
        "card p-3.5 cursor-pointer group transition-all duration-200",
        isDragging && "shadow-[0_8px_24px_rgba(0,0,0,0.4)] scale-105 rotate-1",
        isOverdue && "border-[rgba(244,63,94,0.3)]",
        task.status === "done" && "opacity-60"
      )}
      onClick={() => onEdit?.(task)}
    >
      {/* Header */}
      <div className="flex items-start justify-between gap-2 mb-2">
        <h4
          className={cn(
            "text-sm font-medium text-[#F8FAFC] leading-snug flex-1",
            task.status === "done" && "line-through text-[#475569]"
          )}
        >
          {task.title}
        </h4>
        <PriorityBadge priority={task.priority} />
      </div>

      {/* Description */}
      {task.description && (
        <p className="text-xs text-[#94A3B8] mb-2 line-clamp-2 leading-relaxed">
          {task.description}
        </p>
      )}

      {/* Meta */}
      <div className="flex items-center gap-3 flex-wrap">
        {task.estimated_minutes && (
          <span className="flex items-center gap-1 text-[11px] text-[#475569]">
            <Clock size={11} />
            {task.estimated_minutes}m
          </span>
        )}

        {task.due_date && (
          <span
            className={cn(
              "flex items-center gap-1 text-[11px]",
              isOverdue ? "text-[#F43F5E]" : "text-[#475569]"
            )}
          >
            <Calendar size={11} />
            {formatRelativeDate(task.due_date)}
          </span>
        )}

        {task.tags.slice(0, 2).map((tag) => (
          <span
            key={tag}
            className="flex items-center gap-1 text-[11px] text-[#475569] bg-[rgba(148,163,184,0.06)] px-1.5 py-0.5 rounded"
          >
            <Tag size={9} />
            {tag}
          </span>
        ))}

        {/* AI Score */}
        {task.ai_score && (
          <span className="ml-auto flex items-center gap-1 text-[11px] text-[#8B5CF6]">
            <Zap size={10} />
            {task.ai_score}
          </span>
        )}
      </div>

      {/* Status change buttons */}
      {onStatusChange && task.status !== "done" && (
        <div className="mt-3 pt-2 border-t border-[rgba(148,163,184,0.08)] flex gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
          {task.status === "backlog" && (
            <button
              onClick={(e) => {
                e.stopPropagation();
                onStatusChange(task._id, "today");
              }}
              className="text-[11px] text-[#06B6D4] hover:text-[#F8FAFC] bg-[rgba(6,182,212,0.1)] hover:bg-[rgba(6,182,212,0.2)] px-2 py-1 rounded transition-all"
            >
              → Today
            </button>
          )}
          {(task.status === "today" || task.status === "backlog") && (
            <button
              onClick={(e) => {
                e.stopPropagation();
                onStatusChange(task._id, "in_progress");
              }}
              className="text-[11px] text-[#F59E0B] hover:text-[#F8FAFC] bg-[rgba(245,158,11,0.1)] hover:bg-[rgba(245,158,11,0.2)] px-2 py-1 rounded transition-all"
            >
              → In Progress
            </button>
          )}
          <button
            onClick={(e) => {
              e.stopPropagation();
              onStatusChange(task._id, "done");
            }}
            className="text-[11px] text-[#10B981] hover:text-[#F8FAFC] bg-[rgba(16,185,129,0.1)] hover:bg-[rgba(16,185,129,0.2)] px-2 py-1 rounded transition-all"
          >
            ✓ Done
          </button>
        </div>
      )}
    </motion.div>
  );
}
