"use client";

import { useState, useRef, KeyboardEvent } from "react";
import { motion } from "framer-motion";
import { Send, Sparkles } from "lucide-react";
import { cn } from "@/lib/utils";

interface AgentPromptBarProps {
  onSubmit: (input: string, agentType?: string) => void;
  isRunning: boolean;
  placeholder?: string;
}

const quickCommands = [
  { label: "Plan my day", agentType: "morning_commander" },
  { label: "Urgent task", agentType: "priority_rebalancer" },
  { label: "Goal health", agentType: "goal_analyst" },
  { label: "My patterns", agentType: "pattern_engine" },
  { label: "Plan next week", agentType: "weekly_planner" },
];

export function AgentPromptBar({
  onSubmit,
  isRunning,
  placeholder = "Ask your agent anything... Try 'Plan my day' or 'Which goals are at risk?'",
}: AgentPromptBarProps) {
  const [input, setInput] = useState("");
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  const handleSubmit = () => {
    const trimmed = input.trim();
    if (!trimmed || isRunning) return;
    onSubmit(trimmed);
    setInput("");
    if (textareaRef.current) {
      textareaRef.current.style.height = "auto";
    }
  };

  const handleKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  const handleInput = () => {
    const textarea = textareaRef.current;
    if (textarea) {
      textarea.style.height = "auto";
      textarea.style.height = Math.min(textarea.scrollHeight, 120) + "px";
    }
  };

  return (
    <div className="border-t border-[rgba(148,163,184,0.12)] bg-[#1E293B] p-4">
      {/* Quick commands */}
      <div className="flex items-center gap-2 mb-3 overflow-x-auto pb-1">
        <Sparkles size={12} className="text-[#8B5CF6] flex-shrink-0" />
        {quickCommands.map((cmd) => (
          <button
            key={cmd.label}
            onClick={() => onSubmit(cmd.label, cmd.agentType)}
            disabled={isRunning}
            className="flex-shrink-0 text-xs text-[#94A3B8] hover:text-[#F8FAFC] bg-[rgba(148,163,184,0.06)] hover:bg-[rgba(148,163,184,0.1)] border border-[rgba(148,163,184,0.12)] hover:border-[rgba(139,92,246,0.3)] rounded-full px-3 py-1 transition-all duration-150 disabled:opacity-40 disabled:cursor-not-allowed"
          >
            {cmd.label}
          </button>
        ))}
      </div>

      {/* Input area */}
      <div
        className={cn(
          "flex items-end gap-3 bg-[rgba(148,163,184,0.04)] border rounded-xl p-3 transition-all duration-200",
          isRunning
            ? "border-[rgba(139,92,246,0.3)] bg-[rgba(139,92,246,0.04)]"
            : "border-[rgba(148,163,184,0.12)] focus-within:border-[rgba(139,92,246,0.4)]"
        )}
      >
        <textarea
          ref={textareaRef}
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          onInput={handleInput}
          placeholder={isRunning ? "Agent is working..." : placeholder}
          disabled={isRunning}
          rows={1}
          className="flex-1 bg-transparent text-sm text-[#F8FAFC] placeholder-[#475569] resize-none outline-none leading-relaxed disabled:opacity-50"
          style={{ maxHeight: "120px" }}
        />

        <motion.button
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          onClick={handleSubmit}
          disabled={!input.trim() || isRunning}
          className={cn(
            "flex-shrink-0 w-9 h-9 rounded-lg flex items-center justify-center transition-all duration-200",
            input.trim() && !isRunning
              ? "bg-[#8B5CF6] hover:bg-[#7C3AED] text-white shadow-[0_0_12px_rgba(139,92,246,0.4)]"
              : "bg-[rgba(148,163,184,0.08)] text-[#475569] cursor-not-allowed"
          )}
        >
          {isRunning ? (
            <div className="w-4 h-4 border-2 border-[#475569] border-t-[#8B5CF6] rounded-full animate-spin" />
          ) : (
            <Send size={15} />
          )}
        </motion.button>
      </div>

      <p className="text-[11px] text-[#475569] mt-2 text-center">
        Press Enter to send · Shift+Enter for new line
      </p>
    </div>
  );
}
