"use client";

import { Bell, Search } from "lucide-react";
import { AgentStatusIndicator } from "./AgentStatusIndicator";
import { getGreeting, getDayOfWeek, getUserName } from "@/lib/utils";
import { useEffect, useState } from "react";

interface TopBarProps {
  isAgentRunning?: boolean;
}

export function TopBar({ isAgentRunning = false }: TopBarProps) {
  const [greeting, setGreeting] = useState("Good morning");
  const [dayOfWeek, setDayOfWeek] = useState("");
  const [userName, setUserName] = useState("Alex");
  const [currentDate, setCurrentDate] = useState("");

  useEffect(() => {
    setGreeting(getGreeting());
    setDayOfWeek(getDayOfWeek());
    setUserName(getUserName());
    setCurrentDate(
      new Date().toLocaleDateString("en-US", {
        month: "long",
        day: "numeric",
        year: "numeric",
      })
    );
  }, []);

  return (
    <header className="h-14 flex items-center justify-between px-6 border-b border-[rgba(148,163,184,0.12)] bg-[#1E293B]">
      {/* Left: Greeting */}
      <div className="flex items-center gap-4">
        <div>
          <span className="text-sm text-[#94A3B8]">
            {greeting}, <span className="text-[#F8FAFC] font-medium">{userName}</span>
          </span>
          <span className="text-[#475569] mx-2">·</span>
          <span className="text-sm text-[#475569]">
            {dayOfWeek}, {currentDate}
          </span>
        </div>
      </div>

      {/* Right: Actions */}
      <div className="flex items-center gap-3">
        <AgentStatusIndicator isRunning={isAgentRunning} />

        {/* Search */}
        <button className="flex items-center gap-2 bg-[rgba(148,163,184,0.06)] hover:bg-[rgba(148,163,184,0.1)] border border-[rgba(148,163,184,0.12)] rounded-lg px-3 py-1.5 text-[#94A3B8] hover:text-[#F8FAFC] transition-all duration-150">
          <Search size={14} />
          <span className="text-xs">Search</span>
          <kbd className="text-[10px] bg-[rgba(148,163,184,0.1)] px-1.5 py-0.5 rounded text-[#475569]">
            ⌘K
          </kbd>
        </button>

        {/* Notifications */}
        <button className="relative p-2 rounded-lg text-[#94A3B8] hover:text-[#F8FAFC] hover:bg-[rgba(148,163,184,0.06)] transition-all duration-150">
          <Bell size={16} />
          <span className="absolute top-1.5 right-1.5 w-1.5 h-1.5 bg-[#8B5CF6] rounded-full" />
        </button>
      </div>
    </header>
  );
}
