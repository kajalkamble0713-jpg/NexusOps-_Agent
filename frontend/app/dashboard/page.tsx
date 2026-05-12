"use client";

import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { tasksAPI, goalsAPI, habitsAPI, insightsAPI } from "@/lib/api";
import { Task, Goal, Habit, Insight, DailyPlan } from "@/lib/types";
import { getUserId } from "@/lib/utils";
import { DailyPlanView } from "@/components/dashboard/DailyPlanView";
import { GoalHealthCard } from "@/components/dashboard/GoalHealthCard";
import { HabitGrid } from "@/components/dashboard/HabitGrid";
import { InsightCard } from "@/components/dashboard/InsightCard";
import { AgentPanel } from "@/components/agent/AgentPanel";
import {
  CheckSquare,
  Target,
  Repeat2,
  TrendingUp,
  Bot,
  ArrowRight,
} from "lucide-react";
import Link from "next/link";

export default function DashboardPage() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [goals, setGoals] = useState<Goal[]>([]);
  const [habits, setHabits] = useState<Habit[]>([]);
  const [insights, setInsights] = useState<Insight[]>([]);
  const [dailyPlan, setDailyPlan] = useState<DailyPlan | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [isAgentRunning, setIsAgentRunning] = useState(false);

  const userId = getUserId();

  const loadData = async () => {
    try {
      const [tasksRes, goalsRes, habitsRes, insightsRes, planRes] =
        await Promise.allSettled([
          tasksAPI.getAll(userId),
          goalsAPI.getAll(userId),
          habitsAPI.getAll(userId),
          insightsAPI.getAll(userId, undefined, false),
          insightsAPI.getDailyPlan(userId),
        ]);

      if (tasksRes.status === "fulfilled") setTasks(tasksRes.value.tasks);
      if (goalsRes.status === "fulfilled") setGoals(goalsRes.value.goals);
      if (habitsRes.status === "fulfilled") setHabits(habitsRes.value.habits);
      if (insightsRes.status === "fulfilled")
        setInsights(insightsRes.value.insights);
      if (planRes.status === "fulfilled" && planRes.value.plan)
        setDailyPlan(planRes.value.plan as DailyPlan);
    } catch (error) {
      console.error("Failed to load dashboard data:", error);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const todayTasks = tasks.filter(
    (t) => t.status === "today" || t.status === "in_progress"
  );
  const completedToday = tasks.filter((t) => t.status === "done").length;
  const activeGoals = goals.filter((g) => g.current_progress < 100);

  const stats = [
    {
      label: "Tasks Today",
      value: todayTasks.length,
      icon: CheckSquare,
      color: "#8B5CF6",
      href: "/dashboard/tasks",
    },
    {
      label: "Active Goals",
      value: activeGoals.length,
      icon: Target,
      color: "#06B6D4",
      href: "/dashboard/goals",
    },
    {
      label: "Habit Streaks",
      value: habits.reduce((sum, h) => sum + h.streak_count, 0),
      icon: Repeat2,
      color: "#10B981",
      href: "/dashboard/habits",
    },
    {
      label: "Completed Today",
      value: completedToday,
      icon: TrendingUp,
      color: "#F59E0B",
      href: "/dashboard/tasks",
    },
  ];

  return (
    <div className="max-w-7xl mx-auto space-y-6">
      {/* Stats row */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        {stats.map((stat, i) => {
          const Icon = stat.icon;
          return (
            <motion.div
              key={stat.label}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.07 }}
            >
              <Link href={stat.href}>
                <div className="card p-4 hover:border-[rgba(139,92,246,0.2)] transition-all duration-200 cursor-pointer group">
                  <div className="flex items-center justify-between mb-3">
                    <div
                      className="w-9 h-9 rounded-xl flex items-center justify-center"
                      style={{ background: `${stat.color}15` }}
                    >
                      <Icon size={18} style={{ color: stat.color }} />
                    </div>
                    <ArrowRight
                      size={14}
                      className="text-[#475569] group-hover:text-[#94A3B8] transition-colors"
                    />
                  </div>
                  <div className="text-2xl font-bold text-[#F8FAFC] mb-1">
                    {isLoading ? (
                      <div className="h-7 w-12 bg-[rgba(148,163,184,0.1)] rounded animate-pulse" />
                    ) : (
                      stat.value
                    )}
                  </div>
                  <div className="text-xs text-[#94A3B8]">{stat.label}</div>
                </div>
              </Link>
            </motion.div>
          );
        })}
      </div>

      {/* Main grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left: Daily Plan */}
        <div className="lg:col-span-1">
          <div className="card p-5 h-full">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-sm font-semibold text-[#F8FAFC]">
                Today&apos;s Plan
              </h2>
              <Link
                href="/dashboard/agent"
                className="text-xs text-[#8B5CF6] hover:text-[#A78BFA] flex items-center gap-1 transition-colors"
              >
                <Bot size={12} />
                Plan with AI
              </Link>
            </div>
            <DailyPlanView plan={dailyPlan} isLoading={isLoading} />
          </div>
        </div>

        {/* Center: Goals */}
        <div className="lg:col-span-1">
          <div className="h-full">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-sm font-semibold text-[#F8FAFC]">
                Goal Health
              </h2>
              <Link
                href="/dashboard/goals"
                className="text-xs text-[#94A3B8] hover:text-[#F8FAFC] flex items-center gap-1 transition-colors"
              >
                View all
                <ArrowRight size={12} />
              </Link>
            </div>
            <div className="space-y-3">
              {isLoading ? (
                [...Array(2)].map((_, i) => (
                  <div
                    key={i}
                    className="h-32 bg-[rgba(148,163,184,0.06)] rounded-xl animate-pulse"
                  />
                ))
              ) : activeGoals.length > 0 ? (
                activeGoals.slice(0, 2).map((goal) => (
                  <GoalHealthCard key={goal._id} goal={goal} />
                ))
              ) : (
                <div className="card p-6 text-center">
                  <Target size={24} className="text-[#475569] mx-auto mb-2" />
                  <p className="text-sm text-[#94A3B8]">No active goals</p>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Right: Agent + Habits + Insights */}
        <div className="lg:col-span-1 space-y-4">
          {/* Quick Agent */}
          <div className="card p-4">
            <div className="flex items-center justify-between mb-3">
              <h2 className="text-sm font-semibold text-[#F8FAFC]">
                Quick Agent
              </h2>
              <Link
                href="/dashboard/agent"
                className="text-xs text-[#8B5CF6] hover:text-[#A78BFA] flex items-center gap-1 transition-colors"
              >
                Full workspace
                <ArrowRight size={12} />
              </Link>
            </div>
            <div className="grid grid-cols-2 gap-2">
              {[
                { label: "🌅 Plan my day", type: "morning_commander" },
                { label: "⚡ Urgent task", type: "priority_rebalancer" },
                { label: "🎯 Goal health", type: "goal_analyst" },
                { label: "🧠 My patterns", type: "pattern_engine" },
              ].map((cmd) => (
                <Link key={cmd.label} href={`/dashboard/agent?cmd=${encodeURIComponent(cmd.label)}&type=${cmd.type}`}>
                  <button className="w-full text-xs text-[#94A3B8] hover:text-[#F8FAFC] bg-[rgba(148,163,184,0.04)] hover:bg-[rgba(148,163,184,0.08)] border border-[rgba(148,163,184,0.1)] hover:border-[rgba(139,92,246,0.3)] rounded-lg px-3 py-2.5 text-left transition-all duration-150">
                    {cmd.label}
                  </button>
                </Link>
              ))}
            </div>
          </div>

          {/* Habits */}
          <div className="card p-4">
            <div className="flex items-center justify-between mb-3">
              <h2 className="text-sm font-semibold text-[#F8FAFC]">
                Today&apos;s Habits
              </h2>
              <Link
                href="/dashboard/habits"
                className="text-xs text-[#94A3B8] hover:text-[#F8FAFC] transition-colors"
              >
                View all
              </Link>
            </div>
            {isLoading ? (
              <div className="space-y-2">
                {[...Array(3)].map((_, i) => (
                  <div
                    key={i}
                    className="h-10 bg-[rgba(148,163,184,0.06)] rounded-lg animate-pulse"
                  />
                ))}
              </div>
            ) : (
              <HabitGrid habits={habits.slice(0, 4)} onUpdate={loadData} />
            )}
          </div>

          {/* Insights */}
          {insights.length > 0 && (
            <div className="card p-4">
              <div className="flex items-center justify-between mb-3">
                <h2 className="text-sm font-semibold text-[#F8FAFC]">
                  Latest Insights
                </h2>
                <Link
                  href="/dashboard/insights"
                  className="text-xs text-[#94A3B8] hover:text-[#F8FAFC] transition-colors"
                >
                  View all
                </Link>
              </div>
              <div className="space-y-2">
                {insights.slice(0, 2).map((insight) => (
                  <InsightCard
                    key={insight._id}
                    insight={insight}
                    onAcknowledge={loadData}
                  />
                ))}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
