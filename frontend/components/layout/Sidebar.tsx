"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { motion } from "framer-motion";
import {
  LayoutDashboard,
  CheckSquare,
  Target,
  Repeat2,
  Lightbulb,
  Bot,
  Settings,
  ChevronLeft,
} from "lucide-react";
import { cn } from "@/lib/utils";

const navItems = [
  { href: "/dashboard", icon: LayoutDashboard, label: "Dashboard" },
  { href: "/dashboard/agent", icon: Bot, label: "Agent", badge: "AI" },
  { href: "/dashboard/tasks", icon: CheckSquare, label: "Tasks" },
  { href: "/dashboard/goals", icon: Target, label: "Goals" },
  { href: "/dashboard/habits", icon: Repeat2, label: "Habits" },
  { href: "/dashboard/insights", icon: Lightbulb, label: "Insights" },
];

interface SidebarProps {
  collapsed?: boolean;
  onToggle?: () => void;
}

export function Sidebar({ collapsed = false, onToggle }: SidebarProps) {
  const pathname = usePathname();

  return (
    <aside
      className={cn(
        "flex flex-col h-full bg-[#1E293B] border-r border-[rgba(148,163,184,0.12)] transition-all duration-300",
        collapsed ? "w-16" : "w-56"
      )}
    >
      {/* Logo */}
      <div className="flex items-center gap-3 px-4 py-5 border-b border-[rgba(148,163,184,0.12)]">
        <NexusLogo />
        {!collapsed && (
          <motion.span
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="font-semibold text-[#F8FAFC] text-base"
          >
            NexusOps
          </motion.span>
        )}
      </div>

      {/* Navigation */}
      <nav className="flex-1 px-2 py-4 space-y-1">
        {navItems.map((item) => {
          const isActive = pathname === item.href;
          const Icon = item.icon;

          return (
            <Link key={item.href} href={item.href}>
              <motion.div
                whileHover={{ x: 2 }}
                className={cn(
                  "nav-item flex items-center gap-3 px-3 py-2.5 rounded-lg transition-all duration-150 cursor-pointer group",
                  isActive
                    ? "bg-[rgba(139,92,246,0.15)] text-[#8B5CF6]"
                    : "text-[#94A3B8] hover:bg-[rgba(148,163,184,0.06)] hover:text-[#F8FAFC]",
                  isActive && "active"
                )}
              >
                <Icon
                  size={18}
                  className={cn(
                    "flex-shrink-0 transition-colors",
                    isActive ? "text-[#8B5CF6]" : "text-[#94A3B8] group-hover:text-[#F8FAFC]"
                  )}
                />
                {!collapsed && (
                  <motion.span
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    className="text-sm font-medium flex-1"
                  >
                    {item.label}
                  </motion.span>
                )}
                {!collapsed && item.badge && (
                  <span className="text-[10px] font-semibold bg-[rgba(139,92,246,0.2)] text-[#8B5CF6] px-1.5 py-0.5 rounded-full">
                    {item.badge}
                  </span>
                )}
              </motion.div>
            </Link>
          );
        })}
      </nav>

      {/* Bottom */}
      <div className="px-2 py-4 border-t border-[rgba(148,163,184,0.12)] space-y-1">
        <button
          onClick={onToggle}
          className="w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-[#94A3B8] hover:bg-[rgba(148,163,184,0.06)] hover:text-[#F8FAFC] transition-all duration-150"
        >
          <ChevronLeft
            size={18}
            className={cn("transition-transform duration-300", collapsed && "rotate-180")}
          />
          {!collapsed && <span className="text-sm font-medium">Collapse</span>}
        </button>
      </div>
    </aside>
  );
}

function NexusLogo() {
  return (
    <svg
      width="28"
      height="28"
      viewBox="0 0 32 32"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      className="flex-shrink-0"
    >
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
