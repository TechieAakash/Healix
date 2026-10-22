import re
from typing import List, Dict, Any, Optional
from app.utils.constants import UrgencyLevel
from app.services.clinical.text_normalizer import clean_clinical_text
from app.services.clinical.negation_detector import negation_detector
from app.services.clinical.symptom_engine import symptom_engine
from app.services.clinical.symptom_ontology import concept_key, ontology_facts

RED_FLAG_RULES = [
    {
        "id": "RULE_CARDIO_001",
        "category": "cardiovascular",
        "keywords": [
            "chest pain", "chest pressure", "radiating to arm", "radiating to jaw",
            "crushing chest pain", "substernal chest pain", "chest tightness",
        ],
        "urgency": UrgencyLevel.EMERGENCY.value,
        "description": "Potential acute coronary or cardiopulmonary warning signs detected.",
    },
    {
        "id": "RULE_RESP_001",
        "category": "respiratory",
        "keywords": [
            "shortness of breath at rest", "cannot breathe", "stridor", "blue lips",
            "gasping", "unable to breathe", "severe difficulty breathing",
        ],
        "urgency": UrgencyLevel.EMERGENCY.value,
        "description": "Severe respiratory distress warning signs detected.",
    },
    {
        "id": "RULE_NEURO_001",
        "category": "neurological",
        "keywords": [
            "facial drooping", "face is drooping", "face drooping", "slurred speech", "speech is slurred", "sudden arm weakness",
            "sudden loss of vision", "thunderclap headache", "worst headache of my life",
            "worst headache of life", "sudden numbness on one side",
        ],
        "urgency": UrgencyLevel.EMERGENCY.value,
        "description": "Acute neurological emergency signs detected (e.g. stroke or intracranial hemorrhage alert).",
    },
    {
        "id": "RULE_HEM_001",
        "category": "hemorrhage",
        "keywords": [
            "coughing up blood", "uncontrolled bleeding", "vomiting blood",
            "black tarry stools", "hematemesis", "hemoptysis",
        ],
        "urgency": UrgencyLevel.EMERGENCY.value,
        "description": "Signs of significant hemorrhage or gastrointestinal bleeding.",
    },
    {
        "id": "RULE_SEV_001",
        "category": "severity_threshold",
        "severity_min": 9,
        "urgency": UrgencyLevel.URGENT.value,
        "description": "Extreme self-reported symptom severity (>= 9/10).",
    },
    {
        "id": "RULE_ABDO_001",
        "category": "gastrointestinal",
        "keywords": ["severe abdominal pain", "rigid abdomen", "rebound tenderness"],
        "urgency": UrgencyLevel.EMERGENCY.value,
        "description": "Potential acute peritoneal irritation requiring emergency assessment.",
    },
    {
        "id": "RULE_SEPSIS_001",
        "category": "systemic_infection",
        "keywords": ["confusion with fever", "fever and confusion", "blue or mottled skin", "very fast breathing with fever", "unable to wake with fever"],
        "urgency": UrgencyLevel.EMERGENCY.value,
        "description": "Possible severe systemic illness warning signs detected.",
    },
    {
        "id": "RULE_DEHYDRATION_001",
        "category": "dehydration",
        "keywords": ["no urine for 12 hours", "no urination all day", "unable to keep any fluids down", "fainting from dehydration", "confusion from dehydration"],
        "urgency": UrgencyLevel.EMERGENCY.value,
        "description": "Possible severe dehydration warning signs detected.",
    },
    {
        "id": "RULE_PREGNANCY_001",
        "category": "pregnancy",
        "keywords": ["heavy bleeding during pregnancy", "pregnant and heavy bleeding", "bleeding while pregnant", "pregnant with vaginal bleeding", "pregnancy with severe abdominal pain"],
        "urgency": UrgencyLevel.EMERGENCY.value,
        "description": "Pregnancy-related bleeding or severe pain needs immediate assessment.",
    },
    {
        "id": "RULE_INFANT_FEVER_001",
        "category": "pediatric",
        "keywords": ["under 3 months with fever", "3 month old fever", "newborn with fever", "newborn has fever", "infant under 3 months fever"],
        "urgency": UrgencyLevel.EMERGENCY.value,
        "description": "Fever in a very young infant requires prompt emergency medical assessment.",
    },
    {
        "id": "RULE_SUICIDE_001",
        "category": "mental_health_crisis",
        "keywords": ["suicidal thoughts", "thinking about suicide", "want to kill myself", "planning to end my life", "going to harm myself"],
        "urgency": UrgencyLevel.EMERGENCY.value,
        "description": "Immediate self-harm safety support is needed.",
    },
]


