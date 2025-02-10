import { useEffect, useRef } from "react";
import { ChatMessage } from "@/types/chat";
import ReferenceList from "./ReferenceList";
import { motion } from "framer-motion";
import ReactMarkdown from "react-markdown";

interface MessageListProps {
  messages: ChatMessage[];
}

export default function MessageList({ messages }: MessageListProps) {
  const messagesEndRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: "smooth" });
    }
  }, [messages]);

  return (
    <div className="space-y-6">
      {messages.map((message) => (
        <motion.div
          key={message.id}
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          className={`flex ${message.role === "user" ? "justify-end" : "justify-start"}`}
        >
          <div
            className={`max-w-[85%] md:max-w-[75%] rounded-2xl px-4 py-3 ${
              message.role === "user"
                ? "bg-indigo-600 text-white"
                : "bg-white dark:bg-gray-800 shadow-md"
            }`}
          >
            <ReactMarkdown
              className={`prose ${
                message.role === "user"
                  ? "prose-invert"
                  : "prose-gray dark:prose-invert"
              } max-w-none prose-p:leading-relaxed prose-pre:bg-gray-100 dark:prose-pre:bg-gray-900 prose-pre:p-2 prose-pre:rounded`}
            >
              {message.content}
            </ReactMarkdown>

            {/* Reference List (if available) */}
            {message.references && message.references.length > 0 && (
              <div className={`mt-2 border-t border-gray-300 dark:border-gray-600 pt-2`}>
                <ReferenceList
                  references={message.references}
                  isUserMessage={message.role === "user"}
                />
              </div>
            )}

            {/* Timestamp & Confidence Level */}
            <div className="flex justify-between items-center mt-2 text-xs opacity-70">
              <span className="text-gray-100 dark:text-gray-400">
                {new Date(message.timestamp).toLocaleTimeString([], {
                  hour: "2-digit",
                  minute: "2-digit",
                })}
              </span>
              {message.confidence && (
                <span className="ml-2 text-gray-600 dark:text-gray-400">
                  Confidence: {(message.confidence * 100).toFixed(1)}%
                </span>
              )}
            </div>
          </div>
        </motion.div>
      ))}
      {/* Empty div to scroll into view */}
      <div ref={messagesEndRef} />
    </div>
  );
}
