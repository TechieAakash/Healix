from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from enum import Enum

class QuestionAnswerType(str, Enum):
    BOOLEAN = "BOOLEAN"              # Yes / No / Unknown
    SINGLE_CHOICE = "SINGLE_CHOICE"  # Select one option
    MULTI_CHOICE = "MULTI_CHOICE"    # Select multiple options
    SEVERITY_SCALE = "SEVERITY_SCALE"# 1 to 10 or Mild/Mod/Severe
    FREE_TEXT = "FREE_TEXT"

class QuestionOption(BaseModel):
    id: str
    label: str
    fact_value: str
    is_red_flag: bool = False

class QuestionDefinition(BaseModel):
    id: str
    prompt: str
    subtext: Optional[str] = None
    target_fact_name: str
    answer_type: QuestionAnswerType = QuestionAnswerType.BOOLEAN
    options: List[QuestionOption] = Field(default_factory=list)
    associated_symptoms: List[str]   # e.g. ["sym_headache"]
    required_preconditions: Dict[str, Any] = Field(default_factory=dict) # e.g. {"symptom.headache.present": "TRUE"}
    priority: int = 500              # 1000 = Red Flag Emergency, 700 = Diagnostic Differential, 400 = Character/Context
    is_safety_critical: bool = False
    evidence_provenance: str = "Clinical Practice Guidelines"
    version: str = "2.0.0"

