"use client";

import { useEffect, useRef } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { AgentStep } from "@/lib/types";
import { AgentStepCard } from "./AgentStepCard";
import { Bot } from "lucide-react";

interface AgentActivityFeedProps {
  steps: AgentStep[];
  isRunning: boolean;
}

export function AgentActivityFeed({ steps, isRunning }: AgentActivityFeedProps) {
  const bottomRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to bottom as steps come in
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [steps]);

  if (steps.length === 0 && !isRunning) {
    return (
      <div className="flex flex-col items-center justify-center h-full text-center py-16">
        <div className="w-16 h-16 rounded-2xl bg-[rgba(139,92,246,0.1)] border border-[rgba(139,92,246,0.2)] flex items-center justify-center mb-4">
          <Bot size={28} className="text-[#8B5CF6]" />
        </div>
        <h3 className="text-base font-semibold text-[#F8FAFC] mb-2">
          Agent ready
        </h3>
        <p className="text-sm text-[#94A3B8] max-w-xs">
          Type a command below to invoke an agent. Try &quot;Plan my day&quot; or &quot;Review my goals&quot;.
        </p>
        <div className="mt-6 grid grid-cols-2 gap-2 w-full max-w-sm">
          {[
            "Plan my day",
            "Review my goals",
            "Show me how I work",
            "Plan next week",
          ].map((suggestion) => (
            <button
              key={suggestion}
              className="text-xs text-[#94A3B8] bg-[rgba(148,163,184,0.06)] hover:bg-[rgba(148,163,184,0.1)] border border-[rgba(148,163,184,0.12)] rounded-lg px-3 py-2 text-left transition-all duration-150 hover:text-[#F8FAFC]"
            >
              {suggestion}
            </button>
          ))}
        </div>
      </div>
    );
  }

  return (
    <div className="flex flex-col gap-1 py-2">
      <AnimatePresence>
        {steps.map((step, index) => (
          <AgentStepCard
            key={`${step.timestamp}-${index}`}
            step={step}
            index={index}
            isLast={index === steps.length - 1 && !isRunning}
          />
        ))}
      </AnimatePresence>

      {/* Thinking indicator */}
      {isRunning && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="flex items-center gap-3 px-2 py-2"
        >
          <div className="w-9 h-9 rounded-full bg-[rgba(139,92,246,0.1)] border border-[rgba(139,92,246,0.2)] flex items-center justify-center">
            <div className="flex gap-0.5">
              {[0, 1, 2].map((i) => (
                <motion.div
                  key={i}
                  animate={{ scale: [0.8, 1.3, 0.8], opacity: [0.4, 1, 0.4] }}
                  transition={{ duration: 1.2, repeat: Infinity, delay: i * 0.15 }}
                  className="w-1 h-1 rounded-full bg-[#8B5CF6]"
                />
              ))}
            </div>
          </div>
          <span className="text-sm text-[#475569] italic">Agent is working...</span>
        </motion.div>
      )}

      <div ref={bottomRef} />
    </div>
  );
}
