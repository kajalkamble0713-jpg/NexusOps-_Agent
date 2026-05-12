"use client";

import { motion } from "framer-motion";
import { Insight } from "@/lib/types";
import { insightsAPI } from "@/lib/api";
import { Lightbulb, TrendingUp, AlertTriangle, Trophy, X } from "lucide-react";
import { cn } from "@/lib/utils";
import { formatDate } from "@/lib/utils";
import toast from "react-hot-toast";

interface InsightCardProps {
  insight: Insight;
  onAcknowledge?: () => void;
}

const insightConfig = {
  pattern: {
    icon: TrendingUp,
    color: "#8B5CF6",
    bg: "rgba(139, 92, 246, 0.08)",
    border: "rgba(139, 92, 246, 0.2)",
  },
  recommendation: {
    icon: Lightbulb,
    color: "#06B6D4",
    bg: "rgba(6, 182, 212, 0.08)",
    border: "rgba(6, 182, 212, 0.2)",
  },
  warning: {
    icon: AlertTriangle,
    color: "#F59E0B",
    bg: "rgba(245, 158, 11, 0.08)",
    border: "rgba(245, 158, 11, 0.2)",
  },
  achievement: {
    icon: Trophy,
    color: "#10B981",
    bg: "rgba(16, 185, 129, 0.08)",
    border: "rgba(16, 185, 129, 0.2)",
  },
  goal_health: {
    icon: AlertTriangle,
    color: "#F59E0B",
    bg: "rgba(245, 158, 11, 0.08)",
    border: "rgba(245, 158, 11, 0.2)",
  },
  productivity_pattern: {
    icon: TrendingUp,
    color: "#8B5CF6",
    bg: "rgba(139, 92, 246, 0.08)",
    border: "rgba(139, 92, 246, 0.2)",
  },
};

export function InsightCard({ insight, onAcknowledge }: InsightCardProps) {
  const config =
    insightConfig[insight.type as keyof typeof insightConfig] ||
    insightConfig.recommendation;
  const Icon = config.icon;

  const handleAcknowledge = async () => {
    try {
      await insightsAPI.acknowledge(insight._id);
      toast.success("Insight acknowledged");
      onAcknowledge?.();
    } catch {
      toast.error("Failed to acknowledge insight");
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 5 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, scale: 0.95 }}
      className={cn(
        "relative p-4 rounded-xl border transition-all duration-200",
        insight.acknowledged ? "opacity-50" : ""
      )}
      style={{ background: config.bg, borderColor: config.border }}
    >
      {/* Dismiss button */}
      {!insight.acknowledged && (
        <button
          onClick={handleAcknowledge}
          className="absolute top-3 right-3 p-1 rounded-lg text-[#475569] hover:text-[#94A3B8] hover:bg-[rgba(148,163,184,0.1)] transition-all"
        >
          <X size={13} />
        </button>
      )}

      <div className="flex items-start gap-3 pr-6">
        <div
          className="w-8 h-8 rounded-lg flex items-center justify-center flex-shrink-0"
          style={{ background: `${config.color}20` }}
        >
          <Icon size={15} style={{ color: config.color }} />
        </div>

        <div className="flex-1 min-w-0">
          <p className="text-sm text-[#F8FAFC] leading-relaxed mb-1">
            {insight.content}
          </p>
          <p className="text-[11px] text-[#475569]">
            {formatDate(insight.generated_at)}
          </p>
        </div>
      </div>
    </motion.div>
  );
}
