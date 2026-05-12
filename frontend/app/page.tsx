"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { motion } from "framer-motion";
import { userAPI } from "@/lib/api";

export default function LandingPage() {
  const router = useRouter();
  const [isLoading, setIsLoading] = useState(false);

  const handleEnterDemo = async () => {
    setIsLoading(true);
    try {
      const { user } = await userAPI.getDemoUser();
      // Store user ID in localStorage for demo
      localStorage.setItem("nexusops_user_id", user._id);
      localStorage.setItem("nexusops_user_name", user.name);
      router.push("/dashboard");
    } catch (error) {
      console.error("Failed to get demo user:", error);
      // Use a fallback demo ID
      localStorage.setItem("nexusops_user_id", "demo_user_001");
      localStorage.setItem("nexusops_user_name", "Alex Chen");
      router.push("/dashboard");
    } finally {
      setIsLoading(false);
    }
  };

  const features = [
    {
      icon: "🌅",
      title: "Morning Commander",
      description: "Autonomously plans your day based on tasks, goals, and energy levels",
    },
    {
      icon: "⚡",
      title: "Priority Rebalancer",
      description: "Intelligently rearranges your schedule when urgent tasks appear",
    },
    {
      icon: "🎯",
      title: "Goal Health Analyst",
      description: "Tracks goal progress and proactively suggests recovery actions",
    },
    {
      icon: "🧠",
      title: "Pattern Intelligence",
      description: "Discovers your productivity patterns and optimizes scheduling",
    },
    {
      icon: "📅",
      title: "Weekly Planner",
      description: "Generates balanced 5-day schedules with deep work blocks",
    },
  ];

  return (
    <div className="min-h-screen bg-[#0F172A] flex flex-col">
      {/* Header */}
      <header className="border-b border-[rgba(148,163,184,0.12)] px-6 py-4">
        <div className="max-w-6xl mx-auto flex items-center justify-between">
          <div className="flex items-center gap-3">
            <NexusLogo />
            <span className="text-lg font-semibold text-[#F8FAFC]">NexusOps</span>
          </div>
          <div className="flex items-center gap-3">
            <span className="text-xs text-[#94A3B8] bg-[#1E293B] border border-[rgba(148,163,184,0.12)] px-3 py-1 rounded-full">
              Google Cloud Rapid Agent Hackathon
            </span>
            <span className="text-xs text-[#00ED64] bg-[rgba(0,237,100,0.1)] border border-[rgba(0,237,100,0.2)] px-3 py-1 rounded-full">
              MongoDB Partner Track
            </span>
          </div>
        </div>
      </header>

      {/* Hero */}
      <main className="flex-1 flex flex-col items-center justify-center px-6 py-20">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="text-center max-w-3xl mx-auto"
        >
          {/* Badge */}
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.1 }}
            className="inline-flex items-center gap-2 bg-[rgba(139,92,246,0.1)] border border-[rgba(139,92,246,0.3)] rounded-full px-4 py-2 mb-8"
          >
            <span className="w-2 h-2 rounded-full bg-[#8B5CF6] animate-pulse" />
            <span className="text-sm text-[#8B5CF6] font-medium">
              AI-Powered Operations Intelligence
            </span>
          </motion.div>

          {/* Headline */}
          <h1 className="text-5xl font-bold text-[#F8FAFC] mb-6 leading-tight tracking-tight">
            Your life&apos;s operations center —{" "}
            <span className="gradient-text">intelligently automated.</span>
          </h1>

          <p className="text-lg text-[#94A3B8] mb-10 leading-relaxed max-w-2xl mx-auto">
            NexusOps Agent goes beyond task management. It autonomously plans your day,
            reroutes priorities when disruptions hit, and surfaces hidden patterns in how
            you work — powered by Gemini and MongoDB.
          </p>

          {/* CTA */}
          <div className="flex items-center justify-center gap-4">
            <motion.button
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              onClick={handleEnterDemo}
              disabled={isLoading}
              className="bg-[#8B5CF6] hover:bg-[#7C3AED] text-white font-semibold px-8 py-3.5 rounded-xl transition-all duration-200 shadow-[0_0_20px_rgba(139,92,246,0.3)] disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
            >
              {isLoading ? (
                <>
                  <span className="w-4 h-4 border-2 border-white/30 border-t-white rounded-full animate-spin" />
                  Loading...
                </>
              ) : (
                <>
                  Launch Demo
                  <span>→</span>
                </>
              )}
            </motion.button>
            <a
              href="https://github.com/yourusername/nexusops-agent"
              target="_blank"
              rel="noopener noreferrer"
              className="text-[#94A3B8] hover:text-[#F8FAFC] font-medium px-6 py-3.5 rounded-xl border border-[rgba(148,163,184,0.12)] hover:border-[rgba(148,163,184,0.3)] transition-all duration-200"
            >
              View on GitHub
            </a>
          </div>
        </motion.div>

        {/* Features Grid */}
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3, duration: 0.6 }}
          className="mt-20 grid grid-cols-1 md:grid-cols-3 lg:grid-cols-5 gap-4 max-w-5xl mx-auto w-full"
        >
          {features.map((feature, i) => (
            <motion.div
              key={feature.title}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.4 + i * 0.08 }}
              className="card p-5 hover:border-[rgba(139,92,246,0.3)] transition-all duration-200 group"
            >
              <div className="text-2xl mb-3">{feature.icon}</div>
              <h3 className="text-sm font-semibold text-[#F8FAFC] mb-2 group-hover:text-[#8B5CF6] transition-colors">
                {feature.title}
              </h3>
              <p className="text-xs text-[#94A3B8] leading-relaxed">
                {feature.description}
              </p>
            </motion.div>
          ))}
        </motion.div>

        {/* Tech Stack */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.8 }}
          className="mt-16 flex items-center gap-6 text-[#475569] text-sm"
        >
          <span>Built with</span>
          <div className="flex items-center gap-4">
            {["Gemini 2.0", "Google Cloud Agent Builder", "MongoDB Atlas", "Next.js 14"].map(
              (tech) => (
                <span
                  key={tech}
                  className="bg-[#1E293B] border border-[rgba(148,163,184,0.12)] px-3 py-1 rounded-full text-[#94A3B8] text-xs"
                >
                  {tech}
                </span>
              )
            )}
          </div>
        </motion.div>
      </main>
    </div>
  );
}

function NexusLogo() {
  return (
    <svg width="32" height="32" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg">
      <rect width="32" height="32" rx="8" fill="rgba(139, 92, 246, 0.15)" />
      <circle cx="8" cy="8" r="2.5" fill="#8B5CF6" />
      <circle cx="24" cy="8" r="2.5" fill="#06B6D4" />
      <circle cx="8" cy="24" r="2.5" fill="#06B6D4" />
      <circle cx="24" cy="24" r="2.5" fill="#8B5CF6" />
      <circle cx="16" cy="16" r="3" fill="#8B5CF6" />
      <line x1="8" y1="8" x2="16" y2="16" stroke="#8B5CF6" strokeWidth="1.5" strokeOpacity="0.6" />
      <line x1="24" y1="8" x2="16" y2="16" stroke="#06B6D4" strokeWidth="1.5" strokeOpacity="0.6" />
      <line x1="8" y1="24" x2="16" y2="16" stroke="#06B6D4" strokeWidth="1.5" strokeOpacity="0.6" />
      <line x1="24" y1="24" x2="16" y2="16" stroke="#8B5CF6" strokeWidth="1.5" strokeOpacity="0.6" />
    </svg>
  );
}
