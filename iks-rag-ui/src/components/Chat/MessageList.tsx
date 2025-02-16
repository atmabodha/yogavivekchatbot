import { useEffect, useRef } from "react";
import { ChatMessage } from "@/types/chat";
import ReferenceList from "./ReferenceList";
import { motion } from "framer-motion";
import ReactMarkdown from "react-markdown";
import ChatResponse from "./ChatResponse";

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

  const parseResponse = (content: string) => {
    try {
      // Remove markdown code block markers and parse JSON
      const jsonStr = content.replace(/```json\n|\n```/g, '');
      const parsed = JSON.parse(jsonStr);
      return {
        summary: parsed.summary_answer?.replace(/\*\*/g, ''),
        explanation: parsed.detailed_answer?.replace(/\*\*/g, ''),
        references: parsed.references?.map((ref: any) => ({
          verse: `${ref.source} ${ref.chapter}:${ref.verse}`,
          text: ref.text
        })) || [],
        error: false
      };
    } catch (error) {
      console.error('Error parsing response:', error);
      return {
        error: true
      };
    }
  };

  return (
    <div className="space-y-6">
      {messages.map((message) => (
        <motion.div
          key={message.id}
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          className={`flex ${message.role === "user" ? "justify-end" : "justify-start"}`}
        >
          {message.role === "user" ? (
            <div className="max-w-[85%] md:max-w-[75%] rounded-2xl px-4 py-3 bg-indigo-600 text-white">
              <p className="prose prose-invert max-w-none prose-p:leading-relaxed">
                {message.content}
              </p>
            </div>
          ) : (
            <div className="max-w-[85%] md:max-w-[75%]">
              <ChatResponse {...parseResponse(message.content)} />
            </div>
          )}
        </motion.div>
      ))}
      {/* Empty div to scroll into view */}
      <div ref={messagesEndRef} />
    </div>
  );
}
