from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from app.utils.constants import STANDARD_MEDICAL_DISCLAIMER, QuestionType
from app.utils.validators import AIResponseValidator


class AIService(ABC):
    """
    Abstract AI service interface to allow seamless plug-and-play
    between MockAIService in Phase 1 and LLMService / RAGService in Phase 2.
    """

    @abstractmethod
    async def analyze_symptoms(self, description: str, symptoms: List[Dict[str, Any]]) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def generate_follow_up_questions(
        self, description: str, symptoms: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        pass

    @abstractmethod
    async def generate_summary(
        self,
        description: str,
        symptoms: List[Dict[str, Any]],
        answers: List[Dict[str, Any]],
        triage_result: Dict[str, Any],
        assessment_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        pass

    @abstractmethod
    async def chat(
        self,
        user_message: str,
        conversation_history: List[Dict[str, str]],
        assessment_context: Optional[Dict[str, Any]] = None,
    ) -> str:
        pass


class MockAIService(AIService):
    """
    Mock AI Service for Phase 1.
    Provides realistic, evidence-grounded health information responses
    without claiming definitive medical diagnoses.
    """

    async def analyze_symptoms(self, description: str, symptoms: List[Dict[str, Any]]) -> Dict[str, Any]:
        symptom_names = [s.get("name", "").lower() for s in symptoms]
        combined = f"{description} {' '.join(symptom_names)}".lower()

        if "headache" in combined:
            possible_explanations = [
                {
                    "title": "Tension-type Headache",
                    "description": "A common type of headache causing diffuse, mild to moderate dull band-like discomfort across the forehead or neck. Often associated with stress, eye fatigue, or poor neck posture.",
                    "match_level": "High Relevance",
                    "relevant_symptoms": ["Headache"],
                    "clinical_note": "Typically bilateral and non-pulsatile.",
                },
                {
                    "title": "Mild Dehydration & Screen Fatigue",
                    "description": "Inadequate hydration and sustained visual strain can exacerbate vascular tension and daytime lethargy.",
                    "match_level": "Moderate Relevance",
                    "relevant_symptoms": ["Headache", "Fatigue"],
                    "clinical_note": "Responds well to rest and fluid intake.",
                },
            ]
        elif "chest" in combined:
            possible_explanations = [
                {
                    "title": "Musculoskeletal Chest Wall Discomfort",
                    "description": "Localized tenderness in the rib cage cartilage often worsened by twisting or deep breaths. Must be distinguished clinically from cardiac conditions.",
                    "match_level": "Possible Consideration",
                    "relevant_symptoms": ["Chest discomfort"],
                    "clinical_note": "Requires physician confirmation.",
                }
            ]
        else:
            possible_explanations = [
                {
                    "title": "Transient Functional Strain & Fatigue",
                    "description": "Temporary physiological reaction to elevated physical or psychological strain, inadequate sleep, or mild viral exposure.",
                    "match_level": "Common Consideration",
                    "relevant_symptoms": symptom_names or ["General Discomfort"],
                    "clinical_note": "Monitor trajectory over the next 48 hours.",
                }
            ]

        return {
            "possible_explanations": possible_explanations,
            "general_guidance": [
                "Stay well hydrated with water and light electrolytes.",
                "Ensure a restful 7–8 hour sleep environment in a dark, quiet room.",
                "Take a 15-minute visual break away from screens.",
            ],
            "warning_signs": [
                "Sudden explosive onset of severe pain ('thunderclap')",
                "Shortness of breath, chest tightness, or radiating pain to the arm",
                "High fever combined with stiff neck or confusion",
            ],
            "sources": [
                {
                    "name": "Mayo Clinic",
                    "topic": "Clinical Evidence & Headache Classifications",
                    "url": "https://www.mayoclinic.org",
                    "authority": "Mayo Clinic Department of Neurology",
                },
                {
                    "name": "World Health Organization (WHO)",
                    "topic": "Global Primary Healthcare Standards",
                    "url": "https://www.who.int",
                    "authority": "WHO Guidelines Framework",
                },
            ],
        }

    async def generate_follow_up_questions(
        self, description: str, symptoms: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        symptom_names = [s.get("name", "").lower() for s in symptoms]
        combined = f"{description} {' '.join(symptom_names)}".lower()

        if "head" in combined or "headache" in combined:
            return [
                {
                    "question": "Is the headache sudden and described as the most severe headache of your life?",
                    "type": QuestionType.SINGLE_CHOICE.value,
                    "order_index": 0,
                },
                {
                    "question": "Have you noticed any visual disturbances, such as flashing lights or blind spots?",
                    "type": QuestionType.SINGLE_CHOICE.value,
                    "order_index": 1,
                },
                {
                    "question": "Does moving your neck or touching your chin to your chest cause stiffness or pain?",
                    "type": QuestionType.SINGLE_CHOICE.value,
                    "order_index": 2,
                },
            ]
        elif "chest" in combined:
            return [
                {
                    "question": "Does the discomfort radiate toward your left arm, neck, or jaw?",
                    "type": QuestionType.SINGLE_CHOICE.value,
                    "order_index": 0,
                },
                {
                    "question": "Are you experiencing any shortness of breath or sudden unexplained cold sweats?",
                    "type": QuestionType.SINGLE_CHOICE.value,
                    "order_index": 1,
                },
            ]
        else:
            return [
                {
                    "question": "Have you experienced any shortness of breath or sudden difficulty breathing?",
                    "type": QuestionType.SINGLE_CHOICE.value,
                    "order_index": 0,
                },
                {
                    "question": "Has your body temperature been measured above 38.5°C (101.3°F)?",
                    "type": QuestionType.SINGLE_CHOICE.value,
                    "order_index": 1,
                },
            ]

    async def generate_summary(
        self,
        description: str,
        symptoms: List[Dict[str, Any]],
        answers: List[Dict[str, Any]],
        triage_result: Dict[str, Any],
        assessment_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        analysis = await self.analyze_symptoms(description, symptoms)

        symptom_titles = ", ".join([s.get("name", "") for s in symptoms]) or "General Symptoms"
        summary = (
            f"Preliminary analysis for reported symptoms: {symptom_titles}. "
            f"Triage status assessed as {triage_result['urgency_level']}. "
            f"{triage_result['message']}"
        )

        raw_result = {
            "summary": summary,
            "urgency_level": triage_result["urgency_level"],
            "possible_explanations": analysis["possible_explanations"],
            "general_guidance": analysis["general_guidance"],
            "warning_signs": analysis["warning_signs"],
            "sources": analysis["sources"],
            "disclaimer": STANDARD_MEDICAL_DISCLAIMER,
        }

        # Validate through AI safety layer
        return AIResponseValidator.sanitize_and_validate(raw_result)

    async def chat(
        self,
        user_message: str,
        conversation_history: List[Dict[str, str]],
        assessment_context: Optional[Dict[str, Any]] = None,
    ) -> str:
        lower = user_message.lower()

        if "dehydration" in lower or "water" in lower:
            return (
                "Mild dehydration is a common contributing factor to dull headaches and daytime fatigue. "
                "Drinking water steadily over a few hours rather than all at once helps rebalance fluid volume. "
                "Observe if your urine is pale yellow (well hydrated) versus dark amber.\n\n"
                "*Healix provides health information and triage guidance, not clinical medical diagnosis.*"
            )
        elif "doctor" in lower or "urgent" in lower or "when should i" in lower:
            return (
                "You should consider scheduling an appointment with your doctor if symptoms persist past 5 to 7 days, "
                "or if they interfere with work, sleep, or eating. "
                "If you develop severe warning signs like sudden explosive pain, shortness of breath, or numbness on one side, "
                "seek emergency evaluation immediately."
            )
        else:
            return (
                "Thank you for sharing your question. When clinicians evaluate symptoms like these, "
                "they examine onset timing, pain character, and potential lifestyle factors like sleep and posture. "
                "Let me know if you would like information on self-care measures or warning signs to monitor.\n\n"
                "*Reminder: Healix provides educational context, not medical diagnosis.*"
            )


def get_ai_service() -> AIService:
    """
    Factory resolving active AI service.
    Integrates AIOrchestrator with RAG, Safety, and configured LLM provider.
    """
    from app.services.ai.orchestrator import AIOrchestrator
    return AIOrchestrator()


# Export RealAIService alias for AIOrchestrator
def __getattr__(name: str):
    if name == "RealAIService":
        from app.services.ai.orchestrator import AIOrchestrator
        return AIOrchestrator
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")

