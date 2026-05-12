"use client";

import { useEffect, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Insight } from "@/lib/types";
import { insightsAPI } from "@/lib/api";
import { InsightCard } from "@/components/dashboard/InsightCard";
import { getUserId } from "@/lib/utils";
import { Lightbulb, TrendingUp, BarChart2 } from "lucide-react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  Cell,
} from "recharts";

// Heatmap data generator (last 12 weeks)
function generateHeatmapData() {
  const data = [];
  const today = new Date();
  for (let i = 83; i >= 0; i--) {
    const date = new Date(today);
    date.setDate(date.getDate() - i);
    const dayOfWeek = date.getDay();
    // Skip weekends for work data
    const completions = dayOfWeek === 0 || dayOfWeek === 6
      ? 0
      : Math.floor(Math.random() * 8);
    data.push({
      date: date.toISOString().split("T")[0],
      completions,
      dayOfWeek,
    });
  }
  return data;
}

const weeklyData = [
  { day: "Mon", score: 78, tasks: 8 },
  { day: "Tue", score: 92, tasks: 11 },
  { day: "Wed", score: 85, tasks: 9 },
  { day: "Thu", score: 80, tasks: 8 },
  { day: "Fri", score: 65, tasks: 6 },
];

const hourlyData = [
  { hour: "6am", score: 45 },
  { hour: "7am", score: 60 },
  { hour: "8am", score: 72 },
  { hour: "9am", score: 92 },
  { hour: "10am", score: 95 },
  { hour: "11am", score: 88 },
  { hour: "12pm", score: 55 },
  { hour: "1pm", score: 48 },
  { hour: "2pm", score: 65 },
  { hour: "3pm", score: 70 },
  { hour: "4pm", score: 62 },
  { hour: "5pm", score: 45 },
];

function HeatmapCell({ completions }: { completions: number }) {
  const getColor = (n: number) => {
    if (n === 0) return "rgba(148, 163, 184, 0.08)";
    if (n <= 2) return "rgba(139, 92, 246, 0.2)";
    if (n <= 4) return "rgba(139, 92, 246, 0.45)";
    if (n <= 6) return "rgba(139, 92, 246, 0.7)";
    return "#8B5CF6";
  };

  return (
    <div
      className="heatmap-cell w-3 h-3 rounded-sm"
      style={{ background: getColor(completions) }}
      title={`${completions} tasks completed`}
    />
  );
}

