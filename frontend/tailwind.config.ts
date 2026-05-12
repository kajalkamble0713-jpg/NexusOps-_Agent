import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        // Core backgrounds
        "bg-base": "#0F172A",
        "bg-surface": "#1E293B",
        "bg-elevated": "#334155",
        "bg-subtle": "#0EA5E9",
        // Accents
        "accent-primary": "#8B5CF6",
        "accent-secondary": "#06B6D4",
        "accent-tertiary": "#10B981",
        // Semantic
        warning: "#F59E0B",
        danger: "#F43F5E",
        info: "#38BDF8",
        // Text
        "text-primary": "#F8FAFC",
        "text-secondary": "#94A3B8",
        "text-muted": "#475569",
      },
      fontFamily: {
        sans: ["Inter", "system-ui", "sans-serif"],
        mono: ["JetBrains Mono", "monospace"],
      },
      fontSize: {
        "heading-lg": ["28px", { lineHeight: "1.2", letterSpacing: "-0.02em", fontWeight: "600" }],
        "heading-md": ["20px", { lineHeight: "1.3", fontWeight: "600" }],
        "heading-sm": ["16px", { lineHeight: "1.4", fontWeight: "500" }],
        body: ["14px", { lineHeight: "1.6", fontWeight: "400" }],
        caption: ["12px", { lineHeight: "1.4", fontWeight: "500", letterSpacing: "0.06em" }],
        code: ["13px", { lineHeight: "1.5", fontWeight: "400" }],
      },
      borderColor: {
        default: "rgba(148, 163, 184, 0.12)",
        accent: "rgba(139, 92, 246, 0.40)",
      },
      backdropBlur: {
        card: "8px",
      },
      animation: {
        "pulse-ring": "pulse-ring 2s cubic-bezier(0.4, 0, 0.6, 1) infinite",
        "slide-in": "slide-in 0.3s ease-out",
        "fade-in": "fade-in 0.2s ease-out",
        "spin-slow": "spin 3s linear infinite",
      },
      keyframes: {
        "pulse-ring": {
          "0%, 100%": { opacity: "1" },
          "50%": { opacity: "0.4" },
        },
        "slide-in": {
          "0%": { transform: "translateY(10px)", opacity: "0" },
          "100%": { transform: "translateY(0)", opacity: "1" },
        },
        "fade-in": {
          "0%": { opacity: "0" },
          "100%": { opacity: "1" },
        },
      },
      boxShadow: {
        card: "0 1px 3px rgba(0,0,0,0.3), 0 1px 2px rgba(0,0,0,0.2)",
        "card-hover": "0 4px 12px rgba(0,0,0,0.4)",
        glow: "0 0 20px rgba(139, 92, 246, 0.3)",
      },
    },
  },
  plugins: [],
};

export default config;
