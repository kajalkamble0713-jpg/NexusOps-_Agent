import type { Metadata } from "next";
import "./globals.css";
import { Toaster } from "react-hot-toast";

export const metadata: Metadata = {
  title: "NexusOps Agent — Your life's operations center",
  description:
    "AI-powered personal and professional operations hub. Intelligently automated with Gemini and MongoDB.",
  keywords: ["productivity", "AI agent", "task management", "MongoDB", "Gemini"],
  openGraph: {
    title: "NexusOps Agent",
    description: "Your life's operations center — intelligently automated.",
    type: "website",
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark">
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link
          rel="preconnect"
          href="https://fonts.gstatic.com"
          crossOrigin="anonymous"
        />
        <link
          href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap"
          rel="stylesheet"
        />
      </head>
      <body className="bg-[#0F172A] text-[#F8FAFC] antialiased">
        {children}
        <Toaster
          position="bottom-right"
          toastOptions={{
            style: {
              background: "#1E293B",
              color: "#F8FAFC",
              border: "1px solid rgba(148, 163, 184, 0.12)",
              borderRadius: "10px",
              fontSize: "14px",
            },
            success: {
              iconTheme: {
                primary: "#10B981",
                secondary: "#1E293B",
              },
            },
            error: {
              iconTheme: {
                primary: "#F43F5E",
                secondary: "#1E293B",
              },
            },
          }}
        />
      </body>
    </html>
  );
}
