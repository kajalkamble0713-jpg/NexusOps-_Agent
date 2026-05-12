"use client";

import { useEffect, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Goal, GoalCategory } from "@/lib/types";
import { goalsAPI } from "@/lib/api";
import { GoalHealthCard } from "@/components/dashboard/GoalHealthCard";
import { getUserId } from "@/lib/utils";
import { Plus, Target } from "lucide-react";
import toast from "react-hot-toast";

const CATEGORIES = ["career", "health", "learning", "personal", "financial"];

export default function GoalsPage() {
  const [goals, setGoals] = useState<Goal[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [newGoal, setNewGoal] = useState<{
    title: string;
    category: GoalCategory;
    target_date: string;
    weekly_target: number;
  }>({
    title: "",
    category: "career",
    target_date: "",
    weekly_target: 5,
  });

  const userId = getUserId();

  const loadGoals = async () => {
    try {
      const res = await goalsAPI.getAll(userId);
      setGoals(res.goals);
    } catch {
      toast.error("Failed to load goals");
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    loadGoals();
  }, []);

  const handleCreateGoal = async () => {
    if (!newGoal.title.trim() || !newGoal.target_date) return;

    try {
      await goalsAPI.create({
        ...newGoal,
        user_id: userId,
        current_progress: 0,
        milestones: [],
        insights: [],
        ai_suggestions: [],
      });
      toast.success("Goal created");
      setShowCreateModal(false);
      setNewGoal({ title: "", category: "career", target_date: "", weekly_target: 5 });
      loadGoals();
    } catch {
      toast.error("Failed to create goal");
    }
  };

  const activeGoals = goals.filter((g) => g.current_progress < 100);
  const completedGoals = goals.filter((g) => g.current_progress >= 100);

  return (
    <div className="max-w-5xl mx-auto">
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-xl font-semibold text-[#F8FAFC]">Goal Tracker</h1>
          <p className="text-sm text-[#94A3B8] mt-0.5">
            {activeGoals.length} active · {completedGoals.length} completed
          </p>
        </div>
        <button
          onClick={() => setShowCreateModal(true)}
          className="flex items-center gap-2 text-sm text-white bg-[#8B5CF6] hover:bg-[#7C3AED] px-4 py-2 rounded-lg transition-all shadow-[0_0_12px_rgba(139,92,246,0.3)]"
        >
          <Plus size={14} />
          New Goal
        </button>
      </div>

      {/* Active goals */}
      {isLoading ? (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {[...Array(4)].map((_, i) => (
            <div key={i} className="h-48 bg-[rgba(148,163,184,0.06)] rounded-xl animate-pulse" />
          ))}
        </div>
      ) : activeGoals.length > 0 ? (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <AnimatePresence>
            {activeGoals.map((goal) => (
              <GoalHealthCard key={goal._id} goal={goal} />
            ))}
          </AnimatePresence>
        </div>
      ) : (
        <div className="card p-12 text-center">
          <Target size={40} className="text-[#475569] mx-auto mb-4" />
          <h3 className="text-base font-semibold text-[#F8FAFC] mb-2">No active goals</h3>
          <p className="text-sm text-[#94A3B8] mb-4">
            Set your first goal to start tracking progress
          </p>
          <button
            onClick={() => setShowCreateModal(true)}
            className="text-sm text-white bg-[#8B5CF6] hover:bg-[#7C3AED] px-4 py-2 rounded-lg transition-all"
          >
            Create Goal
          </button>
        </div>
      )}

      {/* Create goal modal */}
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
                Create New Goal
              </h2>

              <div className="space-y-4">
                <div>
                  <label className="text-xs text-[#94A3B8] mb-1.5 block">Goal Title *</label>
                  <input
                    type="text"
                    value={newGoal.title}
                    onChange={(e) => setNewGoal({ ...newGoal, title: e.target.value })}
                    placeholder="What do you want to achieve?"
                    className="w-full bg-[rgba(148,163,184,0.06)] border border-[rgba(148,163,184,0.12)] rounded-lg px-3 py-2.5 text-sm text-[#F8FAFC] placeholder-[#475569] outline-none focus:border-[rgba(139,92,246,0.4)]"
                    autoFocus
                  />
                </div>

                <div className="grid grid-cols-2 gap-3">
                  <div>
                    <label className="text-xs text-[#94A3B8] mb-1.5 block">Category</label>
                    <select
                      value={newGoal.category}
                      onChange={(e) => setNewGoal({ ...newGoal, category: e.target.value as GoalCategory })}
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
                    <label className="text-xs text-[#94A3B8] mb-1.5 block">Target Date *</label>
                    <input
                      type="date"
                      value={newGoal.target_date}
                      onChange={(e) => setNewGoal({ ...newGoal, target_date: e.target.value })}
                      className="w-full bg-[rgba(148,163,184,0.06)] border border-[rgba(148,163,184,0.12)] rounded-lg px-3 py-2.5 text-sm text-[#F8FAFC] outline-none focus:border-[rgba(139,92,246,0.4)]"
                    />
                  </div>
                </div>

                <div>
                  <label className="text-xs text-[#94A3B8] mb-1.5 block">
                    Weekly Progress Target (%)
                  </label>
                  <input
                    type="number"
                    value={newGoal.weekly_target}
                    onChange={(e) => setNewGoal({ ...newGoal, weekly_target: parseInt(e.target.value) || 5 })}
                    min={1}
                    max={50}
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
                  onClick={handleCreateGoal}
                  disabled={!newGoal.title.trim() || !newGoal.target_date}
                  className="flex-1 text-sm text-white bg-[#8B5CF6] hover:bg-[#7C3AED] py-2.5 rounded-xl transition-all disabled:opacity-40 disabled:cursor-not-allowed"
                >
                  Create Goal
                </button>
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
