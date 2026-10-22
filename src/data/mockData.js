// Realistic, clinically-reviewed structure mock data for Healix

export const mockUser = {
  id: "usr_99814",
  name: "Krrish",
  fullName: "Krish Alagh",
  email: "krish@example.com",
  dateOfBirth: "15 Jan 2006",
  gender: "Male",
  bloodGroup: "O+",
  height: "178 cm",
  weight: "72 kg",
  avatarInitials: "KA",
  metrics: {
    heartRate: "72 bpm",
    heartRateRange: "Normal range: 60 - 100",
    spo2: "98%",
    spo2Range: "Normal range: 95 - 100",
    sleep: "7h 42m",
    sleepSub: "Last night",
    steps: "8,432",
    stepsSub: "Today",
    weight: "72 kg",
    healthScore: 82,
    healthStatus: "Good",
    healthNote: "Your health is on track!"
  },
  emergencyContact: {
    name: "Priya Alagh",
    relation: "Sister",
    phone: "+1 (555) 349-8821"
  },
  settings: {
    saveHistory: true,
    personalizeInsights: true,
    emailAlerts: true,
    assessmentReminders: true,
    language: "en"
  }
};

export const commonSymptomChips = [
  { id: "headache", label: "Headache", category: "Head & Neurological" },
  { id: "fatigue", label: "Fatigue", category: "General" },
  { id: "fever", label: "Fever", category: "General" },
  { id: "cough", label: "Cough", category: "Respiratory" },
  { id: "sore-throat", label: "Sore Throat", category: "Ear, Nose, Throat" },
  { id: "nausea", label: "Nausea", category: "Digestive" },
  { id: "stomach-pain", label: "Stomach Pain", category: "Digestive" },
  { id: "dizziness", label: "Dizziness", category: "Head & Neurological" },
  { id: "joint-pain", label: "Joint Stiffness", category: "Musculoskeletal" },
  { id: "shortness-of-breath", label: "Shortness of Breath", category: "Respiratory", redFlagWarning: true },
  { id: "chest-discomfort", label: "Chest Discomfort", category: "Cardiovascular", redFlagWarning: true },
];

export const bodyAreas = [
  { id: "head", label: "Head & Face", icon: "Brain", description: "Headaches, dizziness, facial pain" },
  { id: "throat", label: "Neck & Throat", icon: "Mic", description: "Sore throat, swollen glands, neck stiffness" },
  { id: "chest", label: "Chest & Heart", icon: "Heart", description: "Chest tightness, palpitation, breathing" },
  { id: "abdomen", label: "Abdomen & Stomach", icon: "Shield", description: "Cramps, nausea, digestion, sharp pain" },
  { id: "back", label: "Spine & Back", icon: "Activity", description: "Upper back, lumbar ache, posture stiffness" },
  { id: "limbs", label: "Arms & Legs", icon: "Move", description: "Joint aches, muscle sprains, numbness" },
  { id: "general", label: "Whole Body / Systemic", icon: "User", description: "Fever, fatigue, chills, overall weakness" },
];

