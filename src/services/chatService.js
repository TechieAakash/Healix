import { mockChatSessions } from "../data/mockData";
import { apiRequest } from "./apiClient";

export const chatService = {
  getSessions() {
    try {
      const stored = localStorage.getItem("healix_chat_sessions");
      if (stored) {
        const parsed = JSON.parse(stored);
        if (Array.isArray(parsed) && parsed.length > 0) return parsed;
      }
    } catch (e) {
      console.error(e);
    }
    return mockChatSessions;
  },

  getSessionById(id) {
    const sessions = this.getSessions();
    return sessions.find((s) => s.id === id) || sessions[0];
  },

  async sendMessage(sessionId, messageText) {
    const apiRes = await apiRequest("/chat/message", {
      method: "POST",
      body: JSON.stringify({ sessionId, message: messageText }),
    });

    if (apiRes && apiRes.reply) {
      const reply = apiRes.reply;
      // Save message to current session in localStorage
      const sessions = this.getSessions();
      const updated = sessions.map((sess) => {
        if (sess.id === sessionId) {
          return {
            ...sess,
            messages: [
              ...sess.messages,
              {
                id: `user_${Date.now()}`,
                sender: "user",
                text: messageText,
                timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
              },
              reply,
            ],
          };
        }
        return sess;
      });
      localStorage.setItem("healix_chat_sessions", JSON.stringify(updated));
      return reply;
    }

    // Realistic intelligent medical information assistant simulation
    await new Promise((resolve) => setTimeout(resolve, 800));

    const lower = messageText.toLowerCase();
    let replyText = "";
    let sources = ["Mayo Clinic Clinical Compendium", "WHO Water Requirements", "NHS Evidence"];

    if (lower.includes("hydration") || lower.includes("dehydration") || lower.includes("water") || lower.includes("fluid") || lower.includes("drink")) {
      replyText = `**Clinical Guide to Hydration & Fluid Balance**:\n\nWater is essential for cellular metabolism, body temperature regulation, joint lubrication, cognitive focus, and cardiovascular perfusion.\n\n**1. Daily Fluid Intake Standards (WHO & Mayo Clinic)**:\n• **Adult Men**: ~3.7 liters (125 oz / ~15.5 cups) total fluid per day.\n• **Adult Women**: ~2.7 liters (91 oz / ~11.5 cups) total fluid per day.\n*(Note: ~20% of fluid comes naturally from water-dense foods; the remainder from beverages.)*\n\n**2. How to Monitor Your Hydration Status**:\n• **Urine Color Scale**: Optimal hydration produces light, pale straw yellow urine. Dark amber or tea-colored urine indicates concentrated fluid deficit.\n• **Thirst Perception**: Thirst is a delayed signal triggering after 1%–2% body mass fluid loss.\n• **Urination Frequency**: A well-hydrated individual typically urinates every 2 to 4 hours while awake.\n\n**3. Electrolytes & Safe Replenishment**:\n• Plain water restores fluid volume, but essential electrolytes (sodium, potassium, magnesium, chloride) maintain osmotic cellular balance.\n• During heat or illness, oral rehydration solutions (ORS) or electrolyte beverages help maintain stability and prevent hyponatremia.\n• Sip fluids steadily over hours rather than chugging large amounts at once.\n\n**4. Dehydration Signs to Watch For**:\n• **Mild Symptoms**: Dry mouth, dull tension headache, fatigue, dizziness upon standing, and reduced focus.\n• **Emergency Red Flags (Seek Immediate Medical Care)**: Sunken eyes, inability to retain oral fluids for >24 hours, absence of urination for >8 hours, rapid pulse, or confusion.\n\n*Healix provides health information and triage guidance, not a medical diagnosis.*`;
      sources = ["NHS Inform - Dehydration", "WHO Water Requirements", "Mayo Clinic Hydration"];
    } else if (lower.includes("doctor") || lower.includes("see a doctor") || lower.includes("when to see") || lower.includes("urgent")) {
      replyText = `You should consider consulting a physician or visiting an urgent care facility if:\n\n1. **Duration**: Symptoms persist steadily for more than 5–7 days without noticeable improvement.\n2. **Severity**: The discomfort begins interfering with sleep, eating, or normal daily activities.\n3. **Warning signs ('Red Flags')**: Sudden onset explosive pain ('worst headache of life'), high persistent fever, neck stiffness, confusion, or weakness on one side of the body.\n\n*Healix provides educational information and is not a substitute for clinical diagnosis.*`;
      sources = ["American College of Physicians Guidelines", "Mayo Clinic Triage"];
    } else if (lower.includes("track") || lower.includes("log") || lower.includes("information")) {
      replyText = `When preparing to speak with a healthcare provider, tracking these specific details provides tremendous diagnostic value:\n\n• **Onset & Duration**: Exactly when did it begin, and how many hours or days has it lasted?\n• **Character & Location**: Is the sensation throbbing, dull, burning, or sharp? Where is it centered?\n• **Triggers & Relievers**: Does it worsen after meals, screen exposure, or lack of sleep? Does rest or water relieve it?\n• **Severity scale**: Rate it from 1 (mild annoyance) to 10 (incapacitating).`;
      sources = ["CDC Patient-Provider Health History Guide"];
    } else if (lower.includes("tension") || lower.includes("stress")) {
      replyText = `Tension headaches are the most frequent headache type, characterized by dull, tight, band-like constriction around the forehead or occipital base of the skull.\n\nContributing factors include:\n• Sustained poor neck posture during computer or smartphone use\n• Mental tension and insufficient restorative REM sleep\n• Prolonged visual accommodation without taking screen breaks\n\nErgonomic resets, warm compresses across the back of the neck, and gentle cervical stretches frequently provide meaningful comfort.`;
      sources = ["American Migraine Foundation", "BMJ Best Practice"];
    } else {
      replyText = `Thank you for sharing that. When evaluating symptoms like these, clinicians examine several related factors:\n\n• **Progression**: Have the sensations been staying the same, fluctuating, or steadily intensifying?\n• **Context**: Are there recent lifestyle changes, elevated stress, new foods, or seasonal weather shifts?\n• **Associated indicators**: Are you noticing any concurrent sensations like digestive upset, sleep disruptions, or muscle tightness?\n\nIf you have a specific question about safe home management or warning signs to monitor, feel free to ask!`;
      sources = ["Mayo Clinic Evidence Base", "National Library of Medicine"];
    }

    const reply = {
      id: `msg_${Date.now()}`,
      sender: "assistant",
      text: replyText,
      timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
      sources,
    };

    // Save message to current session in localStorage
    const sessions = this.getSessions();
    const updated = sessions.map((sess) => {
      if (sess.id === sessionId) {
        return {
          ...sess,
          messages: [
            ...sess.messages,
            {
              id: `user_${Date.now()}`,
              sender: "user",
              text: messageText,
              timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
            },
            reply,
          ],
        };
      }
      return sess;
    });

    localStorage.setItem("healix_chat_sessions", JSON.stringify(updated));
    return reply;
  },

  createNewSession(initialTitle = "New Health Inquiry") {
    const newSession = {
      id: `sess_${Date.now()}`,
      title: initialTitle,
      date: "Today",
      messages: [
        {
          id: `msg_welcome_${Date.now()}`,
          sender: "assistant",
          text: "Hello! I'm Healix, your AI health information assistant. Describe what symptoms or health questions you're exploring today, and I'll help you understand relevant evidence-grounded information.\n\n*Reminder: Healix provides educational context and triage information, not medical diagnosis.*",
          timestamp: new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }),
          sources: ["Healix Clinical Information Core"],
        },
      ],
    };

    const sessions = this.getSessions();
    const updated = [newSession, ...sessions];
    localStorage.setItem("healix_chat_sessions", JSON.stringify(updated));
    return newSession;
  },
};
