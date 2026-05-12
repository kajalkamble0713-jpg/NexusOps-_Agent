"use client";

import { motion, AnimatePresence } from "framer-motion";
import { Bot } from "lucide-react";

interface AgentStatusIndicatorProps {
  isRunning: boolean;
}

export function AgentStatusIndicator({ isRunning }: AgentStatusIndicatorProps) {
  return (
    <div className="flex items-center gap-2">
      <AnimatePresence mode="wait">
        {isRunning ? (
          <motion.div
            key="running"
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: 1, scale: 1 }}
            exit={{ opacity: 0, scale: 0.8 }}
            className="flex items-center gap-2 bg-[rgba(139,92,246,0.1)] border border-[rgba(139,92,246,0.3)] rounded-full px-3 py-1.5"
          >
            {/* Pulsing ring */}
            <div className="relative flex items-center justify-center">
              <motion.div
                animate={{ scale: [1, 1.5, 1], opacity: [0.7, 0, 0.7] }}
                transition={{ duration: 1.5, repeat: Infinity }}
                className="absolute w-4 h-4 rounded-full bg-[#8B5CF6]"
              />
              <div className="w-2 h-2 rounded-full bg-[#8B5CF6]" />
            </div>
            <span className="text-xs font-medium text-[#8B5CF6]">Agent thinking...</span>
            {/* Thinking dots */}
            <div className="flex gap-0.5">
              {[0, 1, 2].map((i) => (
                <motion.div
                  key={i}
                  animate={{ scale: [0.8, 1.2, 0.8], opacity: [0.5, 1, 0.5] }}
                  transition={{ duration: 1.4, repeat: Infinity, delay: i * 0.2 }}
                  className="w-1 h-1 rounded-full bg-[#8B5CF6]"
                />
              ))}
            </div>
          </motion.div>
        ) : (
          <motion.div
            key="idle"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="flex items-center gap-2 text-[#475569]"
          >
            <Bot size={14} />
            <span className="text-xs">Agent ready</span>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
