"""
LLM Provider Implementations.
Supports MockLLMProvider for offline/testing/dev and OpenAILLMProvider
for live production LLM integration via robust HTTP client with retries.
"""

import json
import logging
import re
from typing import List, Dict, Any, Optional, Type, TypeVar
import httpx
from pydantic import BaseModel, ValidationError

from app.core.config import settings
from app.services.ai.llm.base import BaseLLMProvider, LLMResponse, LLMUsage
from app.core.exceptions import AIException

logger = logging.getLogger("healix.ai.llm")
T = TypeVar("T", bound=BaseModel)


class LLMProviderException(AIException):
    """Raised when an LLM provider encounters unrecoverable failure."""
    def __init__(self, message: str, status_code: int = 502):
        super().__init__(message=message, status_code=status_code)


class MockLLMProvider(BaseLLMProvider):
    """
    Realistic healthcare mock provider for development, tests, and offline mode.
    Understands Healix schemas and generates high-fidelity medical information.
    """

    def __init__(self, model_name: str = "mock-healix-v1"):
        self.model_name = model_name

    async def generate_text(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ) -> LLMResponse:
        prompt_lower = prompt.lower()
        if "emergency" in prompt_lower or "chest pain" in prompt_lower:
            text = (
                "These symptoms may represent a time-sensitive medical situation. "
                "Immediate medical evaluation at an emergency department or urgent care facility is advised."
            )
        elif "headache" in prompt_lower:
            text = (
                "Cranial tension, dehydration, or sustained eye fatigue often manifest as dull headaches. "
                "Adequate rest, consistent hydration, and reducing screen glare can often assist in symptom monitoring."
            )
        else:
            text = (
                "Your reported symptoms have been categorized for clinical context. "
                "Keep track of symptom duration and seek clinical evaluation if they intensify."
            )

        return LLMResponse(
            text=text,
            usage=LLMUsage(prompt_tokens=len(prompt) // 4, completion_tokens=len(text) // 4, total_tokens=(len(prompt) + len(text)) // 4),
            model=self.model_name,
            finish_reason="stop",
        )

    async def generate_structured(
        self,
        schema: Type[T],
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        max_retries: int = 2,
    ) -> T:
        prompt_lower = prompt.lower()
        schema_name = schema.__name__.lower()

        # Dynamic mock generation tailored to Healix schemas
        if "symptom" in schema_name and "extract" in schema_name or "symptomextraction" in schema_name:
            mock_data = self._mock_symptom_extraction(prompt_lower)
        elif "followup" in schema_name or "question" in schema_name:
            mock_data = self._mock_follow_up_questions(prompt_lower)
        elif "analysis" in schema_name or "symptomanalysis" in schema_name:
            mock_data = self._mock_symptom_analysis(prompt_lower)
        elif "summary" in schema_name or "healthsummary" in schema_name:
            mock_data = self._mock_health_summary(prompt_lower)
        else:
            # Generic fallback mock
            mock_data = {}

        try:
            return schema.model_validate(mock_data)
        except ValidationError as err:
            logger.warning("Mock LLM validation failed: %s. Using default empty construct.", err)
            # Try instantiation with empty dict or defaults
            try:
                return schema()
            except Exception:
                raise LLMProviderException(f"Failed to generate valid mock structured output for {schema.__name__}")

    def _mock_symptom_extraction(self, prompt_lower: str) -> Dict[str, Any]:
        symptoms = []
        associated = []

        if "headache" in prompt_lower or "head" in prompt_lower:
            loc = "right side" if "right side" in prompt_lower else ("left side" if "left side" in prompt_lower else "bilateral")
            dur = "1 day" if "yesterday" in prompt_lower or "1 day" in prompt_lower else "recent"
            symptoms.append({
                "name": "headache",
                "location": loc,
                "severity": "moderate" if "severe" not in prompt_lower else "severe",
                "duration": dur,
                "extraction_type": "explicit",
            })
        if "nausea" in prompt_lower or "nauseous" in prompt_lower or "queasy" in prompt_lower or "vomit" in prompt_lower:
            symptoms.append({
                "name": "nausea",
                "location": "systemic",
                "severity": "mild",
                "duration": "unspecified",
                "extraction_type": "explicit",
            })
        if "light" in prompt_lower or "photophobia" in prompt_lower:
            associated.append("photophobia / light sensitivity")
        if "chest" in prompt_lower:
            symptoms.append({
                "name": "chest discomfort",
                "location": "retrosternal",
                "severity": "moderate",
                "duration": "hours",
                "extraction_type": "explicit",
            })
        if "fever" in prompt_lower:
            symptoms.append({
                "name": "fever",
                "location": "systemic",
                "severity": "moderate",
                "duration": "recent",
                "extraction_type": "explicit",
            })

        if not symptoms:
            symptoms.append({
                "name": "general discomfort",
                "location": "unspecified",
                "severity": "mild",
                "duration": "unspecified",
                "extraction_type": "explicit",
            })

        return {
            "symptoms": symptoms,
            "associated_features": associated,
            "raw_input_summary": "Extracted key clinical features and symptom trajectory from patient description.",
        }

    def _mock_follow_up_questions(self, prompt_lower: str) -> Dict[str, Any]:
        questions = []
        if "headache" in prompt_lower or "head" in prompt_lower:
            questions = [
                {
                    "question": "How severe is the headache on a scale from 0 to 10?",
                    "type": "single_choice",
                    "reasoning": "Clarify severity level to distinguish mild tension from severe acute pain.",
                    "order_index": 0,
                    "options": ["1-3 (Mild)", "4-6 (Moderate)", "7-9 (Severe)", "10 (Worst headache of life)"],
                },
                {
                    "question": "Did the headache begin suddenly within seconds, or build up gradually?",
                    "type": "single_choice",
                    "reasoning": "Identify sudden thunderclap onset requiring emergency neurological evaluation.",
                    "order_index": 1,
                    "options": ["Built up gradually", "Started over a few hours", "Sudden explosive onset within seconds"],
                },
                {
                    "question": "Do you have neck stiffness or difficulty bending your chin to your chest?",
                    "type": "single_choice",
                    "reasoning": "Rule out meningeal irritation warning signs.",
                    "order_index": 2,
                    "options": ["No neck stiffness", "Mild muscle soreness", "Significant stiffness and inability to touch chin to chest"],
                },
            ]
        elif "chest" in prompt_lower:
            questions = [
                {
                    "question": "Does the discomfort radiate to your arm, neck, shoulder, or jaw?",
                    "type": "single_choice",
                    "reasoning": "Screen for radiation patterns associated with acute coronary syndromes.",
                    "order_index": 0,
                    "options": ["No radiation", "Radiates to left arm or jaw", "Radiates to back"],
                },
                {
                    "question": "Are you experiencing shortness of breath, dizziness, or cold sweating?",
                    "type": "single_choice",
                    "reasoning": "Screen for autonomic and cardiopulmonary distress indicators.",
                    "order_index": 1,
                    "options": ["None of these", "Mild shortness of breath", "Sweating and significant breathlessness"],
                },
            ]
        else:
            questions = [
                {
                    "question": "How many days have you been experiencing these symptoms?",
                    "type": "single_choice",
                    "reasoning": "Establish clinical timeline.",
                    "order_index": 0,
                    "options": ["Less than 24 hours", "1 to 3 days", "4 to 7 days", "More than a week"],
                },
                {
                    "question": "Have your symptoms been steadily improving, remaining the same, or worsening?",
                    "type": "single_choice",
                    "reasoning": "Evaluate symptom progression.",
                    "order_index": 1,
                    "options": ["Improving", "Staying about the same", "Steadily worsening"],
                },
            ]

        return {
            "questions": questions,
            "total_questions": len(questions),
            "safety_rationale": "Non-invasive follow-up inquiries targeted to rule out acute red flags.",
        }

    def _mock_symptom_analysis(self, prompt_lower: str) -> Dict[str, Any]:
        if "headache" in prompt_lower or "head" in prompt_lower:
            return {
                "symptoms": ["headache", "photophobia", "nausea"],
                "duration": ["1-2 days"],
                "severity": ["moderate"],
                "possible_explanations": [
                    {
                        "title": "Tension-type Headache",
                        "description": "Common headache pattern characterized by a continuous dull ache or band-like pressure, often triggered by physical or emotional stress, eye fatigue, or cervical muscle strain.",
                        "supporting_information": ["Gradual onset", "Moderate intensity without focal neurological deficits"],
                        "match_level": "High Relevance",
                    },
                    {
                        "title": "Migraine without Aura",
                        "description": "Recurrent headache disorder often unilateral or throbbing, frequently accompanied by sensitivity to ambient lighting and mild gastrointestinal unease.",
                        "supporting_information": ["Photophobia noted", "Mild nausea reported"],
                        "match_level": "Moderate Relevance",
                    },
                ],
                "follow_up_questions": [
                    "Has hydration or resting in a dark room offered relief?",
                    "Have you experienced any changes in vision or speech?",
                ],
                "warning_signs": [
                    "Sudden explosive thunderclap headache onset",
                    "Fever accompanied by severe neck rigidity",
                    "New neurological signs such as unilateral weakness or confusion",
                ],
                "general_guidance": [
                    "Rest in a quiet, dimly illuminated space.",
                    "Maintain steady hydration with oral fluids.",
                    "Limit prolonged exposure to bright display screens.",
                ],
                "uncertainties": [
                    "Individual pain thresholds and specific triggers require direct clinical interview for confirmation.",
                ],
            }
        else:
            return {
                "symptoms": ["general health complaint"],
                "duration": ["recent"],
                "severity": ["mild to moderate"],
                "possible_explanations": [
                    {
                        "title": "Transient Functional Discomfort",
                        "description": "Temporary physiological disturbance often precipitated by sleep irregularity, nutritional factors, or viral exposure.",
                        "supporting_information": ["Non-specific presentation without acute red-flag indicators"],
                        "match_level": "Common Consideration",
                    }
                ],
                "follow_up_questions": [
                    "Are there particular activities that aggravate or relieve your discomfort?",
                ],
                "warning_signs": [
                    "Severe unremitting pain",
                    "Difficulty breathing or chest tightness",
                    "Persistent high fever",
                ],
                "general_guidance": [
                    "Ensure adequate hydration and unhurried rest.",
                    "Monitor symptoms over the next 24 to 48 hours.",
                ],
                "uncertainties": [
                    "Clinical evaluation by a medical provider is required to determine the exact underlying etiology.",
                ],
            }

    def _mock_health_summary(self, prompt_lower: str) -> Dict[str, Any]:
        analysis = self._mock_symptom_analysis(prompt_lower)
        return {
            "summary": (
                "Review of reported symptoms indicates considerations such as "
                + ", ".join([e["title"] for e in analysis["possible_explanations"]])
                + ". Clinical examination is needed to confirm the cause."
            ),
            "reported_symptoms": analysis["symptoms"],
            "possible_explanations": analysis["possible_explanations"],
            "general_guidance": analysis["general_guidance"],
            "warning_signs": analysis["warning_signs"],
            "when_to_seek_care": [
                "Seek immediate emergency care if you experience sudden explosive pain, shortness of breath, or neurological deficits.",
                "Consult a primary care physician if symptoms persist beyond several days or interrupt regular sleep.",
            ],
            "limitations": [
                "Healix provides educational information and triage guidance, not clinical diagnosis.",
                "Assessment is based solely on user self-report without in-person physical examination or laboratory confirmation.",
            ],
        }

    async def generate_chat_response(
        self,
        messages: List[Dict[str, str]],
        system_prompt: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ) -> LLMResponse:
        last_msg = messages[-1]["content"] if messages else ""
        lower = last_msg.lower()

        # Extract actual user query text if formatted in user prompt template
        user_query_match = re.search(r"current user query:\s*<<<\s*(.*?)\s*>>>", lower, re.DOTALL)
        query_text = user_query_match.group(1).strip() if user_query_match else lower

        is_educational_antibiotic = any(phrase in query_text for phrase in [
            "why do antibiotic", "why don't antibiotic", "how do antibiotic", "what is antibiotic",
            "antibiotic resist", "antibiotics not work", "antibiotics against virus", "difference between viral",
            "antibiotics for viral", "antibiotics for cold", "antibiotics for flu"
        ])

        if not is_educational_antibiotic and any(term in query_text for term in [
            "prescribe", "prescription", "dose", "dosage", "how many mg", "stop taking", "start taking",
            "change my pill", "take this pill", "amoxicillin dose", "ibuprofen dose", "increase dose", "decrease dose"
        ]):
            reply = (
                "Healix cannot prescribe medication, calculate dosages, or advise altering prescribed treatment. "
                "Any questions regarding prescription medications or dosage adjustments must be directed to your prescribing doctor, pediatrician, or pharmacist.\n\n"
                "*Healix provides health information and triage guidance, not a medical diagnosis.*"
            )
        elif is_educational_antibiotic or (any(w in query_text for w in ["antibiotic", "amr", "resistance"]) and any(w in query_text for w in ["work", "virus", "viral", "cold", "flu", "why", "how", "what"])):
            reply = (
                "### Clinical & Educational Guide: How Antibiotics Work & Viral Distinctions\n\n"
                "**1. Why Antibiotics Have Zero Effect on Viruses**:\n"
                "• **Target Specificity**: Antibiotics are engineered specifically to disrupt structural components and biochemical pathways unique to bacteria — such as peptidoglycan cell walls, bacterial ribosomes, or bacterial DNA gyrase.\n"
                "• **Viral Biology**: Viruses do not have bacterial cell walls, protein synthesis machinery, or independent metabolic pathways. Viruses are genetic material (RNA or DNA) enclosed in a protein capsid that hide inside human host cells to replicate.\n"
                "• **Result**: Because viruses lack the biological targets that antibiotics attack, taking antibiotics for viral infections like the common cold, flu, COVID-19, or acute bronchitis provides zero therapeutic benefit.\n\n"
                "**2. Risks of Inappropriate Antibiotic Use**:\n"
                "• **Antimicrobial Resistance (AMR)**: Overusing antibiotics creates selective pressure that breeds drug-resistant bacterial strains, rendering future bacterial treatments ineffective.\n"
                "• **Adverse Effects & Microbiome Disruption**: Antibiotics destroy beneficial commensal bacteria in the gut, which can trigger severe diarrhea, fungal yeast overgrowth, or Clostridioides difficile colitis, as well as allergic reactions.\n\n"
                "**3. Evidence-Based Recovery for Viral Infections**:\n"
                "• Prioritize restful sleep to support cell-mediated immunity.\n"
                "• Maintain continuous hydration (warm teas, broth, water) to loosen mucous and replenish insensible sweat losses.\n"
                "• Use saline nasal sprays or honey and throat lozenges for symptomatic relief.\n\n"
                "**4. When to Consult a Clinician**:\n"
                "• If a suspected viral illness lasts longer than 10 to 14 days without improvement, or if you experience a 'double sickening' (feeling better, then abruptly developing a high fever and worsening productive cough), consult a physician to evaluate for a secondary bacterial complication (such as bacterial pneumonia or acute sinusitis).\n\n"
                "*Healix provides health information and triage guidance, not a medical diagnosis.*"
            )
        elif any(w in query_text for w in ["hydration", "dehydration", "water", "fluid", "fluids", "drink", "electrolyt"]):
            reply = (
                "### Clinical Guide to Hydration & Fluid Balance\n\n"
                "Water is essential for cellular metabolism, body temperature regulation, joint lubrication, cognitive focus, and cardiovascular perfusion.\n\n"
                "**1. Daily Recommended Fluid Intake (WHO & Mayo Clinic Standards)**:\n"
                "• **Adult Men**: ~3.7 liters (125 oz / ~15.5 cups) total fluids daily.\n"
                "• **Adult Women**: ~2.7 liters (91 oz / ~11.5 cups) total fluids daily.\n"
                "*(Note: About 20% of daily fluid intake naturally comes from water-rich foods such as vegetables and fruits; the remaining 80% comes from drinking water and other beverages.)*\n\n"
                "**2. How to Accurately Monitor Your Hydration Status**:\n"
                "• **Urine Color Scale**: Ideal hydration produces pale straw or light transparent yellow urine. Dark amber or brownish urine signals concentrated fluid deficit and mild-to-moderate dehydration.\n"
                "• **Thirst Perception**: Thirst is a delayed indicator, typically signaling that you have already lost 1% to 2% of your body's water volume.\n"
                "• **Urination Frequency**: A well-hydrated individual typically urinates every 2 to 4 hours while awake.\n\n"
                "**3. Electrolytes and Safe Replenishment**:\n"
                "• Plain water restores fluid volume, but essential electrolytes (sodium, potassium, chloride, magnesium) maintain osmotic balance within your cells.\n"
                "• When experiencing illness, prolonged sweating, or intense exercise, oral rehydration solutions (ORS) or electrolyte beverages help maintain electrolyte stability and prevent hyponatremia.\n"
                "• Replenish fluids steadily by sipping over several hours rather than consuming excessive volumes all at once.\n\n"
                "**4. Dehydration Signs & Warning Flags**:\n"
                "• **Mild-to-Moderate Symptoms**: Dry mouth, dull tension headache, fatigue, dizziness upon standing, and reduced concentration.\n"
                "• **Emergency Red Flags (Seek Immediate Medical Care)**: Extreme thirst with sunken eyes, inability to retain oral fluids for >24 hours, absence of urination for >8 hours, rapid pulse, low blood pressure, or confusion.\n\n"
                "*Healix provides health information and triage guidance, not a medical diagnosis.*"
            )
        elif any(w in query_text for w in ["diabet", "glucose", "sugar", "insulin", "hba1c"]):
            reply = (
                "### Clinical & Educational Guide: Diabetes Mellitus & Glucose Regulation\n\n"
                "**1. Pathophysiological Overview**:\n"
                "• **Type 1 Diabetes**: An autoimmune condition where the immune system destroys insulin-producing beta cells in the pancreas, leading to absolute insulin deficiency. It requires daily exogenous insulin replacement.\n"
                "• **Type 2 Diabetes**: Characterized by progressive peripheral insulin resistance coupled with relative secretory dysfunction by pancreatic beta cells. Cells in muscle, liver, and adipose tissue do not respond effectively to insulin.\n"
                "• **Prediabetes**: Blood glucose is higher than normal (fasting 100-125 mg/dL; HbA1c 5.7%-6.4%) but below diagnostic diabetes thresholds.\n\n"
                "**2. Glycemic Reference Standards (ADA Guidelines)**:\n"
                "• **Fasting Plasma Glucose**: Normal: <100 mg/dL | Prediabetes: 100-125 mg/dL | Diabetes: >=126 mg/dL\n"
                "• **HbA1c (Glycated Hemoglobin)**: Reflects average blood sugar over 2 to 3 months. Normal: <5.7% | Prediabetes: 5.7%-6.4% | Diabetes: >=6.5%\n\n"
                "**3. Evidence-Based Lifestyle & Management**:\n"
                "• Emphasize fiber-rich complex carbohydrates (legumes, oats, vegetables) and reduce refined sugars and sweetened drinks.\n"
                "• Engage in at least 150 minutes of moderate aerobic exercise plus 2 sessions of resistance training weekly to enhance cellular insulin sensitivity.\n"
                "• Conduct daily self-inspections of feet for blisters, cuts, or loss of sensation to prevent diabetic foot ulcers.\n\n"
                "**4. Critical Red Flags & When to Seek Care**:\n"
                "• **Hypoglycemia Alert (Blood Glucose <70 mg/dL)**: Shakiness, diaphoresis (sweating), rapid pulse, confusion. Treat immediately with the 15-15 rule (15g fast-acting carbs, re-check in 15 mins).\n"
                "• **Diabetic Ketoacidosis (DKA) / Hyperglycemic Emergency**: Fruity breath odor, deep rapid breathing, persistent vomiting, confusion, or blood glucose >300 mg/dL requires immediate emergency room care.\n\n"
                "*Healix provides health information and triage guidance, not a medical diagnosis.*"
            )
        elif any(w in query_text for w in ["blood pressure", "hypertension", "bp", "systolic", "diastolic"]):
            reply = (
                "### Clinical & Educational Guide: Blood Pressure & Cardiovascular Health\n\n"
                "**1. What Blood Pressure Measures**:\n"
                "Blood pressure represents the hydrostatic force circulating blood exerts against arterial walls.\n"
                "• **Systolic (Top number)**: Arterial pressure when the heart beats/contracts.\n"
                "• **Diastolic (Bottom number)**: Arterial pressure when the heart relaxes between contractions.\n\n"
                "**2. Clinical Classification Standards (AHA / ACC)**:\n"
                "• **Normal**: Systolic <120 mmHg AND Diastolic <80 mmHg\n"
                "• **Elevated**: Systolic 120-129 mmHg AND Diastolic <80 mmHg\n"
                "• **Stage 1 Hypertension**: Systolic 130-139 mmHg OR Diastolic 80-89 mmHg\n"
                "• **Stage 2 Hypertension**: Systolic >=140 mmHg OR Diastolic >=90 mmHg\n"
                "• **Hypertensive Crisis**: Systolic >180 mmHg and/or Diastolic >120 mmHg\n\n"
                "**3. Evidence-Based Lifestyle Interventions**:\n"
                "• **DASH Dietary Pattern**: Rich in fruits, vegetables, whole grains, and low-fat dairy while reducing saturated fats.\n"
                "• **Sodium Restriction**: Limit daily dietary sodium to under 2,000 mg (approx 1 teaspoon of table salt).\n"
                "• **Physical Conditioning**: 150 minutes per week of brisk walking, cycling, or swimming lowers systolic BP by 5-8 mmHg.\n"
                "• **Stress Reduction**: Diaphragmatic breathing and mindfulness lower sympathetic nervous vascular tone.\n\n"
                "**4. Warning Signs Requiring Immediate Medical Attention**:\n"
                "• Blood pressure >180/120 mmHg accompanied by chest pain, shortness of breath, blurry vision, severe headache, or numbness (hypertensive emergency requires immediate 911 / ER care).\n\n"
                "*Healix provides health information and triage guidance, not a medical diagnosis.*"
            )
        elif any(w in query_text for w in ["asthma", "inhaler", "wheez", "bronch", "airway"]):
            reply = (
                "### Clinical & Educational Guide: Asthma & Airway Health\n\n"
                "**1. Pathophysiology**:\n"
                "Asthma is a chronic inflammatory disorder of the bronchial airways characterized by episodic airway hyperreactivity, mucosal swelling, and smooth muscle bronchospasm.\n\n"
                "**2. Medication Categories**:\n"
                "• **Rescue / Reliever Bronchodilators (e.g. Albuterol)**: Rapidly relax smooth muscles around airways during acute flares within 5 to 15 minutes.\n"
                "• **Controller / Maintenance Anti-inflammatories (e.g. Inhaled Corticosteroids)**: Taken daily as prescribed to suppress baseline chronic inflammation and prevent future attacks.\n"
                "• **Inhaler Spacers**: Using a spacer significantly improves medication deposition deep into lung alveoli.\n\n"
                "**3. Common Triggers & Environmental Control**:\n"
                "• Aeroallergens (pollen, dust mites, pet dander), viral respiratory infections, cold dry air, strenuous exercise, and tobacco smoke.\n\n"
                "**4. Acute Red Flags Requiring Immediate Emergency Care**:\n"
                "• Inability to speak full sentences without pausing to breathe.\n"
                "• Paradoxical retractions of the ribs, neck, or abdomen during breathing.\n"
                "• Failure of rescue inhaler to relieve breathlessness within 15-20 minutes.\n"
                "• Bluish or grayish discoloration of the lips or nail beds.\n\n"
                "*Healix provides health information and triage guidance, not a medical diagnosis.*"
            )
        elif any(w in query_text for w in ["viral", "bacterial", "bacteria", "virus", "infection", "fever", "pyrogen", "antibiotic"]):
            reply = (
                "### Clinical & Educational Guide: Viral vs Bacterial Infections & Immune Response\n\n"
                "**1. Core Biological Distinctions**:\n"
                "• **Viruses**: Submicroscopic obligate intracellular entities that hijack host cells to replicate. Common viral infections include colds (rhinoviruses), influenza, COVID-19, and acute bronchitis. **Antibiotics have zero efficacy against viruses.**\n"
                "• **Bacteria**: Independent single-celled prokaryotic microorganisms that multiply extracellularly. Bacterial infections (e.g. strep throat, bacterial pneumonia, urinary tract infections) respond to clinician-prescribed antibiotics.\n\n"
                "**2. The Physiology of Fever**:\n"
                "• Core body temperature >38.0°C (100.4°F) is a protective hypothalamic adaptation mediated by endogenous pyrogens (interleukins, TNF) that impairs pathogen replication and mobilizes white blood cells.\n\n"
                "**3. Supportive Self-Care**:\n"
                "• Rest, consistent oral hydration (replenishing sweat losses), light clothing, and monitoring temperatures.\n\n"
                "**4. Critical Clinical Red Flags**:\n"
                "• **Neonatal Alert**: Any infant under 3 months with a fever >=38.0°C (100.4°F) requires emergency hospital evaluation.\n"
                "• Stiff neck (inability to touch chin to chest), confusion, petechial non-blanching purple rash, difficulty breathing, or fever >40.0°C (104.0°F).\n\n"
                "*Healix provides health information and triage guidance, not a medical diagnosis.*"
            )
        elif any(w in query_text for w in ["heartburn", "gerd", "acid reflux", "stomach acid", "reflux"]):
            reply = (
                "### Clinical & Educational Guide: GERD & Digestive Acid Regulation\n\n"
                "**1. Pathophysiology**:\n"
                "Gastroesophageal Reflux Disease occurs when the lower esophageal sphincter (LES) transiently relaxes or weakens, allowing hydrochloric acid and pepsin to reflux upward and irritate esophageal tissues.\n\n"
                "**2. Evidence-Based Lifestyle Measures**:\n"
                "• Avoid reclining or lying down for at least 3 hours following meals.\n"
                "• Elevate the head of the bed by 6 inches (using bed risers or a wedge pillow).\n"
                "• Reduce dietary triggers: caffeine, high-fat fried foods, citrus, tomatoes, mint, and alcohol.\n"
                "• Eat smaller, more frequent meals rather than large heavy dinners.\n\n"
                "**3. Critical Safety Warning (Angina vs Reflux)**:\n"
                "• Cardiac ischemia and heart attacks can mimic acid reflux. If chest discomfort presents as heavy pressure, squeezing, or radiates to the left arm, neck, or jaw with shortness of breath, seek emergency medical care (911) immediately.\n"
                "• Alarm GI features requiring clinical evaluation: difficulty swallowing (dysphagia), unexplained weight loss, vomiting blood, or black tarry stools.\n\n"
                "*Healix provides health information and triage guidance, not a medical diagnosis.*"
            )
        elif any(w in query_text for w in ["cholesterol", "lipid", "ldl", "hdl", "triglycerid"]):
            reply = (
                "### Clinical & Educational Guide: Cholesterol, Lipids & Cardiovascular Health\n\n"
                "**1. Lipoprotein Profiles**:\n"
                "• **LDL-C (Low-Density Lipoprotein)**: Known as 'atherogenic cholesterol'. Elevated circulating LDL particles penetrate arterial walls, oxidize, and build atherosclerotic plaques. Optimal level is <100 mg/dL.\n"
                "• **HDL-C (High-Density Lipoprotein)**: Participates in reverse cholesterol transport, shuttling surplus cholesterol back to the liver for excretion. Cardioprotective level is >=40 mg/dL (men) or >=50 mg/dL (women).\n"
                "• **Triglycerides**: The body's primary energy storage fat. Normal fasting level is <150 mg/dL.\n\n"
                "**2. Evidence-Based Dietary & Lifestyle Actions**:\n"
                "• Emphasize soluble fiber (oats, beans, lentils, psyllium), which binds bile acids and lowers circulating LDL.\n"
                "• Replace saturated fats with heart-healthy unsaturated fats (olive oil, avocados, nuts, omega-3 fatty fish).\n"
                "• Engage in regular aerobic exercise (150 mins/week) to raise HDL and improve vascular elasticity.\n\n"
                "*Healix provides health information and triage guidance, not a medical diagnosis.*"
            )
        elif any(w in query_text for w in ["first aid", "choking", "heimlich", "bleeding", "anaphylaxis"]):
            reply = (
                "### Clinical & Educational Guide: Emergency First Aid Fundamentals\n\n"
                "**1. Conscious Choking (Universal Sign / Inability to Speak or Breathe)**:\n"
                "• Deliver 5 back blows between the shoulder blades with the heel of the hand.\n"
                "• Perform 5 abdominal thrusts (Heimlich maneuver): place fist thumb-side against abdomen just above navel, grasp with other hand, thrust upward and inward. Repeat until airway is clear.\n"
                "• If patient loses consciousness: lower to floor, call 911, begin chest compressions (CPR).\n\n"
                "**2. Severe Bleeding Management**:\n"
                "• Apply firm, direct continuous pressure with sterile gauze or clean cloth. Do not remove soaked gauze; add more on top.\n"
                "• If catastrophic extremity hemorrhage cannot be stopped by direct pressure, apply a commercial tourniquet 2-3 inches above the wound (not on a joint) and tighten until bleeding ceases.\n\n"
                "**3. Anaphylaxis (Severe Allergic Reaction)**:\n"
                "• Immediate administration of an epinephrine auto-injector into the outer mid-thigh and immediate 911 dispatch.\n\n"
                "*Healix provides health information and triage guidance, not a medical diagnosis.*"
            )
        elif "doctor" in query_text or "urgent" in query_text or "when should i" in query_text:
            reply = (
                "You should consider scheduling an appointment with your healthcare provider if symptoms persist "
                "past 5 to 7 days, or if they interfere with work or sleep. "
                "If you develop severe warning signs like sudden explosive pain, shortness of breath, or numbness on one side, "
                "seek emergency evaluation immediately.\n\n"
                "*Healix provides health information and triage guidance, not a medical diagnosis.*"
            )
        else:
            reply = (
                "Thank you for sharing your question. When clinicians evaluate symptoms like these, "
                "they consider timing, severity, and potential lifestyle factors such as rest and hydration. "
                "Let me know if you would like information on self-care measures or warning signs to monitor.\n\n"
                "*Reminder: Healix provides educational context, not medical diagnosis.*"
            )

        return LLMResponse(
            text=reply,
            usage=LLMUsage(prompt_tokens=50, completion_tokens=len(reply) // 4, total_tokens=50 + len(reply) // 4),
            model=self.model_name,
            finish_reason="stop",
        )


class OpenAILLMProvider(BaseLLMProvider):
    """
    Production LLM Provider for OpenAI and OpenAI-compatible API services.
    Uses asynchronous HTTP client, strict JSON schema validation,
    bounded retries, and comprehensive error handling.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: Optional[str] = None,
        base_url: Optional[str] = None,
        timeout: float = 30.0,
    ):
        self.api_key = api_key or settings.AI_API_KEY
        self.model = model or settings.AI_MODEL
        self.base_url = (base_url or settings.AI_BASE_URL or "https://api.openai.com/v1").rstrip("/")
        self.timeout = timeout or settings.AI_REQUEST_TIMEOUT

    def _get_headers(self) -> Dict[str, str]:
        headers = {
            "Content-Type": "application/json",
        }
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        return headers

    async def generate_text(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ) -> LLMResponse:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature if temperature is not None else settings.AI_TEMPERATURE,
            "max_tokens": max_tokens or settings.AI_MAX_TOKENS,
        }

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    headers=self._get_headers(),
                    json=payload,
                )
                response.raise_for_status()
                data = response.json()
                choice = data["choices"][0]
                usage_raw = data.get("usage", {})
                usage = LLMUsage(
                    prompt_tokens=usage_raw.get("prompt_tokens", 0),
                    completion_tokens=usage_raw.get("completion_tokens", 0),
                    total_tokens=usage_raw.get("total_tokens", 0),
                )
                return LLMResponse(
                    text=choice["message"]["content"],
                    usage=usage,
                    model=data.get("model", self.model),
                    finish_reason=choice.get("finish_reason"),
                )
            except httpx.HTTPStatusError as exc:
                logger.error("OpenAI API HTTP error: %s %s", exc.response.status_code, exc.response.text)
                raise LLMProviderException(f"LLM Provider returned error: {exc.response.status_code}")
            except Exception as exc:
                logger.error("OpenAI API request failure: %s", str(exc))
                raise LLMProviderException(f"LLM request failed: {str(exc)}")

    async def generate_structured(
        self,
        schema: Type[T],
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        max_retries: int = 2,
    ) -> T:
        schema_json = json.dumps(schema.model_json_schema(), indent=2)
        strict_system_prompt = (
            (system_prompt or "You are a healthcare information assistant.")
            + "\n\nCRITICAL INSTRUCTION: You must respond ONLY with a valid JSON object matching this schema:\n"
            + schema_json
            + "\nDo NOT wrap with markdown fences or other text. Return raw JSON."
        )

        current_prompt = prompt
        attempts = 0
        last_error = None

        while attempts <= max_retries:
            attempts += 1
            try:
                resp = await self.generate_text(
                    prompt=current_prompt,
                    system_prompt=strict_system_prompt,
                    temperature=temperature or 0.1,
                    max_tokens=max_tokens,
                )
                raw_text = resp.text.strip()
                # Clean optional markdown code fences if model enclosed them
                if raw_text.startswith("```"):
                    raw_text = re.sub(r"^```(?:json)?\s*", "", raw_text)
                    raw_text = re.sub(r"\s*```$", "", raw_text)

                data = json.loads(raw_text)
                validated = schema.model_validate(data)
                return validated
            except (json.JSONDecodeError, ValidationError) as e:
                last_error = e
                logger.warning(
                    "Structured output parsing failure (attempt %d/%d): %s",
                    attempts,
                    max_retries + 1,
                    str(e),
                )
                # Formulate controlled retry prompt
                current_prompt = (
                    f"{prompt}\n\n"
                    f"PREVIOUS ATTEMPT WAS INVALID JSON OR FAILED SCHEMA VALIDATION:\n"
                    f"Error: {str(e)}\n"
                    f"Please output strictly valid JSON conforming to the requested schema."
                )

        logger.error("Exhausted retries for structured LLM generation. Falling back to default.")
        raise LLMProviderException(f"Failed to generate valid structured output after {max_retries} retries: {last_error}")

    async def generate_chat_response(
        self,
        messages: List[Dict[str, str]],
        system_prompt: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ) -> LLMResponse:
        full_messages = []
        if system_prompt:
            full_messages.append({"role": "system", "content": system_prompt})
        full_messages.extend(messages)

        payload = {
            "model": self.model,
            "messages": full_messages,
            "temperature": temperature if temperature is not None else settings.AI_TEMPERATURE,
            "max_tokens": max_tokens or settings.AI_MAX_TOKENS,
        }

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            try:
                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    headers=self._get_headers(),
                    json=payload,
                )
                response.raise_for_status()
                data = response.json()
                choice = data["choices"][0]
                usage_raw = data.get("usage", {})
                usage = LLMUsage(
                    prompt_tokens=usage_raw.get("prompt_tokens", 0),
                    completion_tokens=usage_raw.get("completion_tokens", 0),
                    total_tokens=usage_raw.get("total_tokens", 0),
                )
                return LLMResponse(
                    text=choice["message"]["content"],
                    usage=usage,
                    model=data.get("model", self.model),
                    finish_reason=choice.get("finish_reason"),
                )
            except Exception as exc:
                logger.error("OpenAI Chat API request failure: %s", str(exc))
                raise LLMProviderException(f"LLM chat request failed: {str(exc)}")


class GeminiLLMProvider(BaseLLMProvider):
    """
    Production Google Gemini LLM Provider.
    Interfaces directly with Google Generative Language API (v1beta).
    Supports gemini-3.5-flash, gemini-3.8-flash, gemini-flash-latest with
    automatic fallback across resilient models, structured JSON schema output,
    and graceful safety handling.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: Optional[str] = None,
        timeout: float = 30.0,
    ):
        self.api_key = api_key or settings.AI_API_KEY
        self.model = model or settings.AI_MODEL or "gemini-3.5-flash"
        self.timeout = timeout or settings.AI_REQUEST_TIMEOUT
        self.candidate_models = [
            self.model,
            "gemini-3.5-flash",
            "gemini-3.8-flash",
            "gemini-flash-latest",
            "gemini-pro-latest",
        ]
        # Deduplicate while preserving order
        seen = set()
        self.fallback_models = []
        for m in self.candidate_models:
            if m and m not in seen:
                seen.add(m)
                self.fallback_models.append(m)

    async def _post_generate_content(
        self,
        contents: List[Dict[str, Any]],
        system_instruction: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        response_mime_type: Optional[str] = None,
    ) -> Dict[str, Any]:
        last_error = None
        gen_config: Dict[str, Any] = {
            "temperature": temperature if temperature is not None else settings.AI_TEMPERATURE,
            "maxOutputTokens": max_tokens or settings.AI_MAX_TOKENS,
            "thinkingConfig": {"thinkingBudget": 0},
        }
        if response_mime_type:
            gen_config["responseMimeType"] = response_mime_type

        payload: Dict[str, Any] = {
            "contents": contents,
            "generationConfig": gen_config,
        }
        if system_instruction:
            payload["system_instruction"] = {
                "parts": [{"text": system_instruction}]
            }

        async with httpx.AsyncClient(timeout=self.timeout) as client:
            for model_name in self.fallback_models:
                url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={self.api_key}"
                try:
                    resp = await client.post(url, json=payload)
                    if resp.status_code == 200:
                        return resp.json()
                    elif resp.status_code in (404, 429, 503):
                        logger.warning(
                            "Gemini model %s returned HTTP %d. Trying next candidate model.",
                            model_name,
                            resp.status_code,
                        )
                        last_error = f"HTTP {resp.status_code}: {resp.text[:120]}"
                        continue
                    else:
                        resp.raise_for_status()
                except (httpx.TimeoutException, httpx.RequestError) as net_err:
                    logger.warning("Gemini network error with model %s: %s", model_name, str(net_err))
                    last_error = str(net_err)
                    continue

        raise LLMProviderException(f"All Gemini models exhausted. Last error: {last_error}")

    async def generate_text(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ) -> LLMResponse:
        contents = [{"role": "user", "parts": [{"text": prompt}]}]
        try:
            data = await self._post_generate_content(
                contents=contents,
                system_instruction=system_prompt,
                temperature=temperature,
                max_tokens=max_tokens,
            )
            candidate = data["candidates"][0]
            text = candidate["content"]["parts"][0]["text"]
            meta = data.get("usageMetadata", {})
            return LLMResponse(
                text=text,
                usage=LLMUsage(
                    prompt_tokens=meta.get("promptTokenCount", len(prompt) // 4),
                    completion_tokens=meta.get("candidatesTokenCount", len(text) // 4),
                    total_tokens=meta.get("totalTokenCount", (len(prompt) + len(text)) // 4),
                ),
                model=self.model,
                finish_reason=candidate.get("finishReason", "STOP").lower(),
            )
        except Exception as exc:
            logger.error("Gemini generate_text failed: %s. Using MockLLM fallback.", exc)
            fallback = MockLLMProvider()
            return await fallback.generate_text(prompt, system_prompt, temperature, max_tokens)

    async def generate_chat_response(
        self,
        messages: List[Dict[str, str]],
        system_prompt: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ) -> LLMResponse:
        gemini_contents = []
        for msg in messages:
            r = "user" if msg.get("role") in ("user", "system") else "model"
            content = msg.get("content", "")
            gemini_contents.append({"role": r, "parts": [{"text": content}]})

        try:
            data = await self._post_generate_content(
                contents=gemini_contents,
                system_instruction=system_prompt,
                temperature=temperature,
                max_tokens=max_tokens,
            )
            candidate = data["candidates"][0]
            text = candidate["content"]["parts"][0]["text"]
            meta = data.get("usageMetadata", {})
            return LLMResponse(
                text=text,
                usage=LLMUsage(
                    prompt_tokens=meta.get("promptTokenCount", 50),
                    completion_tokens=meta.get("candidatesTokenCount", len(text) // 4),
                    total_tokens=meta.get("totalTokenCount", 50 + len(text) // 4),
                ),
                model=self.model,
                finish_reason=candidate.get("finishReason", "STOP").lower(),
            )
        except Exception as exc:
            logger.error("Gemini generate_chat_response failed: %s. Using MockLLM fallback.", exc)
            fallback = MockLLMProvider()
            return await fallback.generate_chat_response(messages, system_prompt, temperature, max_tokens)

    async def generate_structured(
        self,
        schema: Type[T],
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        max_retries: int = 2,
    ) -> T:
        schema_json = json.dumps(schema.model_json_schema(), indent=2)
        strict_instruction = (
            (system_prompt or "You are a healthcare information assistant.")
            + "\n\nCRITICAL INSTRUCTION: You must respond ONLY with a valid JSON object matching this schema:\n"
            + schema_json
            + "\nReturn strictly raw JSON."
        )

        current_prompt = prompt
        attempts = 0
        last_error = None

        while attempts <= max_retries:
            attempts += 1
            try:
                contents = [{"role": "user", "parts": [{"text": current_prompt}]}]
                data = await self._post_generate_content(
                    contents=contents,
                    system_instruction=strict_instruction,
                    temperature=temperature if temperature is not None else 0.1,
                    max_tokens=max_tokens,
                    response_mime_type="application/json",
                )
                raw_text = data["candidates"][0]["content"]["parts"][0]["text"].strip()
                if raw_text.startswith("```"):
                    raw_text = re.sub(r"^```(?:json)?\s*", "", raw_text)
                    raw_text = re.sub(r"\s*```$", "", raw_text)

                parsed_json = json.loads(raw_text)
                return schema.model_validate(parsed_json)
            except Exception as e:
                last_error = e
                logger.warning("Gemini structured attempt %d failed: %s", attempts, str(e))
                current_prompt = f"{prompt}\n\nPREVIOUS OUTPUT FAILED JSON VALIDATION: {str(e)}\nReturn ONLY valid JSON."

        logger.warning("Gemini structured retries exhausted. Using Mock fallback.")
        fallback = MockLLMProvider()
        return await fallback.generate_structured(schema, prompt, system_prompt, temperature, max_tokens, max_retries)


def get_llm_provider(provider_type: Optional[str] = None) -> BaseLLMProvider:
    """
    Factory to resolve LLM provider instance from settings or explicit argument.
    """
    selected = (provider_type or settings.AI_PROVIDER).lower()
    if selected == "local":
        from app.services.ai.llm.local_provider import LocalLLMProvider
        return LocalLLMProvider()
    if selected == "mock":
        return MockLLMProvider()
    elif selected == "openai":
        if not settings.AI_API_KEY:
            raise LLMProviderException("AI_API_KEY is required when AI_PROVIDER=openai", status_code=500)
        return OpenAILLMProvider()
    else:
        raise ValueError(f"Unsupported AI provider: {selected}")
