"use client";

import { useEffect, useState, Suspense } from "react";
import { useSearchParams } from "next/navigation";
import { AgentPanel } from "@/components/agent/AgentPanel";
import { motion } from "framer-motion";
import { Bot, Zap, Brain, Target, TrendingUp, Calendar } from "lucide-react";

const agentCards = [
  {
    id: "morning_commander",
    name: "Morning Commander",
    icon: "🌅",
    description: "Plans your day intelligently based on tasks, goals, and energy",
    color: "#8B5CF6",
    example: "Plan my day. I have a team meeting at 2pm and low energy this morning.",
  },
  {
    id: "priority_rebalancer",
    name: "Priority Rebalancer",
    icon: "⚡",
    description: "Rearranges your schedule when urgent tasks appear",
    color: "#F59E0B",
    example: "My client just moved their deadline to tomorrow. Reprioritize everything.",
  },
  {
    id: "goal_analyst",
    name: "Goal Health Analyst",
    icon: "🎯",
    description: "Analyzes goal progress and suggests recovery actions",
    color: "#06B6D4",
    example: "Which of my goals are in danger?",
  },
  {
    id: "pattern_engine",
    name: "Pattern Intelligence",
    icon: "🧠",
    description: "Discovers your productivity patterns",
    color: "#10B981",
    example: "When should I schedule my deep work blocks?",
  },
  {
    id: "weekly_planner",
    name: "Weekly Planner",
    icon: "📅",
    description: "Generates balanced 5-day schedules",
    color: "#F43F5E",
    example: "Plan my next week.",
  },
];

function AgentPageContent() {
  const searchParams = useSearchParams();
  const [isAgentRunning, setIsAgentRunning] = useState(false);
  const [initialCommand, setInitialCommand] = useState<string | null>(null);

  useEffect(() => {
    const cmd = searchParams.get("cmd");
    if (cmd) {
      setInitialCommand(cmd);
    }
  }, [searchParams]);

  return (
    <div className="max-w-7xl mx-auto h-full">
      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6 h-[calc(100vh-8rem)]">
        {/* Left: Agent info */}
        <div className="lg:col-span-1 space-y-4 overflow-y-auto">
          <div>
            <h1 className="text-lg font-semibold text-[#F8FAFC] mb-1">
              Agent Workspace
            </h1>
            <p className="text-xs text-[#94A3B8]">
              5 specialized agents powered by Gemini + MongoDB
            </p>
          </div>

          {/* Agent cards */}
          <div className="space-y-2">
            {agentCards.map((agent, i) => (
              <motion.div
                key={agent.id}
                initial={{ opacity: 0, x: -10 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: i * 0.07 }}
                className="card p-3 hover:border-[rgba(139,92,246,0.2)] transition-all duration-200 cursor-pointer group"
              >
                <div className="flex items-center gap-2 mb-1">
                  <span className="text-base">{agent.icon}</span>
                  <span className="text-xs font-semibold text-[#F8FAFC] group-hover:text-[#8B5CF6] transition-colors">
                    {agent.name}
                  </span>
                </div>
                <p className="text-[11px] text-[#475569] leading-relaxed mb-2">
                  {agent.description}
                </p>
                <p className="text-[10px] text-[#8B5CF6] italic">
                  &quot;{agent.example}&quot;
                </p>
              </motion.div>
            ))}
          </div>

          {/* Architecture note */}
          <div className="card p-3 bg-[rgba(0,237,100,0.04)] border-[rgba(0,237,100,0.15)]">
            <p className="text-[11px] text-[#94A3B8] leading-relaxed">
              <span className="text-[#00ED64] font-semibold">MongoDB MCP</span> — All
              agent reads and writes go through the MongoDB Atlas MCP Server, creating
              persistent operational memory.
            </p>
          </div>
        </div>

        {/* Right: Agent panel */}
        <div className="lg:col-span-3 h-full">
          <AgentPanel
            onAgentStateChange={setIsAgentRunning}
          />
        </div>
      </div>
    </div>
  );
}

export default function AgentPage() {
  return (
    <Suspense fallback={
      <div className="flex items-center justify-center h-64">
        <div className="w-8 h-8 border-2 border-[#8B5CF6] border-t-transparent rounded-full animate-spin" />
      </div>
    }>
      <AgentPageContent />
    </Suspense>
  );
}