export const mockAssessments = [
  {
    id: "asm_101",
    date: "Today, Oct 2, 2026",
    timestamp: "2026-10-02T09:30:00Z",
    symptoms: ["Headache", "Fatigue", "Mild screen sensitivity"],
    primarySymptom: "Headache & fatigue",
    bodyArea: "head",
    duration: "Few days (3 days)",
    severity: "Mild to Moderate",
    frequency: "Comes and goes",
    urgencyLevel: "routine", // 'routine' | 'urgent' | 'emergency'
    urgencyTitle: "Routine Care Recommended",
    urgencyDescription: "Your symptoms appear manageable at home, but discuss them with your general practitioner if they persist beyond another week.",
    status: "Completed",
    followUpSummary: [
      { question: "Have you experienced any sudden vision loss or numbness?", answer: "No" },
      { question: "Are you drinking adequate fluids (at least 2L daily)?", answer: "Not sure / less than usual" },
      { question: "Have you noticed stiff neck preventing chin-to-chest touch?", answer: "No" },
      { question: "Has sleep quality declined over the last 72 hours?", answer: "Yes, slept under 5 hours" }
    ],
    possibleExplanations: [
      {
        title: "Tension-type Headache",
        matchLevel: "High Relevance",
        description: "The most common form of headache, typically presenting as a dull, aching sensation around the forehead or back of the head. Often triggered by stress, screen fatigue, or poor neck posture.",
        matchedSymptoms: ["Headache", "Fatigue", "Screen sensitivity"],
        clinicalInsight: "Characteristically bilateral and non-throbbing, responsive to rest and hydration."
      },
      {
        title: "Mild Dehydration & Sleep Debt",
        matchLevel: "Moderate Relevance",
        description: "Inadequate fluid intake combined with disrupted sleep reduces cerebral vascular compliance and energy balance, precipitating both head heaviness and persistent daytime tiredness.",
        matchedSymptoms: ["Fatigue", "Headache"],
        clinicalInsight: "Typically improves within 2–4 hours of gradual rehydration and restorative rest."
      },
      {
        title: "Digital Eye Strain (Asthenopia)",
        matchLevel: "Possible Factor",
        description: "Prolonged uninterrupted screen engagement causes ciliary muscle fatigue, triggering radiating brow aches and generalized mental fatigue.",
        matchedSymptoms: ["Headache", "Screen sensitivity"],
        clinicalInsight: "Commonly relieved by adopting the 20-20-20 visual hygiene rule."
      }
    ],
    selfCareGuidance: [
      "Hydrate proactively with 500ml water accompanied by light electrolytes.",
      "Practice the 20-20-20 rule: every 20 minutes look at something 20 feet away for 20 seconds.",
      "Take a 15-minute screen-free break in a dim, well-ventilated room.",
      "Maintain a consistent sleep window tonight aiming for 7–8 hours of restorative rest."
    ],
    warningSignsToWatch: [
      "Headache described as the 'worst headache of your life' (sudden thunderclap onset)",
      "High fever combined with neck stiffness or inability to touch chin to chest",
      "New weakness, numbness, difficulty speaking, or visual disturbance",
      "Persistent nausea with repetitive vomiting"
    ],
    sources: [
      {
        name: "Mayo Clinic",
        topic: "Tension Headaches: Symptoms & Causes",
        url: "https://www.mayoclinic.org/diseases-conditions/tension-headache",
        retrievalDate: "October 2026",
        authority: "Reviewed by Mayo Clinic Neurological Team"
      },
      {
        name: "World Health Organization (WHO)",
        topic: "Headache Disorders Fact Sheet",
        url: "https://www.who.int/news-room/fact-sheets/detail/headache-disorders",
        retrievalDate: "2026",
        authority: "Global Health Observatory"
      },
      {
        name: "National Health Service (NHS)",
        topic: "Headaches & Dehydration",
        url: "https://www.nhs.uk/conditions/headaches/",
        retrievalDate: "September 2026",
        authority: "NHS Clinical Guidelines"
      }
    ]
  },
  {
    id: "asm_102",
    date: "Sep 24, 2026",
    timestamp: "2026-09-24T14:15:00Z",
    symptoms: ["Persistent dry cough", "Sinus pressure", "Mild throat scratchiness"],
    primarySymptom: "Dry cough & sinus pressure",
    bodyArea: "throat",
    duration: "1–2 weeks",
    severity: "Mild",
    frequency: "Constant during mornings",
    urgencyLevel: "routine",
    urgencyTitle: "Routine Primary Care",
    urgencyDescription: "Typical viral upper-respiratory post-nasal drip profile. Schedule a routine doctor check if symptoms surpass 14 continuous days.",
    status: "Completed",
    possibleExplanations: [
      {
        title: "Post-Viral Upper Airway Cough Syndrome",
        matchLevel: "High Relevance",
        description: "Lingering cough stimulated by post-nasal drainage following a mild seasonal viral exposure.",
        matchedSymptoms: ["Cough", "Sinus pressure"],
        clinicalInsight: "Frequently self-limiting within 2 to 3 weeks."
      },
      {
        title: "Seasonal Allergic Rhinitis",
        matchLevel: "Moderate Relevance",
        description: "Allergen-induced inflammation of nasal mucosal tissues causing localized pressure and airway reactivity.",
        matchedSymptoms: ["Sinus pressure", "Throat scratchiness"],
        clinicalInsight: "Often exacerbated by environmental air quality or dust."
      }
    ],
    selfCareGuidance: [
      "Use warm saline nasal rinse or steam inhalation twice daily.",
      "Stay hydrated with warm teas containing honey (for adults) or clear broths.",
      "Use an elevated pillow arrangement while sleeping to reduce drainage irritation."
    ],
    warningSignsToWatch: [
      "Difficulty catching breath or wheezing sounds while resting",
      "Coughing up rust-colored or bloody sputum",
      "Fever exceeding 38.5°C (101.3°F) that does not break with antipyretics"
    ],
    sources: [
      {
        name: "American Academy of Family Physicians",
        topic: "Managing Persistent Cough in Adults",
        url: "https://www.aafp.org/pubs/afp/issues/2024",
        retrievalDate: "2026",
        authority: "AAFP Evidence-Based Medicine"
      }
    ]
  },
  {
    id: "asm_103",
    date: "Aug 15, 2026",
    timestamp: "2026-08-15T19:00:00Z",
    symptoms: ["Lower abdominal tenderness", "Low-grade fever", "Loss of appetite"],
    primarySymptom: "Abdominal tenderness & low fever",
    bodyArea: "abdomen",
    duration: "Today (8 hours)",
    severity: "Moderate",
    frequency: "Constant and worsening",
    urgencyLevel: "urgent",
    urgencyTitle: "Urgent Medical Attention Advised",
    urgencyDescription: "New onset progressive abdominal tenderness with systemic fever warrants an in-person clinical evaluation within 6–12 hours.",
    status: "Completed",
    possibleExplanations: [
      {
        title: "Localized Peritoneal / Gastrointestinal Irritation",
        matchLevel: "Requires Evaluation",
        description: "Persistent abdominal pain that increases over hours and is accompanied by fever requires physical palpation and routine laboratory investigation by a licensed physician.",
        matchedSymptoms: ["Abdominal tenderness", "Fever", "Loss of appetite"],
        clinicalInsight: "Differential diagnostics include acute appendicitis, diverticular flare, or infectious gastroenteritis."
      }
    ],
    selfCareGuidance: [
      "Avoid eating heavy solid food or taking NSAIDs like ibuprofen until clinically evaluated.",
      "Rest comfortably in a relaxed position with knees slightly bent to relieve abdominal wall tension.",
      "Proceed to an urgent care clinic or outpatient medical facility for an evaluation."
    ],
    warningSignsToWatch: [
      "Pain abruptly shifting to severe, unbearable intensity",
      "Inability to tolerate any sips of water or uncontrolled vomiting",
      "Rigid, board-like abdomen tender to the lightest touch"
    ],
    sources: [
      {
        name: "Mayo Clinic",
        topic: "Abdominal Pain: Triage Guidelines",
        url: "https://www.mayoclinic.org/symptoms/abdominal-pain",
        retrievalDate: "2026",
        authority: "Mayo Clinic Emergency Medicine"
      }
    ]
  }
];

