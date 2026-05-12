"use client";

import { motion } from "framer-motion";
import { Goal } from "@/lib/types";
import { getGoalStatusColor, formatDate } from "@/lib/utils";
import { Target, TrendingUp, AlertTriangle, CheckCircle } from "lucide-react";

interface GoalHealthCardProps {
  goal: Goal;
}

function ProgressRing({
  progress,
  size = 80,
  strokeWidth = 6,
  color,
}: {
  progress: number;
  size?: number;
  strokeWidth?: number;
  color: string;
}) {
  const radius = (size - strokeWidth) / 2;
  const circumference = radius * 2 * Math.PI;
  const offset = circumference - (progress / 100) * circumference;

  return (
    <svg width={size} height={size} className="transform -rotate-90">
      {/* Background circle */}
      <circle
        cx={size / 2}
        cy={size / 2}
        r={radius}
        fill="none"
        stroke="rgba(148, 163, 184, 0.1)"
        strokeWidth={strokeWidth}
      />
      {/* Progress circle */}
      <motion.circle
        cx={size / 2}
        cy={size / 2}
        r={radius}
        fill="none"
        stroke={color}
        strokeWidth={strokeWidth}
        strokeLinecap="round"
        strokeDasharray={circumference}
        initial={{ strokeDashoffset: circumference }}
        animate={{ strokeDashoffset: offset }}
        transition={{ duration: 0.8, ease: "easeOut" }}
      />
    </svg>
  );
}

const categoryIcons: Record<string, string> = {
  career: "💼",
  health: "💪",
  learning: "📚",
  personal: "🌱",
  financial: "💰",
};

const statusConfig = {
  on_track: { label: "On Track", icon: CheckCircle, color: "#10B981" },
  at_risk: { label: "At Risk", icon: AlertTriangle, color: "#F59E0B" },
  critical: { label: "Critical", icon: AlertTriangle, color: "#F43F5E" },
  overdue: { label: "Overdue", icon: AlertTriangle, color: "#F43F5E" },
};

export function GoalHealthCard({ goal }: GoalHealthCardProps) {
  const status = goal.status || "on_track";
  const statusInfo = statusConfig[status] || statusConfig.on_track;
  const StatusIcon = statusInfo.icon;
  const progressColor = getGoalStatusColor(status);

  const completedMilestones = goal.milestones.filter((m) => m.completed).length;
  const totalMilestones = goal.milestones.length;

  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      className="card p-5 hover:border-[rgba(139,92,246,0.2)] transition-all duration-200"
    >
      {/* Header */}
      <div className="flex items-start justify-between mb-4">
        <div className="flex items-center gap-2">
          <span className="text-xl">{categoryIcons[goal.category] || "🎯"}</span>
          <div>
            <h3 className="text-sm font-semibold text-[#F8FAFC] leading-snug">
              {goal.title}
            </h3>
            <span className="text-[11px] text-[#475569] capitalize">{goal.category}</span>
          </div>
        </div>

        <div
          className="flex items-center gap-1 px-2 py-1 rounded-full text-[11px] font-medium"
          style={{
            background: `${statusInfo.color}15`,
            color: statusInfo.color,
            border: `1px solid ${statusInfo.color}30`,
          }}
        >
          <StatusIcon size={11} />
          {statusInfo.label}
        </div>
      </div>

      {/* Progress ring + stats */}
      <div className="flex items-center gap-4 mb-4">
        <div className="relative flex-shrink-0">
          <ProgressRing
            progress={goal.current_progress}
            size={72}
            strokeWidth={5}
            color={progressColor}
          />
          <div className="absolute inset-0 flex items-center justify-center">
            <span className="text-sm font-bold text-[#F8FAFC]">
              {goal.current_progress}%
            </span>
          </div>
        </div>

        <div className="flex-1 space-y-2">
          <div>
            <div className="flex justify-between text-[11px] mb-1">
              <span className="text-[#94A3B8]">Milestones</span>
              <span className="text-[#F8FAFC]">
                {completedMilestones}/{totalMilestones}
              </span>
            </div>
            <div className="h-1.5 bg-[rgba(148,163,184,0.1)] rounded-full overflow-hidden">
              <motion.div
                initial={{ width: 0 }}
                animate={{
                  width: `${totalMilestones > 0 ? (completedMilestones / totalMilestones) * 100 : 0}%`,
                }}
                transition={{ duration: 0.6, ease: "easeOut" }}
                className="h-full rounded-full"
                style={{ background: progressColor }}
              />
            </div>
          </div>

          {goal.target_date && (
            <div className="flex items-center gap-1 text-[11px] text-[#475569]">
              <Target size={10} />
              <span>Due {formatDate(goal.target_date)}</span>
              {goal.days_remaining !== undefined && (
                <span
                  className={
                    goal.days_remaining < 0
                      ? "text-[#F43F5E]"
                      : goal.days_remaining < 14
                      ? "text-[#F59E0B]"
                      : "text-[#10B981]"
                  }
                >
                  ({goal.days_remaining < 0
                    ? `${Math.abs(goal.days_remaining)}d overdue`
                    : `${goal.days_remaining}d left`})
                </span>
              )}
            </div>
          )}
        </div>
      </div>

      {/* AI Insight chip */}
      {goal.ai_suggestions && goal.ai_suggestions.length > 0 && (
        <div className="bg-[rgba(139,92,246,0.06)] border border-[rgba(139,92,246,0.15)] rounded-lg px-3 py-2">
          <div className="flex items-start gap-2">
            <TrendingUp size={12} className="text-[#8B5CF6] mt-0.5 flex-shrink-0" />
            <p className="text-[11px] text-[#94A3B8] leading-relaxed">
              {goal.ai_suggestions[0]}
            </p>
          </div>
        </div>
      )}
    </motion.div>
  );
}