_RULE_CONTEXTS = {
    "RULE_CARDIO_001": ("cardiovascular", "Does the chest discomfort feel like pressure or pain, or spread to your arm or jaw?", "This checks for the chest-pressure or radiating-pain warning signs used by the safety rules."),
    "RULE_RESP_001": ("respiratory", "Are you having severe trouble breathing, gasping, or noticing blue lips right now?", "This checks whether the breathing symptoms include an emergency warning sign."),
    "RULE_NEURO_001": ("neurological", "Did this start suddenly, or are you having facial drooping, slurred speech, or one-sided weakness?", "This checks for sudden neurological warning signs that need immediate attention."),
    "RULE_HEM_001": ("gastrointestinal", "Have you noticed blood in vomit or stool, or are you coughing up blood?", "This checks whether your symptoms include a significant bleeding warning sign."),
    "RULE_ABDO_001": ("gastrointestinal", "Is the abdominal pain severe or rapidly worsening, or does your abdomen feel rigid?", "This checks for the severe abdominal warning signs used by the safety rules."),
    "RULE_SEPSIS_001": ("systemic_infectious", "Along with the fever or illness, have you had confusion, blue or mottled skin, or been hard to wake?", "This checks whether systemic illness includes one of the emergency warning signs."),
    "RULE_DEHYDRATION_001": ("gastrointestinal", "Are you unable to keep fluids down, fainting, confused, or not urinating?", "This checks for the severe dehydration warning signs used by the safety rules."),
    "RULE_PREGNANCY_001": ("pregnancy_context", "Could you be pregnant, and if so, are you having heavy bleeding or severe abdominal pain?", "This checks whether pregnancy-related bleeding or severe pain is present."),
    "RULE_INFANT_FEVER_001": ("infant_context", "Is the child under 3 months old and currently feverish?", "This checks the age and fever facts used by the infant safety rule."),
    "RULE_SUICIDE_001": ("mental_health_context", "Are you in immediate danger of harming yourself right now?", "This checks whether you need immediate, personal safety support."),
}

_CATEGORY_ONTOLOGY = {
    "cardiovascular": "cardiovascular_symptom",
}


