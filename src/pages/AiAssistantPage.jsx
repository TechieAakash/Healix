import React, { useState, useEffect, useRef } from "react";
import { chatService } from "../services/chatService";
import { ChatMessage } from "../components/chat/ChatMessage";
import { ChatInput } from "../components/chat/ChatInput";
import { SuggestedQuestions } from "../components/chat/SuggestedQuestions";
import { Button } from "../components/common/Button";
import {
  Bot,
  Plus,
  MessageSquare,
  ShieldCheck,
  Sparkles,
  Trash2,
  Clock,
} from "lucide-react";

export function AiAssistantPage() {
  const [sessions, setSessions] = useState([]);
  const [activeSessionId, setActiveSessionId] = useState(null);
  const [currentSession, setCurrentSession] = useState(null);
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef(null);

  useEffect(() => {
    const list = chatService.getSessions();
    setSessions(list);
    if (list.length > 0) {
      setActiveSessionId(list[0].id);
      setCurrentSession(list[0]);
    }
  }, []);

  useEffect(() => {
    if (activeSessionId) {
      const sess = chatService.getSessionById(activeSessionId);
      setCurrentSession(sess);
    }
  }, [activeSessionId]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [currentSession?.messages, isTyping]);

  const handleSelectSession = (id) => {
    setActiveSessionId(id);
  };

  const handleNewChat = () => {
    const newSess = chatService.createNewSession("New Health Inquiry");
    setSessions(chatService.getSessions());
    setActiveSessionId(newSess.id);
  };

  const handleSendMessage = async (text) => {
    if (!activeSessionId) return;

    // Optimistic local add
    const userMsg = {
      id: `usr_${Date.now()}`,
      sender: "user",
      text,
      timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
    };

    setCurrentSession((prev) => ({
      ...prev,
      messages: [...(prev?.messages || []), userMsg],
    }));

    setIsTyping(true);

    try {
      const reply = await chatService.sendMessage(activeSessionId, text);
      const updatedSess = chatService.getSessionById(activeSessionId);
      setCurrentSession(updatedSess);
      setSessions(chatService.getSessions());
    } catch (err) {
      console.error(err);
    } finally {
      setIsTyping(false);
    }
  };

  return (
    <div className="h-[calc(100vh-8.5rem)] flex rounded-3xl bg-white border border-slate-200 shadow-sm overflow-hidden">
      {/* ================= LEFT CONVERSATION SESSIONS SIDEBAR ================= */}
      <div className="w-72 border-r border-slate-200/80 bg-slate-50/60 hidden md:flex flex-col justify-between p-4">
        <div>
          <div className="flex items-center justify-between pb-3 mb-3 border-b border-slate-200">
            <div className="flex items-center gap-2">
              <MessageSquare className="w-4 h-4 text-teal-600" />
              <span className="text-xs font-bold uppercase tracking-wider text-slate-700">
                Health Dialogues
              </span>
            </div>
            <button
              onClick={handleNewChat}
              className="p-1.5 rounded-lg bg-teal-600 text-white hover:bg-teal-700 transition-colors shadow-xs cursor-pointer"
              title="Start New Chat"
            >
              <Plus className="w-4 h-4" />
            </button>
          </div>

          {/* Session List */}
          <div className="space-y-1.5 overflow-y-auto max-h-[calc(100vh-16rem)] pr-1">
            {sessions.map((sess) => {
              const isActive = sess.id === activeSessionId;
              return (
                <button
                  key={sess.id}
                  onClick={() => handleSelectSession(sess.id)}
                  className={`w-full text-left p-3 rounded-xl transition-all cursor-pointer block ${
                    isActive
                      ? "bg-white text-slate-900 border border-slate-200/90 shadow-xs font-semibold"
                      : "text-slate-600 hover:bg-slate-100 hover:text-slate-900"
                  }`}
                >
                  <p className="text-xs truncate">{sess.title}</p>
                  <div className="flex items-center gap-1.5 mt-1 text-[10px] text-slate-400">
                    <Clock className="w-3 h-3" />
                    <span>{sess.date}</span>
                  </div>
                </button>
              );
            })}
          </div>
        </div>

        {/* Clinical Disclaimer footer */}
        <div className="p-3 bg-white rounded-xl border border-slate-200/80 text-[11px] text-slate-500 leading-snug">
          <div className="flex items-center gap-1.5 font-bold text-slate-700 mb-1">
            <ShieldCheck className="w-3.5 h-3.5 text-teal-600" />
            <span>Educational AI</span>
          </div>
          Healix provides clinical information and triage, not medical diagnosis.
        </div>
      </div>

      {/* ================= RIGHT MAIN CHAT INTERFACE ================= */}
      <div className="flex-1 flex flex-col justify-between bg-white min-w-0">
        {/* Chat top header */}
        <div className="px-6 py-4 border-b border-slate-100 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-9 h-9 rounded-xl bg-teal-600 text-white flex items-center justify-center shadow-xs">
              <Bot className="w-5 h-5" />
            </div>
            <div>
              <h2 className="text-sm font-bold text-slate-900 flex items-center gap-2">
                Healix Clinical Assistant
                <span className="w-2 h-2 rounded-full bg-emerald-500"></span>
              </h2>
              <p className="text-xs text-slate-500">
                Evidence-grounded medical Q&A and symptom triage assistance
              </p>
            </div>
          </div>

          <div className="hidden sm:flex items-center gap-2 text-xs text-slate-400">
            <ShieldCheck className="w-4 h-4 text-teal-600" />
            <span>Curated Sources Active</span>
          </div>
        </div>

        {/* Messages Stream */}
        <div className="flex-1 overflow-y-auto p-4 sm:p-6 space-y-4">
          {currentSession?.messages?.map((msg) => (
            <ChatMessage key={msg.id} message={msg} />
          ))}

          {/* Assistant typing indicator */}
          {isTyping && (
            <div className="flex items-center gap-2 text-xs text-slate-400 p-2 pl-4">
              <div className="w-2 h-2 rounded-full bg-teal-500 animate-bounce" />
              <div className="w-2 h-2 rounded-full bg-teal-500 animate-bounce [animation-delay:0.2s]" />
              <div className="w-2 h-2 rounded-full bg-teal-500 animate-bounce [animation-delay:0.4s]" />
              <span className="ml-1 text-slate-500 font-medium">Healix is consulting clinical sources...</span>
            </div>
          )}

          <div ref={messagesEndRef} />
        </div>

        {/* Input Bar & Suggested Questions */}
        <div className="p-4 sm:p-6 border-t border-slate-100 space-y-3 bg-slate-50/50">
          <SuggestedQuestions
            onSelectQuestion={(q) => handleSendMessage(q)}
          />

          <ChatInput
            onSendMessage={handleSendMessage}
            disabled={isTyping}
            placeholder="Ask Healix (e.g. Could it be dehydration? When should I see a doctor?)..."
          />

          {/* Persistent safety disclaimer */}
          <div className="text-center text-[11px] text-slate-400 flex items-center justify-center gap-1">
            <ShieldCheck className="w-3.5 h-3.5 text-slate-400" />
            <span>Healix provides health information, not medical diagnosis. In an emergency, dial 911 or 112 immediately.</span>
          </div>
        </div>
      </div>
    </div>
  );
}