export default function InsightsPage() {
  const [insights, setInsights] = useState<Insight[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [heatmapData] = useState(generateHeatmapData);

  const userId = getUserId();

  const loadInsights = async () => {
    try {
      const res = await insightsAPI.getAll(userId);
      setInsights(res.insights);
    } catch {
      console.error("Failed to load insights");
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    loadInsights();
  }, []);

  // Group heatmap data into weeks
  const weeks: typeof heatmapData[] = [];
  for (let i = 0; i < heatmapData.length; i += 7) {
    weeks.push(heatmapData.slice(i, i + 7));
  }

  return (
    <div className="max-w-5xl mx-auto space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-xl font-semibold text-[#F8FAFC]">Pattern Insights</h1>
        <p className="text-sm text-[#94A3B8] mt-0.5">
          AI-generated insights from your productivity patterns
        </p>
      </div>

      {/* Charts row */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Activity Heatmap */}
        <div className="card p-5">
          <div className="flex items-center gap-2 mb-4">
            <BarChart2 size={16} className="text-[#8B5CF6]" />
            <h2 className="text-sm font-semibold text-[#F8FAFC]">
              Task Completion Heatmap
            </h2>
          </div>
          <p className="text-xs text-[#475569] mb-4">Last 12 weeks</p>

          <div className="flex gap-1 overflow-x-auto pb-2">
            {weeks.map((week, wi) => (
              <div key={wi} className="flex flex-col gap-1">
                {week.map((day, di) => (
                  <HeatmapCell key={di} completions={day.completions} />
                ))}
              </div>
            ))}
          </div>

          <div className="flex items-center gap-2 mt-3">
            <span className="text-[11px] text-[#475569]">Less</span>
            {[0, 2, 4, 6, 8].map((n) => (
              <HeatmapCell key={n} completions={n} />
            ))}
            <span className="text-[11px] text-[#475569]">More</span>
          </div>
        </div>

        {/* Peak Hours */}
        <div className="card p-5">
          <div className="flex items-center gap-2 mb-4">
            <TrendingUp size={16} className="text-[#06B6D4]" />
            <h2 className="text-sm font-semibold text-[#F8FAFC]">
              Peak Productivity Hours
            </h2>
          </div>

          <ResponsiveContainer width="100%" height={160}>
            <BarChart data={hourlyData} margin={{ top: 0, right: 0, left: -20, bottom: 0 }}>
              <XAxis
                dataKey="hour"
                tick={{ fill: "#475569", fontSize: 10 }}
                axisLine={false}
                tickLine={false}
              />
              <YAxis hide />
              <Tooltip
                contentStyle={{
                  background: "#1E293B",
                  border: "1px solid rgba(148,163,184,0.12)",
                  borderRadius: "8px",
                  fontSize: "12px",
                  color: "#F8FAFC",
                }}
                cursor={{ fill: "rgba(148,163,184,0.05)" }}
              />
              <Bar dataKey="score" radius={[3, 3, 0, 0]}>
                {hourlyData.map((entry, index) => (
                  <Cell
                    key={index}
                    fill={entry.score >= 85 ? "#8B5CF6" : entry.score >= 65 ? "#06B6D4" : "rgba(148,163,184,0.2)"}
                  />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>

          <p className="text-xs text-[#94A3B8] mt-2">
            🔥 Peak window: <span className="text-[#8B5CF6] font-medium">9am–11am</span> (92% completion rate)
          </p>
        </div>
      </div>

      {/* Weekly pattern */}
      <div className="card p-5">
        <div className="flex items-center gap-2 mb-4">
          <BarChart2 size={16} className="text-[#10B981]" />
          <h2 className="text-sm font-semibold text-[#F8FAFC]">
            Weekly Productivity Pattern
          </h2>
        </div>

        <ResponsiveContainer width="100%" height={140}>
          <BarChart data={weeklyData} margin={{ top: 0, right: 0, left: -20, bottom: 0 }}>
            <XAxis
              dataKey="day"
              tick={{ fill: "#475569", fontSize: 11 }}
              axisLine={false}
              tickLine={false}
            />
            <YAxis hide />
            <Tooltip
              contentStyle={{
                background: "#1E293B",
                border: "1px solid rgba(148,163,184,0.12)",
                borderRadius: "8px",
                fontSize: "12px",
                color: "#F8FAFC",
              }}
              cursor={{ fill: "rgba(148,163,184,0.05)" }}
            />
            <Bar dataKey="score" radius={[4, 4, 0, 0]}>
              {weeklyData.map((entry, index) => (
                <Cell
                  key={index}
                  fill={entry.score >= 85 ? "#10B981" : entry.score >= 70 ? "#06B6D4" : "rgba(148,163,184,0.2)"}
                />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>

        <div className="flex items-center gap-4 mt-2 text-xs text-[#475569]">
          <span>🏆 Best day: <span className="text-[#10B981]">Tuesday (92%)</span></span>
          <span>📉 Lowest: <span className="text-[#F59E0B]">Friday (65%)</span></span>
        </div>
      </div>

      {/* AI Insights */}
      <div>
        <div className="flex items-center gap-2 mb-4">
          <Lightbulb size={16} className="text-[#F59E0B]" />
          <h2 className="text-sm font-semibold text-[#F8FAFC]">
            AI-Generated Insights
          </h2>
          <span className="text-xs text-[#475569] bg-[rgba(148,163,184,0.06)] px-2 py-0.5 rounded-full">
            {insights.filter((i) => !i.acknowledged).length} unread
          </span>
        </div>

        {isLoading ? (
          <div className="space-y-3">
            {[...Array(3)].map((_, i) => (
              <div key={i} className="h-20 bg-[rgba(148,163,184,0.06)] rounded-xl animate-pulse" />
            ))}
          </div>
        ) : insights.length > 0 ? (
          <div className="space-y-3">
            <AnimatePresence>
              {insights.map((insight) => (
                <InsightCard
                  key={insight._id}
                  insight={insight}
                  onAcknowledge={loadInsights}
                />
              ))}
            </AnimatePresence>
          </div>
        ) : (
          <div className="card p-8 text-center">
            <Lightbulb size={32} className="text-[#475569] mx-auto mb-3" />
            <p className="text-sm text-[#94A3B8]">No insights yet</p>
            <p className="text-xs text-[#475569] mt-1">
              Run the Pattern Intelligence agent to generate insights
            </p>
          </div>
        )}
      </div>
    </div>
  );
}
