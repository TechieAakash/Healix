import React, { useState } from "react";
import { Send, Mic, MicOff } from "lucide-react";

export function ChatInput({
  onSendMessage,
  disabled = false,
  placeholder = "Ask Healix about symptoms, warning signs, or health questions...",
}) {
  const [input, setInput] = useState("");
  const [isRecording, setIsRecording] = useState(false);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!input.trim() || disabled) return;
    onSendMessage(input.trim());
    setInput("");
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  const toggleVoiceInput = () => {
    if (!isRecording) {
      setIsRecording(true);
      // Simulate speech-to-text input
      setTimeout(() => {
        setInput((prev) => (prev ? `${prev} ` : "") + "Could my headache be caused by dehydration or screen fatigue?");
        setIsRecording(false);
      }, 1800);
    } else {
      setIsRecording(false);
    }
  };

  return (
    <form
      onSubmit={handleSubmit}
      className="relative flex items-center gap-2 bg-white rounded-2xl border border-slate-200/90 shadow-sm p-2 transition-all focus-within:border-teal-600 focus-within:ring-2 focus-within:ring-teal-500/10"
    >
      {/* Voice input button */}
      <button
        type="button"
        onClick={toggleVoiceInput}
        className={`p-2.5 rounded-xl transition-all cursor-pointer ${
          isRecording
            ? "bg-teal-100 text-teal-600 animate-pulse"
            : "text-slate-500 hover:text-slate-700 hover:bg-slate-100"
        }`}
        title={isRecording ? "Listening... click to stop" : "Use voice input"}
      >
        {isRecording ? <MicOff className="w-5 h-5 text-teal-600" /> : <Mic className="w-5 h-5" />}
      </button>

      {/* Text input */}
      <input
        type="text"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyDown={handleKeyDown}
        placeholder={isRecording ? "Listening to your voice..." : placeholder}
        disabled={disabled}
        className="flex-1 text-sm bg-transparent outline-none text-slate-800 placeholder:text-slate-500 py-1.5 px-1"
      />

      {/* Send button */}
      <button
        type="submit"
        disabled={!input.trim() || disabled}
        className="p-2.5 rounded-xl bg-slate-900 text-white hover:bg-teal-700 disabled:opacity-30 disabled:pointer-events-none transition-all cursor-pointer shadow-xs"
        title="Send message"
      >
        <Send className="w-4 h-4" />
      </button>
    </form>
  );
}
