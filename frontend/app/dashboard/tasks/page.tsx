"use client";

import { useEffect, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Task } from "@/lib/types";
import { tasksAPI } from "@/lib/api";
import { TaskCard } from "@/components/tasks/TaskCard";
import { getUserId } from "@/lib/utils";
import { Plus, Filter } from "lucide-react";
import toast from "react-hot-toast";

const COLUMNS: { id: Task["status"]; label: string; color: string }[] = [
  { id: "backlog", label: "Backlog", color: "#475569" },
  { id: "today", label: "Today", color: "#8B5CF6" },
  { id: "in_progress", label: "In Progress", color: "#F59E0B" },
  { id: "done", label: "Done", color: "#10B981" },
];

export default function TasksPage() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [newTask, setNewTask] = useState({
    title: "",
    priority: "normal" as Task["priority"],
    estimated_minutes: 30,
    description: "",
  });

  const userId = getUserId();

  const loadTasks = async () => {
    try {
      const res = await tasksAPI.getAll(userId);
      setTasks(res.tasks);
    } catch (error) {
      toast.error("Failed to load tasks");
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    loadTasks();
  }, []);

  const handleStatusChange = async (taskId: string, status: Task["status"]) => {
    try {
      await tasksAPI.update(taskId, { status });
      setTasks((prev) =>
        prev.map((t) => (t._id === taskId ? { ...t, status } : t))
      );
      toast.success("Task updated");
    } catch {
      toast.error("Failed to update task");
    }
  };

  const handleCreateTask = async () => {
    if (!newTask.title.trim()) return;

    try {
      await tasksAPI.create({
        ...newTask,
        user_id: userId,
        status: "backlog",
        tags: [],
        dependencies: [],
        metadata: {},
      });
      toast.success("Task created");
      setShowCreateModal(false);
      setNewTask({ title: "", priority: "normal", estimated_minutes: 30, description: "" });
      loadTasks();
    } catch {
      toast.error("Failed to create task");
    }
  };

  const getColumnTasks = (status: Task["status"]) =>
    tasks.filter((t) => t.status === status);

  return (
    <div className="max-w-7xl mx-auto">
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <div>
          <h1 className="text-xl font-semibold text-[#F8FAFC]">Task Board</h1>
          <p className="text-sm text-[#94A3B8] mt-0.5">
            {tasks.length} total tasks · {getColumnTasks("done").length} completed
          </p>
        </div>
        <div className="flex items-center gap-2">
          <button className="flex items-center gap-2 text-sm text-[#94A3B8] hover:text-[#F8FAFC] bg-[rgba(148,163,184,0.06)] border border-[rgba(148,163,184,0.12)] px-3 py-2 rounded-lg transition-all">
            <Filter size={14} />
            Filter
          </button>
          <button
            onClick={() => setShowCreateModal(true)}
            className="flex items-center gap-2 text-sm text-white bg-[#8B5CF6] hover:bg-[#7C3AED] px-4 py-2 rounded-lg transition-all shadow-[0_0_12px_rgba(139,92,246,0.3)]"
          >
            <Plus size={14} />
            New Task
          </button>
        </div>
      </div>

      {/* Kanban board */}
      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-4">
        {COLUMNS.map((column) => {
          const columnTasks = getColumnTasks(column.id);
          return (
            <div key={column.id} className="flex flex-col">
              {/* Column header */}
              <div className="flex items-center justify-between mb-3">
                <div className="flex items-center gap-2">
                  <div
                    className="w-2 h-2 rounded-full"
                    style={{ background: column.color }}
                  />
                  <span className="text-sm font-medium text-[#F8FAFC]">
                    {column.label}
                  </span>
                </div>
                <span className="text-xs text-[#475569] bg-[rgba(148,163,184,0.06)] px-2 py-0.5 rounded-full">
                  {columnTasks.length}
                </span>
              </div>

              {/* Column body */}
              <div
                className="kanban-column flex-1 rounded-xl border border-[rgba(148,163,184,0.08)] bg-[rgba(148,163,184,0.02)] p-2 space-y-2 min-h-[200px]"
              >
                {isLoading ? (
                  [...Array(2)].map((_, i) => (
                    <div
                      key={i}
                      className="h-20 bg-[rgba(148,163,184,0.06)] rounded-xl animate-pulse"
                    />
                  ))
                ) : (
                  <AnimatePresence>
                    {columnTasks.map((task) => (
                      <TaskCard
                        key={task._id}
                        task={task}
                        onStatusChange={handleStatusChange}
                      />
                    ))}
                  </AnimatePresence>
                )}

                {!isLoading && columnTasks.length === 0 && (
                  <div className="flex items-center justify-center h-20 text-[11px] text-[#475569]">
                    No tasks
                  </div>
                )}
              </div>
            </div>
          );
        })}
      </div>

      {/* Create task modal */}
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
                Create New Task
              </h2>

              <div className="space-y-4">
                <div>
                  <label className="text-xs text-[#94A3B8] mb-1.5 block">Title *</label>
                  <input
                    type="text"
                    value={newTask.title}
                    onChange={(e) => setNewTask({ ...newTask, title: e.target.value })}
                    placeholder="What needs to be done?"
                    className="w-full bg-[rgba(148,163,184,0.06)] border border-[rgba(148,163,184,0.12)] rounded-lg px-3 py-2.5 text-sm text-[#F8FAFC] placeholder-[#475569] outline-none focus:border-[rgba(139,92,246,0.4)]"
                    autoFocus
                  />
                </div>

                <div>
                  <label className="text-xs text-[#94A3B8] mb-1.5 block">Description</label>
                  <textarea
                    value={newTask.description}
                    onChange={(e) => setNewTask({ ...newTask, description: e.target.value })}
                    placeholder="Optional details..."
                    rows={2}
                    className="w-full bg-[rgba(148,163,184,0.06)] border border-[rgba(148,163,184,0.12)] rounded-lg px-3 py-2.5 text-sm text-[#F8FAFC] placeholder-[#475569] outline-none focus:border-[rgba(139,92,246,0.4)] resize-none"
                  />
                </div>

                <div className="grid grid-cols-2 gap-3">
                  <div>
                    <label className="text-xs text-[#94A3B8] mb-1.5 block">Priority</label>
                    <select
                      value={newTask.priority}
                      onChange={(e) => setNewTask({ ...newTask, priority: e.target.value as Task["priority"] })}
                      className="w-full bg-[rgba(148,163,184,0.06)] border border-[rgba(148,163,184,0.12)] rounded-lg px-3 py-2.5 text-sm text-[#F8FAFC] outline-none focus:border-[rgba(139,92,246,0.4)]"
                    >
                      <option value="critical">🔴 Critical</option>
                      <option value="high">🟡 High</option>
                      <option value="normal">🟢 Normal</option>
                      <option value="low">⬛ Low</option>
                    </select>
                  </div>

                  <div>
                    <label className="text-xs text-[#94A3B8] mb-1.5 block">Est. Minutes</label>
                    <input
                      type="number"
                      value={newTask.estimated_minutes}
                      onChange={(e) => setNewTask({ ...newTask, estimated_minutes: parseInt(e.target.value) || 30 })}
                      min={5}
                      max={480}
                      className="w-full bg-[rgba(148,163,184,0.06)] border border-[rgba(148,163,184,0.12)] rounded-lg px-3 py-2.5 text-sm text-[#F8FAFC] outline-none focus:border-[rgba(139,92,246,0.4)]"
                    />
                  </div>
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
                  onClick={handleCreateTask}
                  disabled={!newTask.title.trim()}
                  className="flex-1 text-sm text-white bg-[#8B5CF6] hover:bg-[#7C3AED] py-2.5 rounded-xl transition-all disabled:opacity-40 disabled:cursor-not-allowed"
                >
                  Create Task
                </button>
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
