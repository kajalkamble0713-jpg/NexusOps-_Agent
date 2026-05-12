"use client";

import { motion } from "framer-motion";
import { Habit } from "@/lib/types";
import { habitsAPI } from "@/lib/api";
import { Flame, Check } from "lucide-react";
import { cn } from "@/lib/utils";
import toast from "react-hot-toast";
import { useState } from "react";

interface HabitGridProps {
  habits: Habit[];
  onUpdate?: () => void;
}

const categoryColors: Record<string, string> = {
  health: "#10B981",
  productivity: "#8B5CF6",
  learning: "#06B6D4",
  wellness: "#F59E0B",
};

export function HabitGrid({ habits, onUpdate }: HabitGridProps) {
  const [completing, setCompleting] = useState<string | null>(null);

  const isCompletedToday = (habit: Habit): boolean => {
    const today = new Date().toISOString().split("T")[0];
    return habit.completion_log.some((log) => log.startsWith(today));
  };

  const handleComplete = async (habit: Habit) => {
    if (completing || isCompletedToday(habit)) return;

    setCompleting(habit._id);
    try {
      const result = await habitsAPI.complete(habit._id);
      toast.success(`🔥 ${habit.name} — ${result.streak} day streak!`);
      onUpdate?.();
    } catch (error) {
      toast.error("Failed to complete habit");
    } finally {
      setCompleting(null);
    }
  };

  if (habits.length === 0) {
    return (
      <div className="text-center py-8 text-[#475569] text-sm">
        No habits yet. Add your first habit to start tracking.
      </div>
    );
  }

  return (
    <div className="space-y-2">
      {habits.map((habit, i) => {
        const completed = isCompletedToday(habit);
        const color = categoryColors[habit.category] || "#8B5CF6";

        return (
          <motion.div
            key={habit._id}
            initial={{ opacity: 0, x: -10 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: i * 0.05 }}
            className={cn(
              "flex items-center gap-3 p-3 rounded-xl border transition-all duration-200",
              completed
                ? "bg-[rgba(16,185,129,0.06)] border-[rgba(16,185,129,0.2)]"
                : "bg-[rgba(148,163,184,0.03)] border-[rgba(148,163,184,0.1)] hover:border-[rgba(148,163,184,0.2)]"
            )}
          >
            {/* Complete button */}
            <button
              onClick={() => handleComplete(habit)}
              disabled={completed || completing === habit._id}
              className={cn(
                "w-7 h-7 rounded-full border-2 flex items-center justify-center flex-shrink-0 transition-all duration-200",
                completed
                  ? "bg-[#10B981] border-[#10B981]"
                  : "border-[rgba(148,163,184,0.3)] hover:border-[#10B981]"
              )}
            >
              {completing === habit._id ? (
                <div className="w-3 h-3 border border-[#10B981] border-t-transparent rounded-full animate-spin" />
              ) : completed ? (
                <Check size={13} className="text-white" />
              ) : null}
            </button>

            {/* Habit info */}
            <div className="flex-1 min-w-0">
              <p
                className={cn(
                  "text-sm font-medium truncate",
                  completed ? "text-[#94A3B8] line-through" : "text-[#F8FAFC]"
                )}
              >
                {habit.name}
              </p>
              <p className="text-[11px] text-[#475569] capitalize">{habit.category}</p>
            </div>

            {/* Streak */}
            <div className="flex items-center gap-1 flex-shrink-0">
              <Flame
                size={13}
                className={habit.streak_count > 0 ? "text-[#F59E0B]" : "text-[#475569]"}
              />
              <span
                className={cn(
                  "text-xs font-semibold",
                  habit.streak_count > 0 ? "text-[#F59E0B]" : "text-[#475569]"
                )}
              >
                {habit.streak_count}
              </span>
            </div>
          </motion.div>
        );
      })}
    </div>
  );
}
