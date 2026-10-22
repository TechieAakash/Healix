from typing import List, Tuple, Dict, Any
from uuid import UUID
from datetime import date
from sqlalchemy.orm import Session
from app.models.assessment import Assessment
from app.models.follow_up import FollowUpQuestion, FollowUpAnswer
from app.models.report import Report
from app.repositories.assessment_repository import AssessmentRepository
from app.repositories.symptom_repository import SymptomRepository
from app.repositories.report_repository import ReportRepository
from app.services.triage_service import TriageService
from app.services.clinical.ddxplus_ranker import ddxplus_ranker
from app.services.clinical.evidence_mapper import evidence_mapper
from app.services.clinical.question_search import EvidenceQuestionSearch
from app.services.ai.assessment_agent import AssessmentAgent
from app.schemas.assessment import AssessmentCreateRequest, AssessmentAnalyzeResponse
from app.core.exceptions import EntityNotFoundException
from app.utils.constants import AssessmentStatus, UrgencyLevel, QuestionType, STANDARD_MEDICAL_DISCLAIMER


class AssessmentService:
    def __init__(self, db: Session):
        self.db = db
        self.assessment_repo = AssessmentRepository(db)
        self.symptom_repo = SymptomRepository(db)
        self.report_repo = ReportRepository(db)
        self.triage_service = TriageService()
        self.question_search = EvidenceQuestionSearch()
        self.assessment_agent = AssessmentAgent()

    @staticmethod
    def _profile(assessment: Assessment) -> Tuple[int | None, str | None]:
        user = assessment.user
        if not user:
            return None, None
        age = None
        if user.date_of_birth:
            today = date.today()
            age = today.year - user.date_of_birth.year - ((today.month, today.day) < (user.date_of_birth.month, user.date_of_birth.day))
        return age, user.gender

    def create_assessment(self, user_id: str, req: AssessmentCreateRequest) -> Assessment:
        from app.models.symptom import Symptom
        from app.services.clinical.symptom_engine import symptom_engine

        symptoms = []
        seen_ids = set()
        detailed_by_name = {}

        # Structured intake is authoritative when the frontend submits both
        # chips and their metadata. Create each symptom once with its actual data.
        for item in req.symptom_data:
            data = item.model_dump()
            name = data["name"].strip()
            name_key = name.casefold()
            if name_key in detailed_by_name:
                continue
            symptom = Symptom(
                user_id=user_id,
                name=name,
                severity=data["severity"],
                body_location=data.get("body_location") or data.get("location"),
                duration=data.get("duration"),
                frequency=data.get("frequency"),
                description=data.get("description"),
            )
            self.db.add(symptom)
            symptoms.append(symptom)
            detailed_by_name[name_key] = symptom

        # Support existing symptom IDs and legacy name-only requests. Names
        # already represented by symptom_data must not create duplicate rows.
        if req.symptoms:
            existing = self.symptom_repo.get_by_ids_and_user(req.symptoms, user_id)
            existing_by_id = {s.id: s for s in existing}
            for item in req.symptoms:
                if item in existing_by_id:
                    if item not in seen_ids:
                        symptoms.append(existing_by_id[item])
                        seen_ids.add(item)
                    continue

                clean_name = item.strip()
                try:
                    UUID(clean_name)
                except (ValueError, AttributeError):
                    pass
                else:
                    # A UUID-shaped value that is not owned by this user is
                    # an invalid reference, not a free-text symptom name.
                    raise EntityNotFoundException("Symptom", clean_name)
                if len(clean_name) >= 2 and clean_name.casefold() not in detailed_by_name:
                    symptom = Symptom(
                        user_id=user_id,
                        name=clean_name,
                        severity=5,
                        body_location="unspecified",
                    )
                    self.db.add(symptom)
                    symptoms.append(symptom)
                    detailed_by_name[clean_name.casefold()] = symptom

        # 3. If no symptoms attached but description provided, extract deterministically
        if not symptoms and req.description:
            extraction = symptom_engine.extract(req.description)
            for s_item in extraction.get("active_symptoms", []):
                new_sym = Symptom(
                    user_id=user_id,
                    name=s_item["canonical_name"].capitalize(),
                    severity=s_item.get("severity_score", 5),
                    body_location=s_item.get("body_location", "unspecified"),
                    duration=s_item.get("duration", "unspecified"),
                )
                self.db.add(new_sym)
                symptoms.append(new_sym)

        assessment = Assessment(
            user_id=user_id,
            status=AssessmentStatus.SYMPTOMS_COLLECTED.value,
            urgency_level=UrgencyLevel.UNKNOWN.value,
            user_description=req.description,
            symptoms=symptoms,
        )
        return self.assessment_repo.create(assessment)

    def get_assessment(self, assessment_id: str, user_id: str) -> Assessment:
        assessment = self.assessment_repo.get_by_id_and_user(assessment_id, user_id)
        if not assessment:
            raise EntityNotFoundException("Assessment", assessment_id)
        return assessment

    def list_assessments(self, user_id: str, page: int = 1, page_size: int = 20) -> Tuple[List[Assessment], int]:
        skip = (page - 1) * page_size
        items = self.assessment_repo.get_all_by_user(user_id, skip=skip, limit=page_size)
        total = self.assessment_repo.count_by_user(user_id)
        return items, total

    async def get_or_generate_questions(self, assessment_id: str, user_id: str) -> List[FollowUpQuestion]:
        assessment = self.get_assessment(assessment_id, user_id)

        unanswered = [q for q in assessment.follow_up_questions if not q.answers]
        if unanswered:
            return unanswered

        symptoms_data = [
            {"name": s.name, "severity": s.severity, "description": s.description}
            for s in assessment.symptoms
        ]
        # Questions are deterministic and safety focused. If an emergency
        # rule already fired, do not keep the user in an intake flow.
        age, sex = self._profile(assessment)
        answers_data = [
            {"question": q.question, "answer": a.answer, "evidence_code": q.evidence_code}
            for q in assessment.follow_up_questions for a in q.answers
        ]
        pre_triage = self.triage_service.evaluate(
            description=assessment.user_description or "",
            symptoms=symptoms_data,
            answers=answers_data,
            age=age,
            sex=sex,
        )
        q_dicts = []
        if pre_triage["urgency_level"] != UrgencyLevel.EMERGENCY.value and len(assessment.follow_up_questions) < 5:
            existing_question_text = {" ".join(q.question.casefold().split()) for q in assessment.follow_up_questions}
            safety_questions = [q for q in pre_triage.get("priority_questions", []) if " ".join(q.get("question", "").casefold().split()) not in existing_question_text]
            if safety_questions:
                q_dicts = safety_questions[:1]
            else:
                mapping = evidence_mapper.map_assessment(assessment.user_description or "", symptoms_data, answers_data, age=age, sex=sex)
                positive = {
                    c.split("_@_")[0] for c in mapping["evidence"]
                    if evidence_mapper.definitions.get(c.split("_@_")[0], {}).get("data_type") == "B"
                }
                negative = {
                    code for code in mapping["negated_codes"]
                    if evidence_mapper.definitions.get(code, {}).get("data_type") == "B"
                }
                ranking = ddxplus_ranker.rank(mapping["evidence"])
                chosen = None
                state = self.assessment_agent.update_state(
                    assessment.user_description or "", symptoms_data, answers_data,
                    pre_triage, ranking, 5 - len(assessment.follow_up_questions),
                )
                if self.assessment_agent.select_action(state, has_candidate_question=True) == AssessmentAgent.ACTION_ASK:
                    asked_codes = {q.evidence_code for q in assessment.follow_up_questions if q.evidence_code}
                    chosen = self.question_search.choose(set(mapping["contexts"]), positive, negative, asked_codes, method="lookahead")
                if chosen:
                    q_dicts = [{
                        "question": chosen["question"],
                        "type": QuestionType.SINGLE_CHOICE.value,
                        "options": ["Yes", "No", "Not sure"],
                        "evidence_code": chosen["code"],
                        "reasoning": "This question was selected to reduce uncertainty among synthetic DDXPlus patterns. It cannot diagnose a condition.",
                    }]
                elif not assessment.follow_up_questions:
                    q_dicts = self._build_follow_up_questions(assessment.user_description or "", symptoms_data)[:1]

        question_entities = [
            FollowUpQuestion(
                assessment_id=assessment.id,
                question=q["question"],
                reasoning=q.get("reasoning"),
                evidence_code=q.get("evidence_code"),
                question_type=q.get("type", QuestionType.SINGLE_CHOICE.value),
                order_index=len(assessment.follow_up_questions) + idx,
            )
            for idx, q in enumerate(q_dicts)
        ]

        saved_questions = self.assessment_repo.create_follow_up_questions(question_entities)
        assessment.status = AssessmentStatus.FOLLOW_UP.value
        self.assessment_repo.update(assessment)
        return saved_questions

    @staticmethod
    def _build_follow_up_questions(description: str, symptoms: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Select a small, fixed set of clarifying questions without an LLM."""
        from app.services.clinical.symptom_engine import symptom_engine

        parsed = symptom_engine.extract(
            description,
            preselected_symptoms=symptoms,
        )
        categories = set(parsed["categories"])
        questions = [
            "When did these symptoms begin, and have they changed since then?",
            "How much are these symptoms affecting your usual daily activities?",
        ]
        if "respiratory" in categories or "cardiovascular" in categories:
            questions.insert(0, "Are you having severe trouble breathing, fainting, or new chest pressure right now?")
        elif "neurological" in categories:
            questions.insert(0, "Did the symptoms start suddenly, or are you experiencing new weakness, confusion, or trouble speaking?")
        elif "gastrointestinal" in categories:
            questions.insert(0, "Are you unable to keep fluids down, or have you noticed blood in vomit or stool?")
        else:
            questions.insert(0, "Are any symptoms severe, rapidly worsening, or making it difficult to stay safe?")

        return [
            {
                "question": question,
                "type": QuestionType.TEXT.value,
                "order_index": index,
            }
            for index, question in enumerate(questions)
        ]

    def answer_question(
        self, assessment_id: str, question_id: str, user_id: str, answer_text: str
    ) -> FollowUpAnswer:
        assessment = self.get_assessment(assessment_id, user_id)
        question = self.assessment_repo.get_question_by_id_and_assessment(question_id, assessment.id)
        if not question:
            raise EntityNotFoundException("FollowUpQuestion", question_id)

        answer = FollowUpAnswer(question_id=question.id, answer=answer_text)
        return self.assessment_repo.create_follow_up_answer(answer)

    async def analyze_assessment(self, assessment_id: str, user_id: str) -> AssessmentAnalyzeResponse:
        assessment = self.get_assessment(assessment_id, user_id)

        # Update state to ANALYZING
        assessment.status = AssessmentStatus.ANALYZING.value
        self.assessment_repo.update(assessment)

        try:
            # Gather context
            symptoms_data = [
                {
                    "name": s.name,
                    "severity": s.severity,
                    "description": s.description,
                    "location": s.body_location,
                    "duration": s.duration,
                }
                for s in assessment.symptoms
            ]
            answers_data = [
                {"question": q.question, "answer": a.answer, "evidence_code": q.evidence_code}
                for q in assessment.follow_up_questions
                for a in q.answers
            ]

            # STEP 1: Run Deterministic Red-Flag Triage Engine FIRST
            age, sex = self._profile(assessment)
            triage_result = self.triage_service.evaluate(
                description=assessment.user_description or "",
                symptoms=symptoms_data,
                answers=answers_data,
                age=age,
                sex=sex,
            )

            ranking_result = ddxplus_ranker.analyze(
                assessment.user_description or "", symptoms_data, answers_data, age=age, sex=sex
            )["ranking"]
            agent_state = self.assessment_agent.update_state(
                assessment.user_description or "", symptoms_data, answers_data,
                triage_result, ranking_result, 0,
            )
            # This documents/executes the terminal action. Safety escalation
            # remains represented by triage_result and is never model-overridden.
            agent_action = self.assessment_agent.select_action(agent_state)
            if agent_action in {AssessmentAgent.ACTION_ABSTAIN, AssessmentAgent.ACTION_ESCALATE}:
                ranking_result = {**ranking_result, "ranked_conditions": []}

            # The built-in local provider performs deterministic extraction and
            # retrieves educational content from the bundled offline index.
            # Triage above remains the authority for urgency.
            from app.services.ai_service import get_ai_service
            summary_result = await get_ai_service().generate_summary(
                description=assessment.user_description or "",
                symptoms=symptoms_data,
                answers=answers_data,
                triage_result=triage_result,
                assessment_id=assessment.id,
            )

            # STEP 3: Create or Update Clinical Report
            primary_symptom = assessment.symptoms[0].name if assessment.symptoms else "Health Assessment"
            existing_report = self.report_repo.get_by_assessment_id(assessment.id)
            if existing_report:
                existing_report.title = f"Assessment Report: {primary_symptom}"
                existing_report.summary = summary_result["summary"]
                existing_report.urgency_level = triage_result["urgency_level"]
                existing_report.possible_explanations = summary_result["possible_explanations"]
                existing_report.general_guidance = summary_result["general_guidance"]
                existing_report.warning_signs = summary_result["warning_signs"]
                existing_report.sources = summary_result["sources"]
                existing_report.reasoning_trace = triage_result.get("reasoning_trace", [])
                existing_report.condition_ranking = ranking_result.get("ranked_conditions", [])
                self.report_repo.update(existing_report)
            else:
                report = Report(
                    assessment_id=assessment.id,
                    title=f"Assessment Report: {primary_symptom}",
                    summary=summary_result["summary"],
                    urgency_level=triage_result["urgency_level"],
                    possible_explanations=summary_result["possible_explanations"],
                    general_guidance=summary_result["general_guidance"],
                    warning_signs=summary_result["warning_signs"],
                    sources=summary_result["sources"],
                    reasoning_trace=triage_result.get("reasoning_trace", []),
                    condition_ranking=ranking_result.get("ranked_conditions", []),
                )
                self.report_repo.create(report)

            # STEP 4: Mark assessment COMPLETED
            assessment.status = AssessmentStatus.COMPLETED.value
            assessment.urgency_level = triage_result["urgency_level"]
            assessment.summary = summary_result["summary"]
            self.assessment_repo.update(assessment)

            return AssessmentAnalyzeResponse(
                assessment_id=assessment.id,
                urgency_level=triage_result["urgency_level"],
                summary=summary_result["summary"],
                possible_explanations=summary_result["possible_explanations"],
                general_guidance=summary_result["general_guidance"],
                warning_signs=summary_result["warning_signs"],
                sources=summary_result["sources"],
                reasoning_trace=triage_result.get("reasoning_trace", []),
                condition_ranking=ranking_result.get("ranked_conditions", []),
                disclaimer=STANDARD_MEDICAL_DISCLAIMER,
            )
        except Exception as e:
            assessment.status = AssessmentStatus.FAILED.value
            self.assessment_repo.update(assessment)
            from app.core.exceptions import AnalysisFailedException
            raise AnalysisFailedException(str(e))

    @staticmethod
    def _build_deterministic_summary(
        description: str,
        symptoms_data: List[Dict[str, Any]],
        triage_result: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Build explainable, non-diagnostic findings from Python rules only."""
        from app.services.clinical.pattern_classifier import symptom_pattern_classifier

        urgency = triage_result["urgency_level"]
        symptom_patterns = symptom_pattern_classifier.classify(description, symptoms_data)
        symptom_names = list(dict.fromkeys(
            s.get("name", "").strip() for s in symptoms_data if s.get("name", "").strip()
        ))
        reported = ", ".join(symptom_names) if symptom_names else "the concern you described"

        if urgency == UrgencyLevel.EMERGENCY.value:
            guidance = [triage_result["message"]]
        elif urgency == UrgencyLevel.URGENT.value:
            guidance = [triage_result["message"]]
        elif urgency == UrgencyLevel.UNKNOWN.value:
            guidance = [triage_result["message"]]
        else:
            guidance = [
                "Track when symptoms occur, how they change, and any relevant triggers.",
                "Seek advice from a healthcare professional if symptoms persist, worsen, or concern you.",
            ]

        warning_signs = [] if urgency == UrgencyLevel.EMERGENCY.value else [
            "Seek immediate help for severe breathing difficulty, new chest pressure, fainting, confusion, or sudden weakness.",
            "Contact a healthcare professional if symptoms become severe or rapidly worsen.",
        ]
        summary = (
            f"This health-information review records: {reported}. "
            f"{triage_result['message']}"
        )
        return {
            "summary": summary,
            "possible_explanations": symptom_patterns,
            "general_guidance": guidance,
            "warning_signs": warning_signs,
            # No evidence source is cited unless the result actually uses it.
            "sources": [],
        }