# Comprehensive Question Bank for All Supported Symptoms
QUESTION_BANK: List[QuestionDefinition] = [
    # ---------------------------------------------------------
    # HEADACHE PATHWAY QUESTIONS
    # ---------------------------------------------------------
    QuestionDefinition(
        id="q_headache_thunderclap",
        prompt="Did your headache begin with sudden, explosive, peak intensity (reaching 10/10 within 60 seconds)?",
        subtext="Sudden 'thunderclap' onset cephalea is a critical vascular warning sign requiring immediate emergency imaging.",
        target_fact_name="symptom.headache.onset_thunderclap",
        answer_type=QuestionAnswerType.BOOLEAN,
        options=[
            QuestionOption(id="yes", label="Yes, explosive sudden onset", fact_value="TRUE", is_red_flag=True),
            QuestionOption(id="no", label="No, built up gradually", fact_value="FALSE")
        ],
        associated_symptoms=["sym_headache"],
        priority=1000,
        is_safety_critical=True,
        evidence_provenance="ACEP Neurovascular Clinical Policy"
    ),
    QuestionDefinition(
        id="q_neck_rigidity",
        prompt="Do you have severe neck stiffness where you cannot touch your chin to your chest?",
        subtext="Severe nuchal rigidity paired with headache or fever can indicate meningeal irritation.",
        target_fact_name="symptom.neck_stiffness",
        answer_type=QuestionAnswerType.BOOLEAN,
        options=[
            QuestionOption(id="yes", label="Yes, severe stiffness/resistance", fact_value="TRUE", is_red_flag=True),
            QuestionOption(id="no", label="No neck stiffness", fact_value="FALSE")
        ],
        associated_symptoms=["sym_headache", "sym_neck_stiffness", "sym_fever"],
        priority=950,
        is_safety_critical=True,
        evidence_provenance="IDSA Bacterial Meningitis Guidance"
    ),
    QuestionDefinition(
        id="q_neuro_deficits",
        prompt="Are you experiencing sudden focal neurological changes (facial drooping, arm weakness, or slurred speech)?",
        subtext="Sudden neurological deficits indicate immediate cerebrovascular FAST protocol activation.",
        target_fact_name="symptom.neuro_deficits_fast",
        answer_type=QuestionAnswerType.BOOLEAN,
        options=[
            QuestionOption(id="yes", label="Yes, focal weakness or speech difficulty", fact_value="TRUE", is_red_flag=True),
            QuestionOption(id="no", label="No focal weakness or speech changes", fact_value="FALSE")
        ],
        associated_symptoms=["sym_headache", "sym_dizziness"],
        priority=1000,
        is_safety_critical=True,
        evidence_provenance="AHA/ASA Stroke Guidelines"
    ),
    QuestionDefinition(
        id="q_headache_character",
        prompt="How would you describe the character of your head pain?",
        subtext="The sensation quality helps differentiate vascular migraine from pericranial tension.",
        target_fact_name="symptom.headache.character",
        answer_type=QuestionAnswerType.SINGLE_CHOICE,
        options=[
            QuestionOption(id="throbbing", label="Pulsating / Throbbing (Rhythmic beat)", fact_value="THROBBING"),
            QuestionOption(id="tight_band", label="Pressing / Tight band around head", fact_value="TIGHT_BAND"),
            QuestionOption(id="stabbing", label="Sharp / Piercing around one eye", fact_value="STABBING"),
            QuestionOption(id="dull", label="Dull, generalized ache", fact_value="DULL")
        ],
        associated_symptoms=["sym_headache"],
        priority=700,
        evidence_provenance="ICHD-3 Cephalea Classification"
    ),
    QuestionDefinition(
        id="q_headache_visual_aura",
        prompt="Did you experience flickering zig-zag lights, blind spots, or sensory tingling before the pain began?",
        subtext="Visual or sensory aura points toward episodic neurovascular migraine with aura.",
        target_fact_name="symptom.headache.visual_aura",
        answer_type=QuestionAnswerType.BOOLEAN,
        options=[
            QuestionOption(id="yes", label="Yes, visual disturbances or tingling", fact_value="TRUE"),
            QuestionOption(id="no", label="No visual changes", fact_value="FALSE")
        ],
        associated_symptoms=["sym_headache"],
        priority=650,
        evidence_provenance="ICHD-3 Migraine with Aura Criteria"
    ),
    QuestionDefinition(
        id="q_headache_photophobia",
        prompt="Does normal indoor or daylight bother your eyes or make the headache worse?",
        subtext="Photophobia is a cardinal diagnostic finding in migraine and neurovascular headaches.",
        target_fact_name="symptom.photophobia",
        answer_type=QuestionAnswerType.BOOLEAN,
        options=[
            QuestionOption(id="yes", label="Yes, sensitive to light", fact_value="TRUE"),
            QuestionOption(id="no", label="No light sensitivity", fact_value="FALSE")
        ],
        associated_symptoms=["sym_headache", "sym_photophobia"],
        priority=600
    ),
    QuestionDefinition(
        id="q_headache_nausea",
        prompt="Are you experiencing nausea, queasiness, or have you vomited during this headache?",
        subtext="Autonomic involvement supports migraine while its absence supports tension headache.",
        target_fact_name="symptom.nausea",
        answer_type=QuestionAnswerType.BOOLEAN,
        options=[
            QuestionOption(id="yes", label="Yes, nausea or vomiting present", fact_value="TRUE"),
            QuestionOption(id="no", label="No nausea", fact_value="FALSE")
        ],
        associated_symptoms=["sym_headache", "sym_nausea"],
        priority=600
    ),

    # ---------------------------------------------------------
    # RESPIRATORY PATHWAY QUESTIONS
    # ---------------------------------------------------------
    QuestionDefinition(
        id="q_chest_pain_crushing",
        prompt="Are you experiencing heavy pressure, crushing sensation, or tightness in the center of your chest?",
        subtext="Substernal crushing chest pain can represent acute coronary ischemia and requires immediate emergency evaluation.",
        target_fact_name="symptom.chest_pain.crushing",
        answer_type=QuestionAnswerType.BOOLEAN,
        options=[
            QuestionOption(id="yes", label="Yes, heavy pressure or crushing chest pain", fact_value="TRUE", is_red_flag=True),
            QuestionOption(id="no", label="No crushing chest pain", fact_value="FALSE")
        ],
        associated_symptoms=["sym_chest_pain", "sym_dyspnea"],
        priority=1000,
        is_safety_critical=True,
        evidence_provenance="AHA/ACC Chest Pain Evaluation Guidelines"
    ),
    QuestionDefinition(
        id="q_chest_radiation",
        prompt="Does the chest or neck discomfort radiate to your left arm, jaw, shoulder, or upper back?",
        subtext="Radiation of pain is an established predictor of cardiac involvement.",
        target_fact_name="symptom.chest_pain.radiation",
        answer_type=QuestionAnswerType.BOOLEAN,
        options=[
            QuestionOption(id="yes", label="Yes, radiates to arm, jaw, or back", fact_value="TRUE", is_red_flag=True),
            QuestionOption(id="no", label="No radiation", fact_value="FALSE")
        ],
        associated_symptoms=["sym_chest_pain"],
        priority=950,
        is_safety_critical=True
    ),
    QuestionDefinition(
        id="q_dyspnea_severity",
        prompt="Are you so short of breath that you cannot complete a full sentence without gasping for air?",
        subtext="Inability to speak in full sentences indicates severe respiratory compromise.",
        target_fact_name="symptom.dyspnea.severe_speech_difficulty",
        answer_type=QuestionAnswerType.BOOLEAN,
        options=[
            QuestionOption(id="yes", label="Yes, struggling to speak full sentences", fact_value="TRUE", is_red_flag=True),
            QuestionOption(id="no", label="No, able to speak comfortably", fact_value="FALSE")
        ],
        associated_symptoms=["sym_dyspnea", "sym_cough"],
        priority=1000,
        is_safety_critical=True,
        evidence_provenance="BTS Respiratory Emergency Standards"
    ),
    QuestionDefinition(
        id="q_cough_sputum",
        prompt="What is the nature of your cough?",
        subtext="Differentiates upper viral irritation from lower bronchial hypersecretion.",
        target_fact_name="symptom.cough.character",
        answer_type=QuestionAnswerType.SINGLE_CHOICE,
        options=[
            QuestionOption(id="dry", label="Dry, tickly, non-productive", fact_value="DRY"),
            QuestionOption(id="phlegm", label="Productive with clear or yellow/green phlegm", fact_value="PRODUCTIVE"),
            QuestionOption(id="blood", label="Coughing up blood or rust-colored streaks", fact_value="HEMOPTYSIS", is_red_flag=True)
        ],
        associated_symptoms=["sym_cough"],
        priority=700
    ),
    QuestionDefinition(
        id="q_wheezing_present",
        prompt="Do you hear a high-pitched musical whistling or wheezing sound when breathing out?",
        subtext="Expiratory wheezing indicates lower airway bronchospasm common in asthma or acute bronchitis.",
        target_fact_name="symptom.wheezing",
        answer_type=QuestionAnswerType.BOOLEAN,
        options=[
            QuestionOption(id="yes", label="Yes, audible wheezing sound", fact_value="TRUE"),
            QuestionOption(id="no", label="No wheezing", fact_value="FALSE")
        ],
        associated_symptoms=["sym_cough", "sym_dyspnea"],
        priority=700
    ),
    QuestionDefinition(
        id="q_nasal_symptoms",
        prompt="Do you have a runny or blocked nose, sneezing, or watery eyes?",
        subtext="Presence of upper rhinitis strongly supports common viral coryza (upper respiratory infection).",
        target_fact_name="symptom.rhinorrhea",
        answer_type=QuestionAnswerType.BOOLEAN,
        options=[
            QuestionOption(id="yes", label="Yes, runny or congested nose", fact_value="TRUE"),
            QuestionOption(id="no", label="No nasal symptoms", fact_value="FALSE")
        ],
        associated_symptoms=["sym_cough", "sym_sore_throat", "sym_rhinorrhea"],
        priority=550
    ),

    # ---------------------------------------------------------
    # ABDOMINAL & DIGESTIVE PATHWAY QUESTIONS
    # ---------------------------------------------------------
    QuestionDefinition(
        id="q_abd_rlq_migration",
        prompt="Did the stomach pain start around your belly button and migrate down to your lower right side?",
        subtext="Migration to the right lower quadrant with guarding is classic for acute appendicitis.",
        target_fact_name="symptom.abdominal_pain.rlq_migration",
        answer_type=QuestionAnswerType.BOOLEAN,
        options=[
            QuestionOption(id="yes", label="Yes, migrated to lower right abdomen", fact_value="TRUE", is_red_flag=True),
            QuestionOption(id="no", label="No, pain stayed elsewhere", fact_value="FALSE")
        ],
        associated_symptoms=["sym_abdominal_pain"],
        priority=1000,
        is_safety_critical=True,
        evidence_provenance="WSES Jerusalem Guidelines on Acute Appendicitis"
    ),
    QuestionDefinition(
        id="q_abd_rebound_tenderness",
        prompt="Is the abdominal pain significantly sharper when you suddenly let go after pressing down (rebound pain)?",
        subtext="Rebound tenderness is an indicator of peritoneal irritation requiring urgent surgical evaluation.",
        target_fact_name="symptom.abdominal_pain.rebound",
        answer_type=QuestionAnswerType.BOOLEAN,
        options=[
            QuestionOption(id="yes", label="Yes, sharp pain when releasing pressure", fact_value="TRUE", is_red_flag=True),
            QuestionOption(id="no", label="No rebound pain", fact_value="FALSE")
        ],
        associated_symptoms=["sym_abdominal_pain"],
        priority=950,
        is_safety_critical=True
    ),
    QuestionDefinition(
        id="q_diarrhea_blood",
        prompt="Have you noticed bright red blood or black tarry stools in your bowel movements?",
        subtext="Gastrointestinal bleeding requires immediate clinical exclusion of acute hemorrhage.",
        target_fact_name="symptom.diarrhea.blood_present",
        answer_type=QuestionAnswerType.BOOLEAN,
        options=[
            QuestionOption(id="yes", label="Yes, visible blood or tarry stools", fact_value="TRUE", is_red_flag=True),
            QuestionOption(id="no", label="No blood in stools", fact_value="FALSE")
        ],
        associated_symptoms=["sym_diarrhea", "sym_abdominal_pain"],
        priority=950,
        is_safety_critical=True
    ),
    QuestionDefinition(
        id="q_heartburn_food_relation",
        prompt="Does the burning sensation worsen after meals or when bending over / lying flat?",
        subtext="Postprandial and positional burning is characteristic of gastroesophageal reflux (GERD).",
        target_fact_name="symptom.heartburn.postprandial",
        answer_type=QuestionAnswerType.BOOLEAN,
        options=[
            QuestionOption(id="yes", label="Yes, worse after food or lying down", fact_value="TRUE"),
            QuestionOption(id="no", label="No relation to meals or posture", fact_value="FALSE")
        ],
        associated_symptoms=["sym_heartburn", "sym_chest_pain"],
        priority=600
    ),

    # ---------------------------------------------------------
    # GENERAL / CONSTITUTIONAL & SYSTEMIC QUESTIONS
    # ---------------------------------------------------------
    QuestionDefinition(
        id="q_fever_measured",
        prompt="Have you measured your body temperature with a thermometer?",
        subtext="Helps determine exact pyretic range (afebrile, low-grade, or high-grade fever).",
        target_fact_name="symptom.fever.measured_range",
        answer_type=QuestionAnswerType.SINGLE_CHOICE,
        options=[
            QuestionOption(id="afebrile", label="Normal (< 37.5°C / 99.5°F)", fact_value="NORMAL"),
            QuestionOption(id="low_grade", label="Low-grade fever (37.5°C - 38.4°C)", fact_value="LOW_GRADE"),
            QuestionOption(id="high_grade", label="High fever (>= 38.5°C / 101.3°F)", fact_value="HIGH_GRADE")
        ],
        associated_symptoms=["sym_fever", "sym_headache", "sym_cough", "sym_sore_throat"],
        priority=750
    ),
    QuestionDefinition(
        id="q_dehydration_signs",
        prompt="Are you experiencing pronounced dry mouth, intense thirst, or dark/infrequent urination?",
        subtext="Fluid volume depletion frequently complicates febrile illnesses and gastroenteritis.",
        target_fact_name="symptom.dehydration_signs",
        answer_type=QuestionAnswerType.BOOLEAN,
        options=[
            QuestionOption(id="yes", label="Yes, dry mouth and decreased urination", fact_value="TRUE"),
            QuestionOption(id="no", label="No, normal hydration and urination", fact_value="FALSE")
        ],
        associated_symptoms=["sym_fever", "sym_diarrhea", "sym_nausea", "sym_fatigue"],
        priority=650
    )
]

