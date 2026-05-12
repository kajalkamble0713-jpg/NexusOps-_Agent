"use client";

import { useEffect, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Habit } from "@/lib/types";
import { habitsAPI } from "@/lib/api";
import { HabitGrid } from "@/components/dashboard/HabitGrid";
import { getUserId } from "@/lib/utils";
import { Plus, Flame, Trophy, Repeat2 } from "lucide-react";
import toast from "react-hot-toast";

const CATEGORIES = ["health", "productivity", "learning", "wellness"];
const FREQUENCIES = ["daily", "weekly"];

export default function HabitsPage() {
  const [habits, setHabits] = useState<Habit[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [newHabit, setNewHabit] = useState<{
    name: string;
    category: "health" | "productivity" | "learning" | "wellness";
    frequency: "daily" | "weekly" | "custom";
    reminder_time: string;
  }>({
    name: "",
    category: "health",
    frequency: "daily",
    reminder_time: "09:00",
  });

  const userId = getUserId();

  const loadHabits = async () => {
    try {
      const res = await habitsAPI.getAll(userId);
      setHabits(res.habits);
    } catch {
      toast.error("Failed to load habits");
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    loadHabits();
  }, []);

  const handleCreateHabit = async () => {
    if (!newHabit.name.trim()) return;

    try {
      await habitsAPI.create({
        ...newHabit,
        user_id: userId,
      });
      toast.success("Habit created");
      setShowCreateModal(false);
      setNewHabit({ name: "", category: "health", frequency: "daily", reminder_time: "09:00" });
      loadHabits();
    } catch {
      toast.error("Failed to create habit");
    }
  };

  const totalStreak = habits.reduce((sum, h) => sum + h.streak_count, 0);
  const bestStreak = Math.max(...habits.map((h) => h.best_streak), 0);
  const completedToday = habits.filter((h) => {
    const today = new Date().toISOString().split("T")[0];
    return h.completion_log.some((log) => log.startsWith(today));
  }).length;

  return (
    <div className="max-w-3xl mx-auto">
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-xl font-semibold text-[#F8FAFC]">Habit Tracker</h1>
          <p className="text-sm text-[#94A3B8] mt-0.5">
            {habits.length} habits · {completedToday}/{habits.length} done today
          </p>
        </div>
        <button
          onClick={() => setShowCreateModal(true)}
          className="flex items-center gap-2 text-sm text-white bg-[#8B5CF6] hover:bg-[#7C3AED] px-4 py-2 rounded-lg transition-all shadow-[0_0_12px_rgba(139,92,246,0.3)]"
        >
          <Plus size={14} />
          New Habit
        </button>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-3 gap-4 mb-6">
        {[
          { label: "Total Streak Days", value: totalStreak, icon: Flame, color: "#F59E0B" },
          { label: "Best Streak", value: bestStreak, icon: Trophy, color: "#10B981" },
          { label: "Done Today", value: `${completedToday}/${habits.length}`, icon: Repeat2, color: "#8B5CF6" },
        ].map((stat, i) => {
          const Icon = stat.icon;
          return (
            <motion.div
              key={stat.label}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.07 }}
              className="card p-4 text-center"
            >
              <Icon size={20} className="mx-auto mb-2" style={{ color: stat.color }} />
              <div className="text-xl font-bold text-[#F8FAFC]">{stat.value}</div>
              <div className="text-xs text-[#94A3B8] mt-0.5">{stat.label}</div>
            </motion.div>
          );
        })}
      </div>

      {/* Habits list */}
      <div className="card p-5">
        <h2 className="text-sm font-semibold text-[#F8FAFC] mb-4">All Habits</h2>
        {isLoading ? (
          <div className="space-y-2">
            {[...Array(4)].map((_, i) => (
              <div key={i} className="h-12 bg-[rgba(148,163,184,0.06)] rounded-xl animate-pulse" />
            ))}
          </div>
        ) : habits.length > 0 ? (
          <HabitGrid habits={habits} onUpdate={loadHabits} />
        ) : (
          <div className="text-center py-8">
            <Repeat2 size={32} className="text-[#475569] mx-auto mb-3" />
            <p className="text-sm text-[#94A3B8]">No habits yet</p>
            <button
              onClick={() => setShowCreateModal(true)}
              className="mt-3 text-sm text-[#8B5CF6] hover:text-[#A78BFA] transition-colors"
            >
              Add your first habit
            </button>
          </div>
        )}
      </div>

      {/* Create habit modal */}
      <AnimatePresence>
        {showCreateModal && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 bg-black/60 backdrop-blur-sm flex items-center justify-center z-50 p-4"
            onClick={(e) => e.target === e.currentTarget && setShowCreateModal(false)}
          >
            <motion.div
              initial={{ scale: 0.95, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              exit={{ scale: 0.95, opacity: 0 }}
              className="bg-[#1E293B] border border-[rgba(148,163,184,0.12)] rounded-2xl p-6 w-full max-w-md"
            >
              <h2 className="text-base font-semibold text-[#F8FAFC] mb-4">
                Create New Habit
              </h2>

              <div className="space-y-4">
                <div>
                  <label className="text-xs text-[#94A3B8] mb-1.5 block">Habit Name *</label>
                  <input
                    type="text"
                    value={newHabit.name}
                    onChange={(e) => setNewHabit({ ...newHabit, name: e.target.value })}
                    placeholder="e.g., Morning workout, Read 30 minutes"
                    className="w-full bg-[rgba(148,163,184,0.06)] border border-[rgba(148,163,184,0.12)] rounded-lg px-3 py-2.5 text-sm text-[#F8FAFC] placeholder-[#475569] outline-none focus:border-[rgba(139,92,246,0.4)]"
                    autoFocus
                  />
                </div>

                <div className="grid grid-cols-2 gap-3">
                  <div>
                    <label className="text-xs text-[#94A3B8] mb-1.5 block">Category</label>
                    <select
                      value={newHabit.category}
                      onChange={(e) => setNewHabit({ ...newHabit, category: e.target.value as "health" | "productivity" | "learning" | "wellness" })}
                      className="w-full bg-[rgba(148,163,184,0.06)] border border-[rgba(148,163,184,0.12)] rounded-lg px-3 py-2.5 text-sm text-[#F8FAFC] outline-none focus:border-[rgba(139,92,246,0.4)]"
                    >
                      {CATEGORIES.map((cat) => (
                        <option key={cat} value={cat} className="capitalize">
                          {cat.charAt(0).toUpperCase() + cat.slice(1)}
                        </option>
                      ))}
                    </select>
                  </div>

                  <div>
                    <label className="text-xs text-[#94A3B8] mb-1.5 block">Frequency</label>
                    <select
                      value={newHabit.frequency}
                      onChange={(e) => setNewHabit({ ...newHabit, frequency: e.target.value as "daily" | "weekly" | "custom" })}
                      className="w-full bg-[rgba(148,163,184,0.06)] border border-[rgba(148,163,184,0.12)] rounded-lg px-3 py-2.5 text-sm text-[#F8FAFC] outline-none focus:border-[rgba(139,92,246,0.4)]"
                    >
                      {FREQUENCIES.map((freq) => (
                        <option key={freq} value={freq} className="capitalize">
                          {freq.charAt(0).toUpperCase() + freq.slice(1)}
                        </option>
                      ))}
                    </select>
                  </div>
                </div>

                <div>
                  <label className="text-xs text-[#94A3B8] mb-1.5 block">Reminder Time</label>
                  <input
                    type="time"
                    value={newHabit.reminder_time}
                    onChange={(e) => setNewHabit({ ...newHabit, reminder_time: e.target.value })}
                    className="w-full bg-[rgba(148,163,184,0.06)] border border-[rgba(148,163,184,0.12)] rounded-lg px-3 py-2.5 text-sm text-[#F8FAFC] outline-none focus:border-[rgba(139,92,246,0.4)]"
                  />
                </div>
              </div>

              <div className="flex gap-3 mt-6">
                <button
                  onClick={() => setShowCreateModal(false)}
                  className="flex-1 text-sm text-[#94A3B8] hover:text-[#F8FAFC] bg-[rgba(148,163,184,0.06)] border border-[rgba(148,163,184,0.12)] py-2.5 rounded-xl transition-all"
                >
                  Cancel
                </button>
                <button
                  onClick={handleCreateHabit}
                  disabled={!newHabit.name.trim()}
                  className="flex-1 text-sm text-white bg-[#8B5CF6] hover:bg-[#7C3AED] py-2.5 rounded-xl transition-all disabled:opacity-40 disabled:cursor-not-allowed"
                >
                  Create Habit
                </button>
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
