"use client";

import { motion } from "framer-motion";
import { AgentStep } from "@/lib/types";
import {
  Database,
  Brain,
  Lightbulb,
  Zap,
  CheckCircle2,
  AlertCircle,
  Search,
} from "lucide-react";
import { cn } from "@/lib/utils";

interface AgentStepCardProps {
  step: AgentStep;
  index: number;
  isLast: boolean;
}

const stepConfig = {
  query: {
    icon: Database,
    color: "#00ED64",
    bg: "rgba(0, 237, 100, 0.08)",
    border: "rgba(0, 237, 100, 0.2)",
    label: "MongoDB Query",
  },
  reasoning: {
    icon: Brain,
    color: "#8B5CF6",
    bg: "rgba(139, 92, 246, 0.08)",
    border: "rgba(139, 92, 246, 0.2)",
    label: "AI Reasoning",
  },
  insight: {
    icon: Lightbulb,
    color: "#F59E0B",
    bg: "rgba(245, 158, 11, 0.08)",
    border: "rgba(245, 158, 11, 0.2)",
    label: "Insight",
  },
  action: {
    icon: Zap,
    color: "#06B6D4",
    bg: "rgba(6, 182, 212, 0.08)",
    border: "rgba(6, 182, 212, 0.2)",
    label: "Action",
  },
  result: {
    icon: CheckCircle2,
    color: "#10B981",
    bg: "rgba(16, 185, 129, 0.08)",
    border: "rgba(16, 185, 129, 0.2)",
    label: "Result",
  },
  error: {
    icon: AlertCircle,
    color: "#F43F5E",
    bg: "rgba(244, 63, 94, 0.08)",
    border: "rgba(244, 63, 94, 0.2)",
    label: "Error",
  },
};

export function AgentStepCard({ step, index, isLast }: AgentStepCardProps) {
  const config = stepConfig[step.type] || stepConfig.reasoning;
  const Icon = config.icon;

  const time = new Date(step.timestamp).toLocaleTimeString("en-US", {
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
  });

  return (
    <motion.div
      initial={{ opacity: 0, x: -10, y: 5 }}
      animate={{ opacity: 1, x: 0, y: 0 }}
      transition={{ duration: 0.3, delay: index * 0.06 }}
      className={cn("relative flex gap-3", !isLast && "step-connector")}
    >
      {/* Step number + icon */}
      <div className="flex-shrink-0 flex flex-col items-center">
        <div
          className="w-9 h-9 rounded-full flex items-center justify-center border"
          style={{
            background: config.bg,
            borderColor: config.border,
          }}
        >
          <Icon size={15} style={{ color: config.color }} />
        </div>
      </div>

      {/* Content */}
      <div
        className="flex-1 rounded-xl p-4 mb-2 border"
        style={{
          background: config.bg,
          borderColor: config.border,
        }}
      >
        {/* Header */}
        <div className="flex items-center justify-between mb-2">
          <div className="flex items-center gap-2">
            <span
              className="text-[11px] font-semibold uppercase tracking-wider"
              style={{ color: config.color }}
            >
              {config.label}
            </span>
            {step.mongodb_tool && (
              <span className="mongodb-indicator">
                <span className="font-bold">M</span>
                {step.mongodb_tool}
              </span>
            )}
          </div>
          <span className="text-[11px] text-[#475569] font-mono">{time}</span>
        </div>

        {/* Content */}
        <p
          className={cn(
            "text-sm leading-relaxed whitespace-pre-wrap",
            step.type === "result" ? "text-[#F8FAFC]" : "text-[#94A3B8]"
          )}
        >
          {step.content}
        </p>

        {/* Metadata */}
        {step.metadata && Object.keys(step.metadata).length > 0 && (
          <div className="mt-2 pt-2 border-t border-[rgba(148,163,184,0.08)]">
            {step.metadata.result_count !== undefined && (
              <span className="text-[11px] text-[#475569]">
                {step.metadata.result_count as number} documents returned
              </span>
            )}
          </div>
        )}
      </div>
    </motion.div>
  );
}