export const mockHealthActivityData = [
  { week: "Week 1", checkins: 1, fatigueLevel: 3, painIntensity: 2 },
  { week: "Week 2", checkins: 0, fatigueLevel: 2, painIntensity: 1 },
  { week: "Week 3", checkins: 2, fatigueLevel: 4, painIntensity: 3 },
  { week: "Week 4", checkins: 1, fatigueLevel: 3, painIntensity: 2 },
  { week: "Week 5", checkins: 3, fatigueLevel: 5, painIntensity: 4 },
  { week: "Week 6", checkins: 1, fatigueLevel: 2, painIntensity: 1 },
  { week: "Week 7", checkins: 2, fatigueLevel: 4, painIntensity: 3 },
  { week: "Week 8", checkins: 2, fatigueLevel: 3, painIntensity: 2 },
];

export const mockChatSessions = [
  {
    id: "sess_01",
    title: "Understanding Tension Headaches",
    date: "Today, 10:15 AM",
    messages: [
      {
        id: "msg_1",
        sender: "user",
        text: "I've had a headache since yesterday and feel unusually tired.",
        timestamp: "10:15 AM"
      },
      {
        id: "msg_2",
        sender: "assistant",
        text: "I can help you understand what information may be relevant to discuss with a healthcare provider. \n\nTo give you the most accurate context, could you tell me:\n1. Where do you feel the headache most (e.g. across your forehead, one side, or back of the neck)?\n2. Does it feel like a dull band of pressure, or more like a pulsing throb?",
        timestamp: "10:15 AM",
        sources: ["Mayo Clinic - Headache Classifications", "NHS Clinical Knowledge"]
      },
      {
        id: "msg_3",
        sender: "user",
        text: "It feels like a tight band across my forehead, and my neck feels stiff from staring at my laptop.",
        timestamp: "10:17 AM"
      },
      {
        id: "msg_4",
        sender: "assistant",
        text: "Thank you for that description. A steady, band-like tightness around the forehead frequently aligns with what clinicians describe as a **tension-type headache**, often aggravated by prolonged posture strain and digital eye fatigue.\n\nHere are gentle, safe actions often recommended for self-care:\n- **Visual respite**: Step away from backlit screens for 15–20 minutes in natural or indirect light.\n- **Hydration**: Drink 1–2 glasses of water, as mild dehydration commonly amplifies head pressure.\n- **Neck relaxation**: Gently roll your shoulders backwards and tilt your ear toward each shoulder.\n\n*Note: If your headache ever becomes sudden and explosive ('thunderclap'), or is paired with high fever and neck stiffness preventing your chin from touching your chest, seek urgent medical evaluation immediately.*",
        timestamp: "10:18 AM",
        sources: ["American Migraine Foundation", "World Health Organization"]
      }
    ]
  },
  {
    id: "sess_02",
    title: "Post-nasal Drip & Night Cough",
    date: "Sep 25, 2026",
    messages: [
      {
        id: "msg_21",
        sender: "user",
        text: "Why does my dry cough get worse right when I lie down to sleep?",
        timestamp: "9:40 PM"
      },
      {
        id: "msg_22",
        sender: "assistant",
        text: "When you lie flat on your back, gravity no longer assists in moving natural nasal secretions down the throat effortlessly. Instead, post-nasal secretions pool near the laryngeal nerves at the back of the throat, triggering the cough reflex.\n\nElevating your head with an extra pillow and keeping bedroom humidity between 40–50% can noticeably decrease overnight tickling.",
        timestamp: "9:41 PM",
        sources: ["AAFP Cough Guidelines"]
      }
    ]
  }
];

export const redFlagTriggers = [
  "crushing chest pain",
  "pain radiating to left arm",
  "shortness of breath at rest",
  "sudden facial drooping",
  "sudden arm weakness",
  "slurred speech",
  "thunderclap headache",
  "coughing up blood",
  "uncontrolled bleeding",
  "sudden loss of vision"
];
