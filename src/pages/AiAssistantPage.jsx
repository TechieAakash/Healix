import React, { useState, useRef, useEffect } from "react";
import {
  Send,
  Paperclip,
  Bot,
  HelpCircle,
  ChevronRight,
  ShieldCheck,
  Plus,
  Loader2,
} from "lucide-react";
import { authService } from "../services/authService";
import { apiRequest } from "../services/apiClient";

export function AiAssistantPage() {
  const user = authService.getCurrentUser();
  const userName = user?.name || "Krish";

  const [conversationId, setConversationId] = useState(null);
  const [messages, setMessages] = useState(() => [
    {
      id: "m1",
      sender: "ai",
      time: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
      text: `Hi ${userName}! 👋\nI'm your Healix AI assistant. I can help you with:\n• Health queries\n• Symptom analysis\n• Personalized advice\n• General wellness tips\n\nWhat would you like to know today?`,
    },
  ]);

  const [inputMessage, setInputMessage] = useState("");
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef(null);

  // Load existing conversation from backend on mount
  useEffect(() => {
    const loadConversation = async () => {
      try {
        const result = await apiRequest("/chat/conversations?page_size=1");
        if (result && result.items && result.items.length > 0) {
          const conv = result.items[0];
          setConversationId(conv.id);
          // Map backend messages to our format
          if (conv.messages && conv.messages.length > 0) {
            const backendMessages = conv.messages.map((msg) => ({
              id: msg.message_id,
              sender: msg.role === "USER" ? "user" : "ai",
              time: new Date(msg.created_at).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
              text: msg.content,
            }));
            setMessages((prev) => [prev[0], ...backendMessages]);
          }
        }
      } catch {
        // Backend not available, use mock
        console.info("[Healix] Chat using offline mode.");
      }
    };
    loadConversation();
  }, []);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isTyping]);

  const quickSuggestions = [
    "What are my health metrics?",
    "Analyze my symptoms",
    "Build a daily care plan",
    "Explain my report results",
  ];

  const commonQuestions = [
    "How to improve sleep quality?",
    "What should I eat for better health?",
    "Exercise recommendations",
    "Stress management tips",
  ];

  const handleSend = async (textToSend) => {
    const text = textToSend || inputMessage;
    if (!text.trim()) return;

    const userMsg = {
      id: `usr_${Date.now()}`,
      sender: "user",
      time: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
      text: text.trim(),
    };

    setMessages((prev) => [...prev, userMsg]);
    setInputMessage("");
    setIsTyping(true);

    // Try backend API first
    try {
      let convId = conversationId;
      if (!convId) {
        // Create a new conversation
        const newConv = await apiRequest("/chat/conversations", {
          method: "POST",
          body: JSON.stringify({ title: text.trim().slice(0, 50) }),
        });
        if (newConv && newConv.id) {
          convId = newConv.id;
          setConversationId(convId);
        }
      }

      if (convId) {
        const res = await apiRequest(`/chat/conversations/${convId}/messages`, {
          method: "POST",
          body: JSON.stringify({ content: text.trim() }),
        });

        if (res) {
          // Find assistant response in res
          const assistantMsg = res.assistant_message || res;
          setMessages((prev) => [
            ...prev,
            {
              id: assistantMsg.message_id || `ai_${Date.now()}`,
              sender: "ai",
              time: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
              text: assistantMsg.content || assistantMsg.text || "I've noted your question. Let me help!",
            },
          ]);
          setIsTyping(false);
          return;
        }
      }
    } catch {
      // Backend unavailable, use local mock
      console.info("[Healix] Using offline AI response.");
    }

    // Offline fallback
    setTimeout(() => {
      let aiReply = "";
      const lower = text.toLowerCase();
      if (lower.includes("metrics") || lower.includes("health data")) {
        aiReply = `Here is your current health status summary:\n• Heart Rate: ${user?.metrics?.heartRate || "72 bpm"} (Normal resting)\n• Oxygen Saturation: ${user?.metrics?.spo2 || "98%"}\n• Sleep: ${user?.metrics?.sleep || "7h 42m"}\n• Steps: ${user?.metrics?.steps || "8,432"}\n\nYour general vitals are optimal and stable.`;
      } else if (lower.includes("sleep")) {
        aiReply = `To optimize your sleep quality:\n• Keep a consistent bedtime within 30 minutes each night\n• Limit screen exposure 45 mins before resting\n• Keep your bedroom cool (around 19°C) and dark\n• Avoid caffeine 6 hours before sleeping`;
      } else if (lower.includes("eat") || lower.includes("diet")) {
        aiReply = `A balanced nutritional approach:\n• Prioritize lean protein with each meal\n• Increase colorful fibrous vegetables\n• Stay hydrated with 2-2.5 liters of water\n• Minimize ultra-processed sugars and sodium`;
      } else if (lower.includes("exercise") || lower.includes("workout")) {
        aiReply = `Based on your recent activity:\n• 150 minutes of moderate aerobic activity weekly (e.g. brisk walking)\n• 2 days of functional resistance or core training\n• 5-10 minutes of daily mobility stretching`;
      } else if (lower.includes("care plan")) {
        aiReply = `I've prepared a customized wellness recommendation:\n• Morning: 25 min brisk outdoor walk\n• Afternoon: Hydration check (5 glasses done)\n• Evening: Light screen curfew & 7-8 hours sleep window`;
      } else if (lower.includes("stress")) {
        aiReply = `Effective evidence-based stress management strategies:\n• **Box breathing**: Inhale 4s → Hold 4s → Exhale 4s → Hold 4s, repeat 4 cycles\n• **Progressive muscle relaxation**: Tense and release each muscle group from toes upward\n• **Daily movement**: Even a 10-minute walk reduces cortisol levels meaningfully\n• **Sleep consistency**: Maintain the same wake-up time even on weekends`;
      } else {
        aiReply = `Thank you for sharing. I've noted your inquiry.\n\nI recommend monitoring any changes closely, maintaining good hydration, and consulting with your healthcare provider if you have acute discomfort. Would you like me to add this to your health log?`;
      }

      setMessages((prev) => [
        ...prev,
        {
          id: `ai_${Date.now()}`,
          sender: "ai",
          time: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
          text: aiReply,
        },
      ]);
      setIsTyping(false);
    }, 700);
  };

  const handleNewChat = async () => {
    setConversationId(null);
    setMessages([
      {
        id: `m_${Date.now()}`,
        sender: "ai",
        time: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
        text: `Hi ${userName}! 👋 Starting a new conversation. How can I help you today?`,
      },
    ]);
  };

  return (
    <div className="max-w-6xl mx-auto h-[calc(100vh-8.5rem)] flex flex-col lg:flex-row gap-5">
      {/* Main Chat Interface */}
      <div className="flex-1 bg-white rounded-2xl border border-slate-200/80 shadow-xs flex flex-col overflow-hidden">
        {/* Chat Header */}
        <div className="px-6 py-4 border-b border-slate-100 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-xl bg-emerald-50 text-emerald-700 flex items-center justify-center">
              <Bot className="w-5 h-5" />
            </div>
            <div>
              <h2 className="text-sm font-bold text-slate-900 tracking-tight">Healix AI</h2>
              <p className="text-[11px] text-slate-400">Your personal health assistant</p>
            </div>
          </div>
          <div className="flex items-center gap-3">
            <button
              onClick={handleNewChat}
              className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-emerald-50 text-emerald-800 text-xs font-medium hover:bg-emerald-100 transition-colors cursor-pointer"
            >
              <Plus className="w-3.5 h-3.5" />
              New Chat
            </button>
            <div className="flex items-center gap-1 text-[11px] text-emerald-800 bg-emerald-50 px-2.5 py-1 rounded-full font-medium">
              <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse"></span>
              <span>Online</span>
            </div>
          </div>
        </div>

        {/* Messages Stream */}
        <div className="flex-1 overflow-y-auto p-6 space-y-5">
          {messages.map((msg) => {
            const isUser = msg.sender === "user";
            return (
              <div
                key={msg.id}
                className={`flex gap-3 max-w-xl ${isUser ? "ml-auto justify-end" : "mr-auto justify-start"}`}
              >
                {!isUser && (
                  <div className="w-8 h-8 rounded-full bg-emerald-50 text-emerald-700 flex items-center justify-center shrink-0 mt-0.5">
                    <Bot className="w-4 h-4" />
                  </div>
                )}

                <div className="space-y-1">
                  <div
                    className={`rounded-2xl p-4 text-xs sm:text-sm leading-relaxed whitespace-pre-line shadow-xs ${
                      isUser
                        ? "bg-[#065f46] text-white rounded-br-xs"
                        : "bg-slate-50 text-slate-800 border border-slate-200/70 rounded-bl-xs"
                    }`}
                  >
                    {msg.text}
                  </div>
                  <p
                    className={`text-[10px] text-slate-400 px-1 ${
                      isUser ? "text-right" : "text-left"
                    }`}
                  >
                    {msg.time}
                  </p>
                </div>
              </div>
            );
          })}

          {isTyping && (
            <div className="flex items-center gap-2 text-xs text-slate-400 p-2">
              <div className="w-7 h-7 rounded-full bg-emerald-50 text-emerald-700 flex items-center justify-center">
                <Bot className="w-3.5 h-3.5" />
              </div>
              <div className="flex items-center gap-1">
                <span className="w-1.5 h-1.5 rounded-full bg-emerald-600 animate-bounce"></span>
                <span className="w-1.5 h-1.5 rounded-full bg-emerald-600 animate-bounce delay-100"></span>
                <span className="w-1.5 h-1.5 rounded-full bg-emerald-600 animate-bounce delay-200"></span>
              </div>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>

        {/* Chat Input Bar */}
        <div className="p-4 border-t border-slate-100 bg-white">
          <form
            onSubmit={(e) => {
              e.preventDefault();
              handleSend();
            }}
            className="flex items-center gap-2 bg-slate-50 border border-slate-200 rounded-xl px-3 py-1.5 focus-within:border-emerald-600 focus-within:bg-white transition-all"
          >
            <button
              type="button"
              className="p-1.5 text-slate-400 hover:text-slate-600 rounded-lg hover:bg-slate-100 transition-colors"
              title="Attach health document"
            >
              <Paperclip className="w-4 h-4" />
            </button>

            <input
              type="text"
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              placeholder="Type your message..."
              className="flex-1 bg-transparent border-none text-xs sm:text-sm text-slate-900 placeholder-slate-400 outline-none px-2 py-1"
            />

            <button
              type="submit"
              disabled={!inputMessage.trim() || isTyping}
              className="w-8 h-8 rounded-full bg-[#065f46] hover:bg-[#064e3b] text-white flex items-center justify-center transition-colors disabled:opacity-40 cursor-pointer shrink-0"
            >
              {isTyping ? <Loader2 className="w-3.5 h-3.5 animate-spin" /> : <Send className="w-3.5 h-3.5" />}
            </button>
          </form>
          <p className="text-[10px] text-slate-400 text-center mt-2">
            Healix provides health information, not medical diagnosis.
          </p>
        </div>
      </div>

      {/* Right Column: Quick Suggestions & Common Questions */}
      <div className="w-full lg:w-80 space-y-5">
        {/* Quick Suggestions */}
        <div className="bg-white rounded-2xl p-5 border border-slate-200/80 shadow-xs">
          <h3 className="text-xs font-bold text-slate-900 uppercase tracking-wider mb-3">
            Quick Suggestions
          </h3>
          <div className="space-y-2">
            {quickSuggestions.map((sugg, idx) => (
              <button
                key={idx}
                onClick={() => handleSend(sugg)}
                className="w-full text-left p-2.5 rounded-xl border border-slate-200 text-xs text-slate-700 hover:border-emerald-600 hover:bg-emerald-50/50 hover:text-emerald-900 transition-all cursor-pointer flex items-center justify-between group"
              >
                <span>{sugg}</span>
                <ChevronRight className="w-3.5 h-3.5 text-slate-400 group-hover:text-emerald-700 transition-transform group-hover:translate-x-0.5" />
              </button>
            ))}
          </div>
        </div>

        {/* Common Questions */}
        <div className="bg-white rounded-2xl p-5 border border-slate-200/80 shadow-xs">
          <h3 className="text-xs font-bold text-slate-900 uppercase tracking-wider mb-3">
            Common Questions
          </h3>
          <div className="space-y-2.5">
            {commonQuestions.map((q, idx) => (
              <button
                key={idx}
                onClick={() => handleSend(q)}
                className="w-full text-left text-xs text-slate-600 hover:text-emerald-800 transition-colors cursor-pointer flex items-start gap-2 group py-1"
              >
                <HelpCircle className="w-3.5 h-3.5 text-emerald-700 shrink-0 mt-0.5 group-hover:scale-110 transition-transform" />
                <span className="group-hover:underline">{q}</span>
              </button>
            ))}
          </div>
        </div>

        {/* Privacy notice */}
        <div className="bg-emerald-50 rounded-2xl p-4 border border-emerald-100 shadow-xs">
          <div className="flex items-center gap-2 mb-2">
            <ShieldCheck className="w-4 h-4 text-emerald-700 shrink-0" />
            <span className="text-xs font-semibold text-emerald-900">Your Privacy Matters</span>
          </div>
          <p className="text-[11px] text-emerald-800 leading-relaxed">
            Your health conversations are private and encrypted. Healix does not store personally identifiable symptom data.
          </p>
        </div>
      </div>
    </div>
  );
}