class AdaptiveQuestionSelector:
    """
    Selects the next most clinically discriminative and safety-critical question
    based on the user's reported symptoms, current working memory, and answered history.
    """

    @staticmethod
    def get_candidate_questions(
        reported_symptom_ids: List[str],
        answered_fact_names: List[str],
        working_memory_facts: Dict[str, Any]
    ) -> List[QuestionDefinition]:
        candidates: List[QuestionDefinition] = []

        for q in QUESTION_BANK:
            # 1. Skip if already answered
            if q.target_fact_name in answered_fact_names:
                continue

            # 2. Check if question is relevant to any of the user's reported symptoms
            is_relevant = any(sym_id in q.associated_symptoms for sym_id in reported_symptom_ids)
            if not is_relevant:
                continue

            # 3. Check preconditions (e.g. if headache.present is FALSE, don't ask about aura)
            preconditions_met = True
            for pre_fact, required_val in q.required_preconditions.items():
                actual_val = working_memory_facts.get(pre_fact)
                if actual_val != required_val:
                    preconditions_met = False
                    break

            if preconditions_met:
                candidates.append(q)

        # 4. Sort candidates:
        # Highest priority first (Red Flag 1000 > Differential 700 > Context 500)
        candidates.sort(key=lambda q: (-q.priority, q.id))
        return candidates

    @classmethod
    def get_next_question(
        cls,
        reported_symptom_ids: List[str],
        answered_fact_names: List[str],
        working_memory_facts: Dict[str, Any]
    ) -> Optional[QuestionDefinition]:
        candidates = cls.get_candidate_questions(
            reported_symptom_ids=reported_symptom_ids,
            answered_fact_names=answered_fact_names,
            working_memory_facts=working_memory_facts
        )
        return candidates[0] if candidates else None

