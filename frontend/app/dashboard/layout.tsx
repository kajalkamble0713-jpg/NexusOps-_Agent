"use client";

import { useState } from "react";
import { Sidebar } from "@/components/layout/Sidebar";
import { TopBar } from "@/components/layout/TopBar";

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);
  const [isAgentRunning, setIsAgentRunning] = useState(false);

  return (
    <div className="flex h-screen overflow-hidden bg-[#0F172A]">
      {/* Sidebar */}
      <Sidebar
        collapsed={sidebarCollapsed}
        onToggle={() => setSidebarCollapsed(!sidebarCollapsed)}
      />

      {/* Main content */}
      <div className="flex-1 flex flex-col overflow-hidden">
        <TopBar isAgentRunning={isAgentRunning} />
        <main className="flex-1 overflow-y-auto p-6">
          {children}
        </main>
      </div>
    </div>
  );
}
