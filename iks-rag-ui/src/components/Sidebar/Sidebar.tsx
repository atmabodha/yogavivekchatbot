"use client";

import { useState, useEffect } from "react";

import { useTheme } from "next-themes";
import Image from "next/image";
interface Chat {
  id: string;
  title: string;
  preview: string;
  timestamp: string;
}

interface SidebarProps {
  onClose: () => void;
}

export default function Sidebar({ }: SidebarProps) {
  const [searchQuery] = useState("");
  const { resolvedTheme, setTheme } = useTheme();
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    if (resolvedTheme) setMounted(true);
  }, [resolvedTheme]);

  const toggleTheme = () => {
    setTheme(resolvedTheme === "dark" ? "light" : "dark");
  };

  const [chats] = useState<Chat[]>([
    {
      id: "1",
      title: "Understanding Karma Yoga",
      preview: "What is karma yoga and how can I practice it?",
      timestamp: "2h ago",
    },
    {
      id: "2",
      title: "Meditation Techniques",
      preview: "Can you guide me through basic meditation?",
      timestamp: "1d ago",
    },
    {
      id: "3",
      title: "Mindfulness Tips",
      preview: "Best ways to stay mindful in daily life?",
      timestamp: "3d ago",
    },
  ]);

  // Filter chats based on search query
  const filteredChats = chats.filter(
    (chat) =>
      chat.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
      chat.preview.toLowerCase().includes(searchQuery.toLowerCase())
  );

  if (!mounted) {
    return null; // Avoid hydration mismatch
  }

  return (
    <div className="fixed inset-y-0 left-0 w-[360px] sm:w-80 h-full bg-white dark:bg-gray-800 border-r border-gray-200 dark:border-gray-700 flex flex-col transition-all">
      {/* Header Section */}
      {/* Footer (Theme Toggle) */}
      <div className="p-4 border-t border-gray-200 dark:border-gray-700">
        <button
          onClick={toggleTheme}
          className="flex items-center space-x-2 text-sm text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white transition-colors"
        >
          <span>{resolvedTheme === "dark" ? "☀️" : "🌙"}</span>
          <span>{resolvedTheme === "dark" ? "Light Mode" : "Dark Mode"}</span>
        </button>
      </div>
     
      <Image
              src="/assets/images/krishna-2.jpg"
              alt="SAMAY"
              width={500}
              height={1000}
              className="object-cover h-full opacity-80"
            />

      
    </div>
  );
}