def _configure_rules(rules: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Add explicit production-system fields while retaining the original rule IDs."""
    for rule in rules:
        conditions: Dict[str, Any] = {}
        if rule.get("keywords"):
            conditions["any_symptom_phrase"] = list(rule["keywords"])
        parent = _CATEGORY_ONTOLOGY.get(rule.get("category"))
        if parent:
            conditions["any_isa"] = [parent]
        if "severity_min" in rule:
            conditions["severity_at_least"] = rule["severity_min"]
        if rule["id"] == "RULE_INFANT_FEVER_001":
            conditions["age_group_and_symptom"] = {"age_group": "under_3_months", "symptom": "fever"}
        rule["conditions"] = conditions
        rule["conclusion_fact"] = f"safety_rule_fired:{rule['id']}"
        rule["conclusion"] = rule["description"]
        rule["source"] = "Existing Healix deterministic safety heuristic; not a clinical guideline"
        rule["reference"] = f"Original Healix rule {rule['id']}"
    return rules


RED_FLAG_RULES = _configure_rules(RED_FLAG_RULES)


class WorkingMemory:
    """Small fact store; absent facts remain unknown rather than false."""

    def __init__(self):
        self.facts: List[Dict[str, Any]] = []
        self._keys = set()

    def add(self, predicate: str, value: Any, source: str, **metadata: Any) -> bool:
        key = (predicate, str(value), source)
        if key in self._keys:
            return False
        self._keys.add(key)
        self.facts.append({"predicate": predicate, "value": value, "source": source, **metadata})
        return True

    def has(self, predicate: str, value: Any) -> bool:
        value_key = str(value)
        return any(f["predicate"] == predicate and str(f["value"]) == value_key for f in self.facts)

    def matching(self, predicate: str) -> List[Dict[str, Any]]:
        return [fact for fact in self.facts if fact["predicate"] == predicate]


class TriageService:
    """Offline, safety-first forward-chaining production system."""

    def __init__(self, rules: Optional[List[Dict[str, Any]]] = None):
        self.rules = _configure_rules([dict(rule) for rule in rules]) if rules is not None else RED_FLAG_RULES

    @staticmethod
    def _group_age(age: Any) -> Optional[str]:
        try:
            years = float(age)
        except (TypeError, ValueError):
            return None
        if years < 0.25:
            return "under_3_months"
        if years < 2:
            return "infant"
        if years < 18:
            return "child_or_adolescent"
        if years < 65:
            return "adult"
        return "older_adult"

    def _seed_working_memory(
        self, description: str, symptoms: List[Dict[str, Any]], answers: List[Dict[str, Any]], extraction: Dict[str, Any]
    ) -> WorkingMemory:
        memory = WorkingMemory()
        active = extraction["active_symptoms"]
        for item in extraction.get("all_extracted", []):
            canonical = item.get("canonical_name", item.get("name", ""))
            pred = "negated_symptom" if item.get("is_negated") else "hypothetical_symptom" if item.get("is_hypothetical") else "has_symptom"
            memory.add(pred, canonical, "symptom_extractor")
            if pred == "has_symptom":
                for parent in ontology_facts(canonical):
                    memory.add("isa", parent, "symptom_ontology", child=concept_key(canonical))
            severity = item.get("severity_score")
            if severity is not None:
                memory.add("severity", severity, "symptom_extractor", symptom=canonical)
            duration = item.get("duration")
            if duration and duration != "unspecified":
                memory.add("duration", duration, "symptom_extractor", symptom=canonical)

        all_clauses: List[tuple[str, str]] = []
        cleaned = clean_clinical_text(description)
        all_clauses.extend((clause, "description") for clause in negation_detector.split_into_clauses(cleaned) if cleaned)
        for answer in answers:
            text = clean_clinical_text(answer.get("answer", ""))
            all_clauses.extend((clause, "answer") for clause in negation_detector.split_into_clauses(text) if text)

        for clause, source in all_clauses:
            for rule in self.rules:
                for keyword in rule.get("keywords", []):
                    pattern = r"\b" + re.escape(keyword) + r"\b"
                    if not re.search(pattern, clause, re.IGNORECASE):
                        continue
                    negated = negation_detector.is_negated(keyword, clause)
                    hypothetical = negation_detector.is_third_party_or_hypothetical(keyword, clause)
                    predicate = "negated_symptom" if negated else "hypothetical_symptom" if hypothetical else "has_symptom"
                    if not negated and not hypothetical:
                        memory.add(predicate, keyword.casefold(), source)
                    else:
                        memory.add(predicate, keyword.casefold(), source)

        for symptom in symptoms + active:
            symptom_name = str(symptom.get("name", "")).casefold()
            for rule in self.rules:
                for keyword in rule.get("keywords", []):
                    pattern = r"\b" + re.escape(keyword.casefold()) + r"\b"
                    if keyword.casefold() in symptom_name or re.search(pattern, symptom_name, re.IGNORECASE):
                        memory.add("has_symptom", keyword.casefold(), "structured_symptom")
            value = symptom.get("severity", symptom.get("severity_score"))
            if isinstance(value, (int, float)):
                memory.add("severity", value, "structured_symptom", symptom=symptom.get("name", ""))
            duration = symptom.get("duration")
            if duration:
                memory.add("duration", duration, "structured_symptom", symptom=symptom.get("name", ""))
            age = symptom.get("age")
            age_group = symptom.get("age_group") or (self._group_age(age) if age is not None else None)
            if age_group:
                memory.add("age_group", age_group, "structured_intake")
            if symptom.get("sex"):
                memory.add("sex", str(symptom["sex"]).casefold(), "structured_intake")
        return memory

    @staticmethod
    def _condition_matches(rule: Dict[str, Any], memory: WorkingMemory) -> List[Dict[str, Any]]:
        conditions = rule.get("conditions", {})
        matched: List[Dict[str, Any]] = []
        phrase_hits = [
            fact for fact in memory.matching("has_symptom")
            if fact["value"] in conditions.get("any_symptom_phrase", [])
        ]
        isa_hits = [
            fact for fact in memory.matching("isa")
            if fact["value"] in conditions.get("any_isa", [])
        ]
        severity_floor = conditions.get("severity_at_least")
        severity_hits = [
            fact for fact in memory.matching("severity")
            if severity_floor is not None and isinstance(fact["value"], (int, float)) and fact["value"] >= severity_floor
        ]
        if conditions.get("any_symptom_phrase") or conditions.get("any_isa"):
            matched = phrase_hits + isa_hits
        if severity_floor is not None:
            matched.extend(severity_hits)
        age_condition = conditions.get("age_group_and_symptom")
        if age_condition and memory.has("age_group", age_condition["age_group"]) and memory.has("has_symptom", age_condition["symptom"]):
            matched.extend(
                fact for fact in memory.facts
                if (fact["predicate"] == "age_group" and fact["value"] == age_condition["age_group"])
                or (fact["predicate"] == "has_symptom" and fact["value"] == age_condition["symptom"])
            )
        return matched

    def _backward_chain_questions(
        self, memory: WorkingMemory, extraction: Dict[str, Any], description: str, fired_ids: set[str]
    ) -> List[Dict[str, Any]]:
        """Find missing emergency-rule facts relevant to the currently described context."""
        known_contexts = set(extraction.get("categories", []))
        clean = clean_clinical_text(description).casefold()
        questions = []
        for rule in self.rules:
            if rule.get("urgency") != UrgencyLevel.EMERGENCY.value or rule["id"] in fired_ids:
                continue
            context, question, reason = _RULE_CONTEXTS.get(rule["id"], (None, None, None))
            context_present = context in known_contexts
            if context == "pregnancy_context":
                context_present = any(w in clean for w in ("pregnan", "pregnant", "pregnancy"))
            elif context == "infant_context":
                context_present = "infant" in clean or "newborn" in clean or "under 3 month" in clean
            elif context == "mental_health_context":
                context_present = any(w in clean for w in ("suicid", "self-harm", "harm myself", "hurt myself"))
            if not context_present or not question:
                continue
            missing = [
                {"predicate": "has_symptom", "value": phrase}
                for phrase in rule.get("keywords", [])
                if not memory.has("has_symptom", phrase.casefold())
            ]
            if not missing:
                continue
            questions.append({
                "question": question,
                "reasoning": reason,
                "type": "free_text",
                "order_index": len(questions),
                "priority": "safety_confirmation",
                "rule_id": rule["id"],
                "unknown_facts": missing,
            })
            if len(questions) >= 3:
                break
        return questions

    def evaluate(
        self,
        description: str = "",
        symptoms: Optional[List[Dict[str, Any]]] = None,
        answers: Optional[List[Dict[str, Any]]] = None,
        age: Optional[int] = None,
        sex: Optional[str] = None,
    ) -> Dict[str, Any]:
        symptoms, answers = symptoms or [], answers or []
        cleaned_desc = clean_clinical_text(description)
        extraction = symptom_engine.extract(text=cleaned_desc, preselected_symptoms=symptoms)
        memory = self._seed_working_memory(description, symptoms, answers, extraction)
        age_group = self._group_age(age) if age is not None else None
        if age_group:
            memory.add("age_group", age_group, "profile")
        if sex:
            memory.add("sex", str(sex).casefold(), "profile")
        trace: List[Dict[str, Any]] = []
        fired: Dict[str, Dict[str, Any]] = {}

        # Forward-chain to a fixed point. Each rule can add its conclusion once.
        changed = True
        while changed:
            changed = False
            for rule in self.rules:
                if rule["id"] in fired:
                    continue
                matches = self._condition_matches(rule, memory)
                if not matches:
                    continue
                trace_item = {
                    "rule_id": rule["id"],
                    "matched_facts": [dict(fact) for fact in matches],
                    "conclusion": rule["conclusion"],
                    "conclusion_fact": rule["conclusion_fact"],
                    "urgency": rule["urgency"],
                    "source": rule["source"],
                    "reference": rule["reference"],
                }
                fired[rule["id"]] = trace_item
                trace.append(trace_item)
                changed = memory.add("rule_fired", rule["id"], "forward_chaining") or changed
                changed = memory.add("urgency", rule["urgency"], "forward_chaining", rule_id=rule["id"]) or changed
                changed = memory.add("conclusion", rule["conclusion_fact"], "forward_chaining", text=rule["conclusion"]) or changed

        fired_rules = [rule for rule in self.rules if rule["id"] in fired]
        fired_ids = set(fired)
        highest_urgency = UrgencyLevel.ROUTINE.value
        if any(r["urgency"] == UrgencyLevel.EMERGENCY.value for r in fired_rules):
            highest_urgency = UrgencyLevel.EMERGENCY.value
        elif any(r["urgency"] == UrgencyLevel.URGENT.value for r in fired_rules):
            highest_urgency = UrgencyLevel.URGENT.value

        is_unknown_or_ambiguous = extraction["is_unknown_or_ambiguous"]
        if highest_urgency == UrgencyLevel.EMERGENCY.value:
            if "RULE_SUICIDE_001" in fired_ids:
                message = (
                    "Your immediate safety matters. If you may act on thoughts of self-harm, contact local emergency services or a crisis line now, "
                    "stay with someone you trust, and move away from anything you could use to hurt yourself."
                )
            else:
                message = (
                    "IMPORTANT: Symptoms reported may indicate an acute medical emergency. "
                    "Healix cannot determine the cause of your symptoms. "
                    "Please contact your local emergency services (or go to the nearest emergency department) immediately."
                )
            requires_professional_attention = True
        elif highest_urgency == UrgencyLevel.URGENT.value:
            message = "Symptoms reported suggest you should be evaluated promptly by a healthcare professional or at an urgent care clinic within 12 to 24 hours."
            requires_professional_attention = True
        elif is_unknown_or_ambiguous:
            highest_urgency = UrgencyLevel.UNKNOWN.value
            message = (
                "Healix could not identify specific medical symptoms from your description. We cannot determine the nature of your concern. "
                "Please provide more detail about what you are experiencing, its duration, and severity, or consult a healthcare professional for guidance."
            )
            requires_professional_attention = False
        else:
            message = "The safety rules did not identify an emergency from the information provided. This does not rule out a serious cause. Contact a healthcare professional if symptoms persist, worsen, or concern you."
            requires_professional_attention = False

        priority_questions = [] if highest_urgency == UrgencyLevel.EMERGENCY.value else self._backward_chain_questions(
            memory, extraction, description, fired_ids
        )
        return {
            "urgency_level": highest_urgency,
            "triggered_rules": [r["id"] for r in fired_rules],
            "message": message,
            "requires_professional_attention": requires_professional_attention,
            "clinical_notes": [r["description"] for r in fired_rules],
            "active_symptoms": extraction["active_symptoms"],
            "is_ambiguous": is_unknown_or_ambiguous,
            "reasoning_trace": trace,
            "working_memory": list(memory.facts),
            "priority_questions": priority_questions,
        }
