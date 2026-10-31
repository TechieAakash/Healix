from typing import List
from ..facts import FactValue
from ..rules import (
    Rule, RuleCategory, SimpleCondition, CompoundCondition, Operator,
    Conclusion, RecommendationTier
)

KB_VERSION = "v2.0.0"

def get_clinical_knowledge_base() -> List[Rule]:
    return [
        # =====================================================================
        # 1. EMERGENCY RED FLAG RULES (Priority 1000)
        # =====================================================================
        Rule(
            id="RULE_EMERGENCY_THUNDERCLAP",
            name="Emergency Red Flag: Thunderclap Cephalea",
            description="Sudden excruciating headache reaching peak within 60 seconds poses risk of subarachnoid hemorrhage.",
            priority=1000,
            category=RuleCategory.EMERGENCY_RED_FLAG,
            version=KB_VERSION,
            provenance="American College of Emergency Physicians (ACEP) Neurovascular Guidelines",
            conditions=SimpleCondition(
                fact_name="symptom.headache.onset_thunderclap",
                operator=Operator.EQUALS,
                target_value=FactValue.TRUE
            ),
            conclusions=[
                Conclusion(
                    id="CONC_RED_FLAG_THUNDERCLAP",
                    fact_name="observation.emergency.subarachnoid_risk",
                    asserted_value=FactValue.TRUE,
                    confidence=1.0,
                    category="EMERGENCY",
                    summary="CRITICAL RED FLAG: Thunderclap Headache Pattern Detected",
                    detailed_explanation="Sudden 'worst headache of life' peaking within seconds requires immediate neuroimaging (CT/LP) to exclude vascular rupture.",
                    recommendation_tier=RecommendationTier.EMERGENCY,
                    actionable_steps=[
                        "Dial emergency medical services (911 / 112) immediately.",
                        "Do not drive yourself to the emergency department.",
                        "Refrain from taking aspirin or blood-thinning analgesics until medical imaging is completed."
                    ]
                )
            ]
        ),

        Rule(
            id="RULE_EMERGENCY_MENINGISM",
            name="Emergency Red Flag: Acute Meningeal Irritation",
            description="Combination of fever, neck stiffness (nuchal rigidity), and altered sensorium indicates possible central nervous system infection.",
            priority=1000,
            category=RuleCategory.EMERGENCY_RED_FLAG,
            version=KB_VERSION,
            provenance="Infectious Diseases Society of America (IDSA) Bacterial Meningitis Management Standards",
            conditions=CompoundCondition(
                logical_operator="AND",
                conditions=[
                    SimpleCondition(fact_name="symptom.fever", operator=Operator.EQUALS, target_value=FactValue.TRUE),
                    SimpleCondition(fact_name="symptom.neck_stiffness", operator=Operator.EQUALS, target_value=FactValue.TRUE),
                    SimpleCondition(fact_name="symptom.headache.present", operator=Operator.EQUALS, target_value=FactValue.TRUE)
                ]
            ),
            conclusions=[
                Conclusion(
                    id="CONC_RED_FLAG_MENINGISM",
                    fact_name="observation.emergency.meningism_risk",
                    asserted_value=FactValue.TRUE,
                    confidence=1.0,
                    category="EMERGENCY",
                    summary="CRITICAL RED FLAG: Meningeal Triad (Fever + Neck Rigidity + Cephalea)",
                    detailed_explanation="Nuchal rigidity combined with systemic pyrexia requires emergent evaluation for bacterial or viral meningoencephalitis.",
                    recommendation_tier=RecommendationTier.EMERGENCY,
                    actionable_steps=[
                        "Proceed immediately to the nearest Emergency Department.",
                        "Do not delay for symptomatic home remedies.",
                        "Avoid unprescribed antibiotic administration prior to clinical blood cultures."
                    ]
                )
            ]
        ),

        Rule(
            id="RULE_EMERGENCY_ACS",
            name="Emergency Red Flag: Acute Coronary Constellation",
            description="Crushing retrosternal chest pain radiating to left arm/jaw with dyspnea suggests acute myocardial ischemia.",
            priority=1000,
            category=RuleCategory.EMERGENCY_RED_FLAG,
            version=KB_VERSION,
            provenance="American Heart Association / American College of Cardiology (AHA/ACC) ACS Guidelines",
            conditions=CompoundCondition(
                logical_operator="AND",
                conditions=[
                    SimpleCondition(fact_name="symptom.chest_pain.crushing", operator=Operator.EQUALS, target_value=FactValue.TRUE),
                    CompoundCondition(
                        logical_operator="OR",
                        conditions=[
                            SimpleCondition(fact_name="symptom.chest_pain.radiation_left_arm", operator=Operator.EQUALS, target_value=FactValue.TRUE),
                            SimpleCondition(fact_name="symptom.dyspnea", operator=Operator.EQUALS, target_value=FactValue.TRUE)
                        ]
                    )
                ]
            ),
            conclusions=[
                Conclusion(
                    id="CONC_RED_FLAG_ACS",
                    fact_name="observation.emergency.myocardial_ischemia_risk",
                    asserted_value=FactValue.TRUE,
                    confidence=1.0,
                    category="EMERGENCY",
                    summary="CRITICAL RED FLAG: Acute Coronary / Ischemic Syndrome Warning",
                    detailed_explanation="Substernal crushing chest pain with radiation or shortness of breath meets criteria for immediate emergency medical dispatch to rule out acute myocardial infarction.",
                    recommendation_tier=RecommendationTier.EMERGENCY,
                    actionable_steps=[
                        "Dial 911 / 112 immediately. Inform the dispatcher of crushing chest discomfort.",
                        "Chew a single adult aspirin (325 mg) if not allergic and advised by dispatch.",
                        "Rest seated upright and minimize any physical movement."
                    ]
                )
            ]
        ),

        Rule(
            id="RULE_EMERGENCY_APPENDICITIS",
            name="Emergency Red Flag: Acute Lower Abdominal Surgical Sign",
            description="Severe acute pain localizing to Right Lower Quadrant (RLQ) accompanied by fever.",
            priority=1000,
            category=RuleCategory.EMERGENCY_RED_FLAG,
            version=KB_VERSION,
            provenance="World Society of Emergency Surgery (WSES) Acute Abdomen Guidelines",
            conditions=CompoundCondition(
                logical_operator="AND",
                conditions=[
                    SimpleCondition(fact_name="symptom.abdominal.rlq_localization", operator=Operator.EQUALS, target_value=FactValue.TRUE),
                    SimpleCondition(fact_name="symptom.fever", operator=Operator.EQUALS, target_value=FactValue.TRUE)
                ]
            ),
            conclusions=[
                Conclusion(
                    id="CONC_RED_FLAG_APPENDICITIS",
                    fact_name="observation.emergency.appendicitis_risk",
                    asserted_value=FactValue.TRUE,
                    confidence=0.96,
                    category="EMERGENCY",
                    summary="CRITICAL RED FLAG: Acute Surgical Abdomen (Peritoneal / Appendiceal Sign)",
                    detailed_explanation="Focal RLQ tenderness combined with systemic pyrexia requires physical surgical assessment and ultrasound/CT to exclude acute appendicitis.",
                    recommendation_tier=RecommendationTier.EMERGENCY,
                    actionable_steps=[
                        "Proceed promptly to an emergency medical facility.",
                        "Maintain NPO status (refrain from eating or drinking fluids) in preparation for potential surgical evaluation.",
                        "Do not administer heating pads or laxatives to the abdomen."
                    ]
                )
            ]
        ),

        # =====================================================================
        # 2. CLINICAL TRIAGE RULES (Priority 500 - 400)
        # =====================================================================
        Rule(
            id="RULE_MIGRAINE_042",
            name="Clinical Triage: Neurovascular Cephalea (Migraine Pattern)",
            description="Recurrent unilateral throbbing headache aggravated by routine activity and accompanied by photophobia or nausea.",
            priority=500,
            category=RuleCategory.CLINICAL_TRIAGE,
            version=KB_VERSION,
            provenance="International Classification of Headache Disorders 3rd Edition (ICHD-3) 1.1",
            conditions=CompoundCondition(
                logical_operator="AND",
                conditions=[
                    SimpleCondition(fact_name="symptom.headache.present", operator=Operator.EQUALS, target_value=FactValue.TRUE),
                    CompoundCondition(
                        logical_operator="OR",
                        conditions=[
                            SimpleCondition(fact_name="symptom.headache.throbbing", operator=Operator.EQUALS, target_value=FactValue.TRUE),
                            SimpleCondition(fact_name="symptom.headache.unilateral", operator=Operator.EQUALS, target_value=FactValue.TRUE),
                            SimpleCondition(fact_name="symptom.headache.visual_aura", operator=Operator.EQUALS, target_value=FactValue.TRUE)
                        ]
                    ),
                    CompoundCondition(
                        logical_operator="OR",
                        conditions=[
                            SimpleCondition(fact_name="symptom.photophobia", operator=Operator.EQUALS, target_value=FactValue.TRUE),
                            SimpleCondition(fact_name="symptom.nausea", operator=Operator.EQUALS, target_value=FactValue.TRUE)
                        ]
                    ),
                    SimpleCondition(fact_name="symptom.headache.onset_thunderclap", operator=Operator.NOT_EQUALS, target_value=FactValue.TRUE),
                    SimpleCondition(fact_name="symptom.neck_stiffness", operator=Operator.NOT_EQUALS, target_value=FactValue.TRUE)
                ]
            ),
            conclusions=[
                Conclusion(
                    id="CONC_TRIAGE_MIGRAINE",
                    fact_name="observation.triage.migraine_pattern",
                    asserted_value=FactValue.TRUE,
                    confidence=0.92,
                    category="OBSERVATION",
                    summary="Benign Neurovascular Cephalea (Consistent with Migraine Pattern)",
                    detailed_explanation="Symptom constellation of pulsating unilateral pain with sensory hypersensitivity matches clinical migraine criteria. Emergency intracranial red flags are absent.",
                    recommendation_tier=RecommendationTier.CONSULT_PHYSICIAN,
                    actionable_steps=[
                        "Schedule an outpatient evaluation with a primary care physician or neurologist.",
                        "Maintain a headache diary logging triggers, duration, and food intake.",
                        "Rest in a quiet, dark, temperature-controlled environment."
                    ]
                )
            ]
        ),

        Rule(
            id="RULE_HEADACHE_FEBRILE_022",
            name="Clinical Triage: Systemic Febrile Cephalea",
            description="Headache accompanied by fever without meningeal signs or acute focal neurological deficits.",
            priority=490,
            category=RuleCategory.CLINICAL_TRIAGE,
            version=KB_VERSION,
            provenance="American Academy of Family Physicians (AAFP) Headache Assessment Guidelines",
            conditions=CompoundCondition(
                logical_operator="AND",
                conditions=[
                    SimpleCondition(fact_name="symptom.headache.present", operator=Operator.EQUALS, target_value=FactValue.TRUE),
                    SimpleCondition(fact_name="symptom.fever", operator=Operator.EQUALS, target_value=FactValue.TRUE),
                    SimpleCondition(fact_name="symptom.neck_stiffness", operator=Operator.NOT_EQUALS, target_value=FactValue.TRUE),
                    SimpleCondition(fact_name="symptom.headache.onset_thunderclap", operator=Operator.NOT_EQUALS, target_value=FactValue.TRUE)
                ]
            ),
            conclusions=[
                Conclusion(
                    id="CONC_TRIAGE_FEBRILE_HEADACHE",
                    fact_name="observation.triage.febrile_headache_pattern",
                    asserted_value=FactValue.TRUE,
                    confidence=0.89,
                    category="OBSERVATION",
                    summary="Acute Febrile Cephalea (Systemic Infection-Related Headache)",
                    detailed_explanation="Co-occurrence of headache and systemic pyrexia in the absence of nuchal rigidity suggests a systemic viral or bacterial infection causing secondary vascular dilation.",
                    recommendation_tier=RecommendationTier.CONSULT_PHYSICIAN,
                    actionable_steps=[
                        "Consult an outpatient physician for targeted infectious evaluation.",
                        "Maintain hydration and use antipyretics (e.g. acetaminophen) as directed by clinical guidance.",
                        "Seek immediate medical attention if new neck stiffness, confusion, or rash develops."
                    ]
                )
            ]
        ),

        Rule(
            id="RULE_TENSION_HEADACHE_015",
            name="Clinical Triage: Tension-Type Headache Pattern",
            description="Bilateral, non-pulsating band-like pressure of mild to moderate intensity without nausea or vomiting.",
            priority=480,
            category=RuleCategory.CLINICAL_TRIAGE,
            version=KB_VERSION,
            provenance="ICHD-3 Diagnostic Criteria 2.1 (Episodic Tension-Type Headache)",
            conditions=CompoundCondition(
                logical_operator="AND",
                conditions=[
                    SimpleCondition(fact_name="symptom.headache.present", operator=Operator.EQUALS, target_value=FactValue.TRUE),
                    CompoundCondition(
                        logical_operator="OR",
                        conditions=[
                            SimpleCondition(fact_name="symptom.headache.band_like_pressure", operator=Operator.EQUALS, target_value=FactValue.TRUE),
                            SimpleCondition(fact_name="symptom.headache.bilateral", operator=Operator.EQUALS, target_value=FactValue.TRUE)
                        ]
                    ),
                    SimpleCondition(fact_name="symptom.nausea", operator=Operator.NOT_EQUALS, target_value=FactValue.TRUE),
                    SimpleCondition(fact_name="symptom.headache.onset_thunderclap", operator=Operator.NOT_EQUALS, target_value=FactValue.TRUE)
                ]
            ),
            conclusions=[
                Conclusion(
                    id="CONC_TRIAGE_TENSION",
                    fact_name="observation.triage.tension_headache_pattern",
                    asserted_value=FactValue.TRUE,
                    confidence=0.88,
                    category="OBSERVATION",
                    summary="Episodic Musculoskeletal/Tension-Type Headache Pattern",
                    detailed_explanation="Bilateral pressing quality without autonomic nausea suggests pericranial muscle strain or stress-related tension headache.",
                    recommendation_tier=RecommendationTier.SELF_MONITOR,
                    actionable_steps=[
                        "Evaluate ergonomic posture, screen brightness, and cervical spine support.",
                        "Hydrate adequately and practice stress-reduction or progressive muscle relaxation.",
                        "Seek medical consultation if frequency exceeds 15 days per month."
                    ]
                )
            ]
        ),

        Rule(
            id="RULE_PRIMARY_HEADACHE_GENERAL",
            name="Clinical Triage: General Cephalea Symptom Pattern",
            description="Headache present without emergency red flags, consistent with common primary outpatient cephalea.",
            priority=450,
            category=RuleCategory.CLINICAL_TRIAGE,
            version=KB_VERSION,
            provenance="ICHD-3 Primary Headache Evaluation Consensus",
            conditions=CompoundCondition(
                logical_operator="AND",
                conditions=[
                    SimpleCondition(fact_name="symptom.headache.present", operator=Operator.EQUALS, target_value=FactValue.TRUE),
                    SimpleCondition(fact_name="symptom.headache.onset_thunderclap", operator=Operator.NOT_EQUALS, target_value=FactValue.TRUE),
                    SimpleCondition(fact_name="symptom.neck_stiffness", operator=Operator.NOT_EQUALS, target_value=FactValue.TRUE)
                ]
            ),
            conclusions=[
                Conclusion(
                    id="CONC_TRIAGE_HEADACHE_GENERAL",
                    fact_name="observation.triage.general_cephalea_pattern",
                    asserted_value=FactValue.TRUE,
                    confidence=0.85,
                    category="OBSERVATION",
                    summary="Primary Cephalea Pattern (Outpatient Evaluation Recommended)",
                    detailed_explanation="Reported head discomfort without acute thunderclap onset or meningeal signs. Follow up with your physician if pain persists or recurs.",
                    recommendation_tier=RecommendationTier.CONSULT_PHYSICIAN,
                    actionable_steps=[
                        "Keep an accurate symptom log detailing triggers, sleep patterns, and caffeine intake.",
                        "Ensure regular hydration and screen breaks every 20 minutes.",
                        "Seek urgent care if pain intensity suddenly escalates to an unbearable level."
                    ]
                )
            ]
        ),

        Rule(
            id="RULE_VIRAL_URI_021",
            name="Clinical Triage: Viral Upper Respiratory Tract Infection",
            description="Rhinorrhea, pharyngeal discomfort, sneezing, and low-grade constitutional symptoms without severe dyspnea.",
            priority=500,
            category=RuleCategory.CLINICAL_TRIAGE,
            version=KB_VERSION,
            provenance="CDC Clinical Guidance for Common Cold and Viral Pharyngitis",
            conditions=CompoundCondition(
                logical_operator="AND",
                conditions=[
                    CompoundCondition(
                        logical_operator="OR",
                        conditions=[
                            SimpleCondition(fact_name="symptom.sore_throat", operator=Operator.EQUALS, target_value=FactValue.TRUE),
                            SimpleCondition(fact_name="symptom.rhinorrhea", operator=Operator.EQUALS, target_value=FactValue.TRUE),
                            SimpleCondition(fact_name="symptom.nasal_congestion", operator=Operator.EQUALS, target_value=FactValue.TRUE)
                        ]
                    ),
                    SimpleCondition(fact_name="symptom.dyspnea", operator=Operator.NOT_EQUALS, target_value=FactValue.TRUE)
                ]
            ),
            conclusions=[
                Conclusion(
                    id="CONC_TRIAGE_URI",
                    fact_name="observation.triage.viral_uri_pattern",
                    asserted_value=FactValue.TRUE,
                    confidence=0.90,
                    category="OBSERVATION",
                    summary="Acute Viral Rhinopharyngitis (Upper Respiratory Infection)",
                    detailed_explanation="Symptom profile indicates a self-limiting viral infection of the upper airways. Antibiotic therapy is ineffective against viral pathogens.",
                    recommendation_tier=RecommendationTier.SELF_MONITOR,
                    actionable_steps=[
                        "Ensure generous hydration (warm teas, clear broths, water).",
                        "Use warm saline gargles for pharyngeal comfort.",
                        "Consult a physician if symptoms persist beyond 10 days or if high fever (>38.5°C) develops."
                    ]
                )
            ]
        ),

        Rule(
            id="RULE_ACUTE_BRONCHITIS_025",
            name="Clinical Triage: Acute Bronchial Cough Pattern",
            description="Cough presenting without severe dyspnea, wheezing, or hemoptysis.",
            priority=480,
            category=RuleCategory.CLINICAL_TRIAGE,
            version=KB_VERSION,
            provenance="American College of Chest Physicians (CHEST) Cough Guidelines",
            conditions=CompoundCondition(
                logical_operator="AND",
                conditions=[
                    SimpleCondition(fact_name="symptom.cough", operator=Operator.EQUALS, target_value=FactValue.TRUE),
                    SimpleCondition(fact_name="symptom.dyspnea", operator=Operator.NOT_EQUALS, target_value=FactValue.TRUE),
                    SimpleCondition(fact_name="symptom.wheezing", operator=Operator.NOT_EQUALS, target_value=FactValue.TRUE)
                ]
            ),
            conclusions=[
                Conclusion(
                    id="CONC_TRIAGE_BRONCHIAL_COUGH",
                    fact_name="observation.triage.bronchial_cough_pattern",
                    asserted_value=FactValue.TRUE,
                    confidence=0.88,
                    category="OBSERVATION",
                    summary="Acute Bronchial Irritation / Tracheobronchial Cough Syndrome",
                    detailed_explanation="Cough presentation without shortness of breath or airway wheezing is characteristic of self-limiting tracheobronchial inflammation.",
                    recommendation_tier=RecommendationTier.SELF_MONITOR,
                    actionable_steps=[
                        "Utilize warm steam inhalation and honey/lemon soothing preparations.",
                        "Avoid exposure to aerosol irritants, dust, and cigarette smoke.",
                        "Consult a physician if cough persists for more than 3 weeks or produces rust-colored sputum."
                    ]
                )
            ]
        ),

        Rule(
            id="RULE_ASTHMA_EXACERBATION_033",
            name="Clinical Triage: Bronchospastic Airway Constriction",
            description="Wheezing, episodic dyspnea, and dry cough with personal history of asthma or reactive airway disease.",
            priority=600,
            category=RuleCategory.CLINICAL_TRIAGE,
            version=KB_VERSION,
            provenance="Global Initiative for Asthma (GINA) Management Strategy",
            conditions=CompoundCondition(
                logical_operator="AND",
                conditions=[
                    SimpleCondition(fact_name="symptom.wheezing", operator=Operator.EQUALS, target_value=FactValue.TRUE),
                    SimpleCondition(fact_name="symptom.dyspnea", operator=Operator.EQUALS, target_value=FactValue.TRUE)
                ]
            ),
            conclusions=[
                Conclusion(
                    id="CONC_TRIAGE_ASTHMA",
                    fact_name="observation.triage.bronchospasm_pattern",
                    asserted_value=FactValue.TRUE,
                    confidence=0.91,
                    category="OBSERVATION",
                    summary="Active Bronchospastic Pattern (Wheezing & Airway Restriction)",
                    detailed_explanation="Audible expiratory wheezing coupled with dyspnea suggests lower airway narrowing requiring structured bronchodilator evaluation.",
                    recommendation_tier=RecommendationTier.URGENT_EVALUATION,
                    actionable_steps=[
                        "If prescribed a rescue inhaler (e.g. Albuterol), utilize it per your physician's Asthma Action Plan.",
                        "Sit upright and avoid triggers such as tobacco smoke, cold air, or dust.",
                        "Seek emergency care if speaking full sentences becomes difficult."
                    ]
                )
            ]
        ),

        Rule(
            id="RULE_GASTROENTERITIS_031",
            name="Clinical Triage: Acute Enteric Irritation / Gastroenteritis",
            description="Abdominal cramping or pain accompanied by nausea, vomiting, or diarrhea.",
            priority=500,
            category=RuleCategory.CLINICAL_TRIAGE,
            version=KB_VERSION,
            provenance="American College of Gastroenterology (ACG) Acute Diarrheal Infections Guidelines",
            conditions=CompoundCondition(
                logical_operator="AND",
                conditions=[
                    SimpleCondition(fact_name="symptom.abdominal_pain", operator=Operator.EQUALS, target_value=FactValue.TRUE),
                    CompoundCondition(
                        logical_operator="OR",
                        conditions=[
                            SimpleCondition(fact_name="symptom.nausea", operator=Operator.EQUALS, target_value=FactValue.TRUE),
                            SimpleCondition(fact_name="symptom.diarrhea", operator=Operator.EQUALS, target_value=FactValue.TRUE)
                        ]
                    ),
                    SimpleCondition(fact_name="symptom.abdominal.rlq_localization", operator=Operator.NOT_EQUALS, target_value=FactValue.TRUE)
                ]
            ),
            conclusions=[
                Conclusion(
                    id="CONC_TRIAGE_GASTROENTERITIS",
                    fact_name="observation.triage.gastroenteritis_pattern",
                    asserted_value=FactValue.TRUE,
                    confidence=0.90,
                    category="OBSERVATION",
                    summary="Acute Enteric Irritation / Viral Gastroenteritis Syndrome",
                    detailed_explanation="Abdominal discomfort coupled with nausea or loose stools in the absence of localized RLQ peritoneal signs is consistent with acute gastroenteritis.",
                    recommendation_tier=RecommendationTier.SELF_MONITOR,
                    actionable_steps=[
                        "Prioritize small, frequent sips of oral rehydration solution (ORS) or electrolyte broths.",
                        "Follow a bland BRAT diet (bananas, rice, applesauce, toast) as tolerated.",
                        "Seek clinical attention if unable to keep fluids down for 24 hours or if high fever occurs."
                    ]
                )
            ]
        ),

        Rule(
            id="RULE_DYSPEPSIA_GERD_035",
            name="Clinical Triage: Acid Peptic Reflux / Dyspepsia",
            description="Retrosternal or epigastric burning discomfort exacerbated by recumbency or meals.",
            priority=480,
            category=RuleCategory.CLINICAL_TRIAGE,
            version=KB_VERSION,
            provenance="ACG Guidelines for the Diagnosis and Management of GERD",
            conditions=CompoundCondition(
                logical_operator="AND",
                conditions=[
                    SimpleCondition(fact_name="symptom.heartburn", operator=Operator.EQUALS, target_value=FactValue.TRUE),
                    SimpleCondition(fact_name="symptom.chest_pain.crushing", operator=Operator.NOT_EQUALS, target_value=FactValue.TRUE)
                ]
            ),
            conclusions=[
                Conclusion(
                    id="CONC_TRIAGE_GERD",
                    fact_name="observation.triage.gerd_pattern",
                    asserted_value=FactValue.TRUE,
                    confidence=0.89,
                    category="OBSERVATION",
                    summary="Gastroesophageal Reflux / Acid Peptic Discomfort Pattern",
                    detailed_explanation="Retrosternal pyrosis without acute coronary warning signs indicates gastric acid reflux or functional dyspepsia.",
                    recommendation_tier=RecommendationTier.SELF_MONITOR,
                    actionable_steps=[
                        "Avoid lying flat within 3 hours after meals; elevate the head of the bed 6 inches.",
                        "Limit dietary triggers (caffeine, acidic citrus, tomato sauces, and peppermint).",
                        "Consult your physician if symptoms require antacids more than twice weekly."
                    ]
                )
            ]
        ),

        Rule(
            id="RULE_ACUTE_FEBRILE_040",
            name="Clinical Triage: Acute Systemic Febrile Response",
            description="Elevated temperature accompanied by constitutional fatigue or generalized malaise.",
            priority=470,
            category=RuleCategory.CLINICAL_TRIAGE,
            version=KB_VERSION,
            provenance="WHO Clinical Guidance on Fever and Systemic Infections",
            conditions=CompoundCondition(
                logical_operator="AND",
                conditions=[
                    SimpleCondition(fact_name="symptom.fever", operator=Operator.EQUALS, target_value=FactValue.TRUE),
                    CompoundCondition(
                        logical_operator="OR",
                        conditions=[
                            SimpleCondition(fact_name="symptom.fatigue", operator=Operator.EQUALS, target_value=FactValue.TRUE),
                            SimpleCondition(fact_name="symptom.mild_fatigue", operator=Operator.EQUALS, target_value=FactValue.TRUE)
                        ]
                    ),
                    SimpleCondition(fact_name="symptom.neck_stiffness", operator=Operator.NOT_EQUALS, target_value=FactValue.TRUE)
                ]
            ),
            conclusions=[
                Conclusion(
                    id="CONC_TRIAGE_FEBRILE_SYSTEMIC",
                    fact_name="observation.triage.acute_febrile_pattern",
                    asserted_value=FactValue.TRUE,
                    confidence=0.88,
                    category="OBSERVATION",
                    summary="Acute Systemic Febrile Syndrome (Constitutional Infection Response)",
                    detailed_explanation="Elevated core temperature with generalized fatigue represents a host immune response to an acute, likely viral or bacterial, antigenic trigger.",
                    recommendation_tier=RecommendationTier.CONSULT_PHYSICIAN,
                    actionable_steps=[
                        "Monitor body temperature every 6 to 8 hours using a calibrated oral thermometer.",
                        "Stay generously hydrated with water, herbal teas, and electrolyte-rich broths.",
                        "Consult a healthcare professional if fever persists beyond 72 hours."
                    ]
                )
            ]
        ),

        Rule(
            id="RULE_MUSCULOSKELETAL_BACK_045",
            name="Clinical Triage: Mechanical Lumbar Strain",
            description="Non-radiating axial back discomfort without systemic fever or neurological deficits.",
            priority=480,
            category=RuleCategory.CLINICAL_TRIAGE,
            version=KB_VERSION,
            provenance="American College of Physicians (ACP) Non-Invasive Low Back Pain Guidelines",
            conditions=CompoundCondition(
                logical_operator="AND",
                conditions=[
                    SimpleCondition(fact_name="symptom.back_pain", operator=Operator.EQUALS, target_value=FactValue.TRUE),
                    SimpleCondition(fact_name="symptom.fever", operator=Operator.NOT_EQUALS, target_value=FactValue.TRUE)
                ]
            ),
            conclusions=[
                Conclusion(
                    id="CONC_TRIAGE_LUMBAR_STRAIN",
                    fact_name="observation.triage.lumbar_strain_pattern",
                    asserted_value=FactValue.TRUE,
                    confidence=0.89,
                    category="OBSERVATION",
                    summary="Mechanical Musculoskeletal Strain (Axial Back Pain)",
                    detailed_explanation="Localized muscular back discomfort in the absence of fever, spinal tenderness, or radicular neurological signs is typical of mechanical lumbar strain.",
                    recommendation_tier=RecommendationTier.SELF_MONITOR,
                    actionable_steps=[
                        "Maintain light activity as tolerated; avoid prolonged strict bed rest.",
                        "Apply local heat or cold packs for 15-20 minutes at a time.",
                        "Consult a spine specialist or physical therapist if pain radiates below the knee."
                    ]
                )
            ]
        ),

        Rule(
            id="RULE_FATIGUE_MALAISE_001",
            name="Clinical Triage: Constitutional Fatigue & Malaise Pattern",
            description="Persistent fatigue or body weakness without acute organ-specific red flags.",
            priority=400,
            category=RuleCategory.CLINICAL_TRIAGE,
            version=KB_VERSION,
            provenance="CDC Chronic Fatigue and Post-Viral Convalescence Guidelines",
            conditions=CompoundCondition(
                logical_operator="AND",
                conditions=[
                    SimpleCondition(fact_name="symptom.fatigue", operator=Operator.EQUALS, target_value=FactValue.TRUE),
                    SimpleCondition(fact_name="symptom.dyspnea", operator=Operator.NOT_EQUALS, target_value=FactValue.TRUE)
                ]
            ),
            conclusions=[
                Conclusion(
                    id="CONC_TRIAGE_FATIGUE",
                    fact_name="observation.triage.fatigue_pattern",
                    asserted_value=FactValue.TRUE,
                    confidence=0.85,
                    category="OBSERVATION",
                    summary="Constitutional Fatigue & Energy Depletion Pattern",
                    detailed_explanation="Subjective exhaustion or weakness without respiratory distress suggests physiological recuperation, sleep deficit, or post-viral convalescence.",
                    recommendation_tier=RecommendationTier.SELF_MONITOR,
                    actionable_steps=[
                        "Ensure 7 to 9 hours of quality sleep on a regular schedule.",
                        "Review recent dietary intake, hydration, and workplace physical exertion.",
                        "Consult your physician for routine metabolic panel testing if fatigue lasts longer than 2 weeks."
                    ]
                )
            ]
        ),

        # =====================================================================
        # 3. SELF CARE & PREVENTIVE GUIDANCE (Priority 100)
        # =====================================================================
        Rule(
            id="RULE_SELFCARE_HYDRATION_001",
            name="Self-Care Advisory: Electrolyte Balance & Fluid Support",
            description="When mild constitutional fatigue or headaches are present without severe dehydration signs.",
            priority=100,
            category=RuleCategory.SELF_CARE_GUIDANCE,
            version=KB_VERSION,
            provenance="WHO Guidelines on Oral Rehydration and Wellness",
            conditions=CompoundCondition(
                logical_operator="AND",
                conditions=[
                    CompoundCondition(
                        logical_operator="OR",
                        conditions=[
                            SimpleCondition(fact_name="symptom.mild_fatigue", operator=Operator.EQUALS, target_value=FactValue.TRUE),
                            SimpleCondition(fact_name="symptom.fatigue", operator=Operator.EQUALS, target_value=FactValue.TRUE),
                            SimpleCondition(fact_name="symptom.headache.present", operator=Operator.EQUALS, target_value=FactValue.TRUE)
                        ]
                    ),
                    SimpleCondition(fact_name="symptom.dyspnea", operator=Operator.NOT_EQUALS, target_value=FactValue.TRUE)
                ]
            ),
            conclusions=[
                Conclusion(
                    id="CONC_SELFCARE_HYDRATION",
                    fact_name="observation.advisory.hydration_wellness",
                    asserted_value=FactValue.TRUE,
                    confidence=0.85,
                    category="ADVISORY",
                    summary="General Wellness: Rest and Oral Rehydration Guidance",
                    detailed_explanation="Supportive physical recovery through balanced fluid intake and restorative sleep.",
                    recommendation_tier=RecommendationTier.ROUTINE_PREVENTIVE,
                    actionable_steps=[
                        "Target 2 to 2.5 liters of clean fluid intake throughout the day.",
                        "Prioritize 7-8 hours of uninterrupted rest."
                    ]
                )
            ]
        )
    ]
