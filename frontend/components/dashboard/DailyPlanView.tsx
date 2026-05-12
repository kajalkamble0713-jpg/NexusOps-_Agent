"use client";

import { motion } from "framer-motion";
import { DailyPlan, ScheduleBlock } from "@/lib/types";
import { Clock, Coffee, Users, Zap, FileText, Calendar } from "lucide-react";
import { cn } from "@/lib/utils";

interface DailyPlanViewProps {
  plan: DailyPlan | null;
  isLoading?: boolean;
}

const blockTypeConfig = {
  deep_work: {
    icon: Zap,
    color: "#8B5CF6",
    bg: "rgba(139, 92, 246, 0.1)",
    border: "rgba(139, 92, 246, 0.2)",
    label: "Deep Work",
  },
  meeting: {
    icon: Users,
    color: "#06B6D4",
    bg: "rgba(6, 182, 212, 0.1)",
    border: "rgba(6, 182, 212, 0.2)",
    label: "Meeting",
  },
  admin: {
    icon: FileText,
    color: "#94A3B8",
    bg: "rgba(148, 163, 184, 0.06)",
    border: "rgba(148, 163, 184, 0.12)",
    label: "Admin",
  },
  break: {
    icon: Coffee,
    color: "#10B981",
    bg: "rgba(16, 185, 129, 0.08)",
    border: "rgba(16, 185, 129, 0.15)",
    label: "Break",
  },
  task: {
    icon: Clock,
    color: "#F59E0B",
    bg: "rgba(245, 158, 11, 0.08)",
    border: "rgba(245, 158, 11, 0.15)",
    label: "Task",
  },
  habit: {
    icon: Calendar,
    color: "#10B981",
    bg: "rgba(16, 185, 129, 0.08)",
    border: "rgba(16, 185, 129, 0.15)",
    label: "Habit",
  },
  buffer: {
    icon: Clock,
    color: "#475569",
    bg: "rgba(71, 85, 105, 0.06)",
    border: "rgba(71, 85, 105, 0.12)",
    label: "Buffer",
  },
};

function ScheduleBlockItem({
  block,
  index,
}: {
  block: ScheduleBlock;
  index: number;
}) {
  const type = block.type || "task";
  const config = blockTypeConfig[type as keyof typeof blockTypeConfig] || blockTypeConfig.task;
  const Icon = config.icon;
  const timeStr = block.time || `${block.start_time || ""}-${block.end_time || ""}`;
  const taskTitle = block.task || block.title || "Untitled";

  return (
    <motion.div
      initial={{ opacity: 0, x: -8 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ delay: index * 0.05 }}
      className="flex items-center gap-3 p-2.5 rounded-lg border transition-all hover:scale-[1.01]"
      style={{ background: config.bg, borderColor: config.border }}
    >
      <div
        className="w-7 h-7 rounded-lg flex items-center justify-center flex-shrink-0"
        style={{ background: `${config.color}20` }}
      >
        <Icon size={13} style={{ color: config.color }} />
      </div>

      <div className="flex-1 min-w-0">
        <p className="text-xs font-medium text-[#F8FAFC] truncate">{taskTitle}</p>
        <p className="text-[11px] text-[#475569]">{timeStr}</p>
      </div>

      <span
        className="text-[10px] font-medium px-1.5 py-0.5 rounded"
        style={{ color: config.color, background: `${config.color}15` }}
      >
        {config.label}
      </span>
    </motion.div>
  );
}

export function DailyPlanView({ plan, isLoading }: DailyPlanViewProps) {
  if (isLoading) {
    return (
      <div className="space-y-2">
        {[...Array(5)].map((_, i) => (
          <div
            key={i}
            className="h-12 bg-[rgba(148,163,184,0.06)] rounded-lg animate-pulse"
          />
        ))}
      </div>
    );
  }

  if (!plan || plan.actual_schedule.length === 0) {
    return (
      <div className="text-center py-8">
        <Calendar size={28} className="text-[#475569] mx-auto mb-3" />
        <p className="text-sm text-[#94A3B8] mb-1">No plan for today yet</p>
        <p className="text-xs text-[#475569]">
          Ask the Morning Commander to plan your day
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-1.5">
      {plan.morning_brief && (
        <div className="bg-[rgba(139,92,246,0.06)] border border-[rgba(139,92,246,0.15)] rounded-lg px-3 py-2 mb-3">
          <p className="text-xs text-[#94A3B8] leading-relaxed">{plan.morning_brief}</p>
        </div>
      )}

      {plan.actual_schedule.map((block, i) => (
        <ScheduleBlockItem key={i} block={block} index={i} />
      ))}

      {plan.agent_insights && plan.agent_insights.length > 0 && (
        <div className="mt-3 pt-3 border-t border-[rgba(148,163,184,0.08)]">
          {plan.agent_insights.slice(0, 2).map((insight, i) => (
            <p key={i} className="text-[11px] text-[#475569] mb-1">
              💡 {insight}
            </p>
          ))}
        </div>
      )}
    </div>
  );
}
