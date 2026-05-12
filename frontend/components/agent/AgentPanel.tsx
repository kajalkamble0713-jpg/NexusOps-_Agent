"use client";

import { useState, useCallback } from "react";
import { motion } from "framer-motion";
import { AgentStep, AgentType } from "@/lib/types";
import { agentAPI } from "@/lib/api";
import { AgentActivityFeed } from "./AgentActivityFeed";
import { AgentPromptBar } from "./AgentPromptBar";
import { getUserId } from "@/lib/utils";
import { Trash2, Download } from "lucide-react";
import toast from "react-hot-toast";

interface AgentPanelProps {
  onAgentStateChange?: (isRunning: boolean) => void;
  compact?: boolean;
}

export function AgentPanel({ onAgentStateChange, compact = false }: AgentPanelProps) {
  const [steps, setSteps] = useState<AgentStep[]>([]);
  const [isRunning, setIsRunning] = useState(false);
  const [sessionCount, setSessionCount] = useState(0);

  const invokeAgent = useCallback(
    async (input: string, agentType?: string) => {
      if (isRunning) return;

      setIsRunning(true);
      onAgentStateChange?.(true);
      setSteps([]);
      setSessionCount((c) => c + 1);

      const userId = getUserId();

      await agentAPI.invoke(
        {
          user_id: userId,
          input,
          agent_type: agentType as AgentType | undefined,
        },
        (step) => {
          setSteps((prev) => [...prev, step]);
        },
        () => {
          setIsRunning(false);
          onAgentStateChange?.(false);
          toast.success("Agent completed successfully");
        },
        (error) => {
          setIsRunning(false);
          onAgentStateChange?.(false);
          toast.error(`Agent error: ${error.message}`);
          setSteps((prev) => [
            ...prev,
            {
              type: "error",
              content: `Connection error: ${error.message}. Make sure the backend is running.`,
              timestamp: new Date().toISOString(),
              metadata: {},
            },
          ]);
        }
      );
    },
    [isRunning, onAgentStateChange]
  );

  const clearSession = () => {
    if (isRunning) return;
    setSteps([]);
  };

  const exportSession = () => {
    const content = steps
      .map((s) => `[${s.type.toUpperCase()}] ${s.content}`)
      .join("\n\n");
    const blob = new Blob([content], { type: "text/plain" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `nexusops-session-${Date.now()}.txt`;
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div
      className={`flex flex-col h-full ${
        isRunning ? "agent-panel-active" : "card"
      } overflow-hidden`}
    >
      {/* Header */}
      <div className="flex items-center justify-between px-4 py-3 border-b border-[rgba(148,163,184,0.12)]">
        <div className="flex items-center gap-3">
          <div
            className={`w-2 h-2 rounded-full ${
              isRunning ? "bg-[#8B5CF6] animate-pulse" : "bg-[#475569]"
            }`}
          />
          <span className="text-sm font-semibold text-[#F8FAFC]">
            Agent Workspace
          </span>
          {sessionCount > 0 && (
            <span className="text-xs text-[#475569] bg-[rgba(148,163,184,0.06)] px-2 py-0.5 rounded-full">
              Session #{sessionCount}
            </span>
          )}
        </div>

        <div className="flex items-center gap-1">
          {steps.length > 0 && (
            <>
              <button
                onClick={exportSession}
                className="p-1.5 rounded-lg text-[#475569] hover:text-[#94A3B8] hover:bg-[rgba(148,163,184,0.06)] transition-all"
                title="Export session"
              >
                <Download size={14} />
              </button>
              <button
                onClick={clearSession}
                disabled={isRunning}
                className="p-1.5 rounded-lg text-[#475569] hover:text-[#F43F5E] hover:bg-[rgba(244,63,94,0.06)] transition-all disabled:opacity-40"
                title="Clear session"
              >
                <Trash2 size={14} />
              </button>
            </>
          )}
        </div>
      </div>

      {/* Steps feed */}
      <div className="flex-1 overflow-y-auto px-4 py-2">
        <AgentActivityFeed steps={steps} isRunning={isRunning} />
      </div>

      {/* Prompt bar */}
      <AgentPromptBar onSubmit={invokeAgent} isRunning={isRunning} />
    </div>
  );
}
