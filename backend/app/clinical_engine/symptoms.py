from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class AnatomicalLocation(BaseModel):
    id: str
    name: str
    system: str  # HEAD, ABDOMEN, CHEST, SPINE, EXTREMITIES, GENERAL
    description: str

class SymptomDefinition(BaseModel):
    id: str
    name: str
    system: str  # NEUROLOGICAL, RESPIRATORY, DIGESTIVE, MUSCULOSKELETAL, GENERAL
    description: str
    synonyms: List[str]
    allowed_locations: List[str]
    primary_fact_name: Optional[str] = None
    severity_options: List[str] = ["Mild", "Moderate", "Severe"]
    duration_options: List[str] = ["< 24 Hours", "1-3 Days", "4-7 Days", "1-3 Weeks", "> 1 Month"]
    character_options: List[str] = Field(default_factory=list)
    common_triggers: List[str] = Field(default_factory=list)
    is_emergency_candidate: bool = False

# Anatomical Locations Registry
ANATOMICAL_LOCATIONS: List[AnatomicalLocation] = [
    # Head & Neck
    AnatomicalLocation(id="loc_forehead", name="Forehead", system="HEAD", description="Frontal cranial region"),
    AnatomicalLocation(id="loc_temple_left", name="Left Temple", system="HEAD", description="Left temporal region"),
    AnatomicalLocation(id="loc_temple_right", name="Right Temple", system="HEAD", description="Right temporal region"),
    AnatomicalLocation(id="loc_temple_bilateral", name="Both Temples", system="HEAD", description="Bilateral temporal band"),
    AnatomicalLocation(id="loc_head_back", name="Back of Head (Occiput)", system="HEAD", description="Occipital and suboccipital area"),
    AnatomicalLocation(id="loc_head_top", name="Top of Head (Vertex)", system="HEAD", description="Vertex cranial surface"),
    AnatomicalLocation(id="loc_eyes", name="Around the Eyes (Periorbital)", system="HEAD", description="Orbital and retro-orbital region"),
    AnatomicalLocation(id="loc_neck", name="Neck / Cervical Spine", system="HEAD", description="Posterior cervical region"),
    AnatomicalLocation(id="loc_head_entire", name="Entire Head (Generalized)", system="HEAD", description="Diffuse global cephalea"),

    # Chest & Respiratory
    AnatomicalLocation(id="loc_chest_center", name="Center of Chest (Retrosternal)", system="CHEST", description="Substernal midline"),
    AnatomicalLocation(id="loc_chest_left", name="Left Chest", system="CHEST", description="Left precordial region"),
    AnatomicalLocation(id="loc_chest_right", name="Right Chest", system="CHEST", description="Right hemithorax"),

    # Abdomen
    AnatomicalLocation(id="loc_abd_ruq", name="Upper Right Abdomen", system="ABDOMEN", description="Right hypochondrium (liver/gallbladder)"),
    AnatomicalLocation(id="loc_abd_luq", name="Upper Left Abdomen", system="ABDOMEN", description="Left hypochondrium (stomach/spleen)"),
    AnatomicalLocation(id="loc_abd_epigastric", name="Upper Central (Epigastric)", system="ABDOMEN", description="Epigastrium above umbilicus"),
    AnatomicalLocation(id="loc_abd_rlq", name="Lower Right Abdomen", system="ABDOMEN", description="Right iliac fossa (appendix region)"),
    AnatomicalLocation(id="loc_abd_llq", name="Lower Left Abdomen", system="ABDOMEN", description="Left iliac fossa (sigmoid colon)"),
    AnatomicalLocation(id="loc_abd_periumbilical", name="Around Navel (Periumbilical)", system="ABDOMEN", description="Umbilical region"),
    AnatomicalLocation(id="loc_abd_diffuse", name="Entire Abdomen (Diffuse)", system="ABDOMEN", description="Generalized abdominal cramp"),

    # Musculoskeletal
    AnatomicalLocation(id="loc_back_lower", name="Lower Back (Lumbar)", system="SPINE", description="Lumbar and sacral spinal zone"),
    AnatomicalLocation(id="loc_back_upper", name="Upper Back (Thoracic)", system="SPINE", description="Interscapular and thoracic spine"),
    AnatomicalLocation(id="loc_joints_knees", name="Knees", system="EXTREMITIES", description="Bilateral or unilateral knee joints"),
    AnatomicalLocation(id="loc_joints_shoulders", name="Shoulders", system="EXTREMITIES", description="Glenohumeral and acromioclavicular joints")
]

# Supported Symptom Catalogue
SYMPTOM_CATALOGUE: List[SymptomDefinition] = [
    # Head & Neurological
    SymptomDefinition(
        id="sym_headache",
        name="Headache",
        system="NEUROLOGICAL",
        description="Pain or discomfort localized to the cranial or facial region.",
        synonyms=["head pain", "migraine", "cephalea", "pounding head", "throbbing head", "temple pain"],
        allowed_locations=["loc_forehead", "loc_temple_left", "loc_temple_right", "loc_temple_bilateral", "loc_head_back", "loc_head_top", "loc_eyes", "loc_neck", "loc_head_entire"],
        primary_fact_name="symptom.headache.present",
        character_options=["Pulsating / Throbbing", "Pressing / Tight Band", "Sharp / Stabbing", "Dull / Aching", "Explosive / Thunderclap"],
        common_triggers=["Stress", "Bright Screens / Light", "Lack of Sleep", "Physical Exertion", "Dehydration", "Bending Forward"],
        is_emergency_candidate=True
    ),
    SymptomDefinition(
        id="sym_dizziness",
        name="Dizziness or Vertigo",
        system="NEUROLOGICAL",
        description="Sensation of spinning, unsteadiness, or lightheadedness.",
        synonyms=["lightheaded", "spinning sensation", "vertigo", "woozy", "off balance", "faint feeling"],
        allowed_locations=["loc_head_entire"],
        primary_fact_name="symptom.dizziness",
        character_options=["Room Spinning (Vertigo)", "Lightheadedness", "Disequilibrium / Imbalance"],
        common_triggers=["Sudden Standing", "Head Movement", "Prolonged Fasting", "Dehydration"]
    ),
    SymptomDefinition(
        id="sym_nausea",
        name="Nausea",
        system="NEUROLOGICAL",
        description="Inclination to vomit or stomach queasiness.",
        synonyms=["feeling sick", "queasy", "upset stomach", "urge to vomit"],
        allowed_locations=["loc_abd_epigastric", "loc_abd_diffuse"],
        primary_fact_name="symptom.nausea",
        character_options=["Intermittent", "Constant", "Motion-related"]
    ),
    SymptomDefinition(
        id="sym_photophobia",
        name="Sensitivity to Light (Photophobia)",
        system="NEUROLOGICAL",
        description="Abnormal discomfort or eye pain in illuminated environments.",
        synonyms=["light hurts eyes", "glare sensitivity", "cannot look at screens"],
        allowed_locations=["loc_eyes", "loc_forehead"],
        primary_fact_name="symptom.photophobia"
    ),

    # Respiratory
    SymptomDefinition(
        id="sym_cough",
        name="Cough",
        system="RESPIRATORY",
        description="Reflex action to clear airways of irritants or secretions.",
        synonyms=["coughing", "hacking", "dry cough", "chesty cough", "phlegm"],
        allowed_locations=["loc_chest_center"],
        primary_fact_name="symptom.cough",
        character_options=["Dry / Irritating", "Productive / Phlegm", "Barking", "Paroxysmal / Spasmodic"],
        common_triggers=["Cold Air", "Lying Flat", "Dust / Pollen", "Exertion"]
    ),
    SymptomDefinition(
        id="sym_dyspnea",
        name="Shortness of Breath (Dyspnea)",
        system="RESPIRATORY",
        description="Subjective sensation of uncomfortable or labored breathing.",
        synonyms=["difficulty breathing", "breathless", "tight chest", "air hunger", "wheezing"],
        allowed_locations=["loc_chest_center"],
        primary_fact_name="symptom.dyspnea",
        character_options=["Sudden Onset", "Gradual on Exertion", "Worse when Lying Down (Orthopnea)"],
        common_triggers=["Physical Activity", "Allergens", "Cold Temperatures"],
        is_emergency_candidate=True
    ),
    SymptomDefinition(
        id="sym_sore_throat",
        name="Sore Throat",
        system="RESPIRATORY",
        description="Pain, scratchiness, or irritation of the pharynx that worsens on swallowing.",
        synonyms=["throat pain", "scratchy throat", "pharyngitis", "painful swallowing"],
        allowed_locations=["loc_neck"],
        primary_fact_name="symptom.sore_throat",
        character_options=["Scratchy", "Sharp on Swallowing", "Raw / Burning"]
    ),
    SymptomDefinition(
        id="sym_rhinorrhea",
        name="Runny or Congested Nose",
        system="RESPIRATORY",
        description="Nasal discharge or obstruction of nasal passages.",
        synonyms=["stuffy nose", "nasal congestion", "rhinorrhea", "sneezing", "blocked nose"],
        allowed_locations=["loc_forehead"],
        primary_fact_name="symptom.rhinorrhea"
    ),

    # Digestive & Abdominal
    SymptomDefinition(
        id="sym_abdominal_pain",
        name="Abdominal Pain",
        system="DIGESTIVE",
        description="Cramping, aching, or sharp discomfort in the stomach or lower belly.",
        synonyms=["stomach ache", "belly pain", "tummy ache", "gut cramps", "abdominal cramps"],
        allowed_locations=["loc_abd_ruq", "loc_abd_luq", "loc_abd_epigastric", "loc_abd_rlq", "loc_abd_llq", "loc_abd_periumbilical", "loc_abd_diffuse"],
        primary_fact_name="symptom.abdominal_pain",
        character_options=["Sharp / Localized", "Dull / Aching", "Colicky / Cramping", "Burning"],
        common_triggers=["Eating Fatty Food", "Movement", "Empty Stomach"],
        is_emergency_candidate=True
    ),
    SymptomDefinition(
        id="sym_diarrhea",
        name="Diarrhea",
        system="DIGESTIVE",
        description="Frequent, loose, or watery bowel movements.",
        synonyms=["loose stools", "watery motions", "upset bowels", "stomach bug"],
        allowed_locations=["loc_abd_diffuse"],
        primary_fact_name="symptom.diarrhea",
        character_options=["Watery", "Mucous", "Bloody (Red Flag)"],
        is_emergency_candidate=True
    ),
    SymptomDefinition(
        id="sym_heartburn",
        name="Heartburn / Acid Reflux",
        system="DIGESTIVE",
        description="Burning sensation in the chest or upper stomach rising toward throat.",
        synonyms=["acid reflux", "indigestion", "GERD", "burning chest after eating"],
        allowed_locations=["loc_chest_center", "loc_abd_epigastric"],
        primary_fact_name="symptom.heartburn",
        character_options=["Burning", "Sour Regurgitation", "Worse when bending or reclining"],
        common_triggers=["Spicy Meals", "Coffee / Alcohol", "Lying Down Post-Meal"]
    ),

    # Musculoskeletal
    SymptomDefinition(
        id="sym_back_pain",
        name="Back Pain",
        system="MUSCULOSKELETAL",
        description="Pain, muscle tension, or stiffness along spinal columns.",
        synonyms=["lower back ache", "lumbago", "sciatica", "stiff back"],
        allowed_locations=["loc_back_lower", "loc_back_upper"],
        primary_fact_name="symptom.back_pain",
        character_options=["Dull Muscular Ache", "Sharp / Shooting down leg", "Stiff upon waking"],
        common_triggers=["Heavy Lifting", "Prolonged Sitting", "Bending Forward"]
    ),
    SymptomDefinition(
        id="sym_neck_stiffness",
        name="Neck Stiffness",
        system="MUSCULOSKELETAL",
        description="Pain and limited mobility in the neck, especially when flexing forward.",
        synonyms=["stiff neck", "nuchal rigidity", "cannot bend neck"],
        allowed_locations=["loc_neck"],
        primary_fact_name="symptom.neck_stiffness",
        character_options=["Severe Rigid Resistance (Red Flag)", "Mild Muscular Strain"],
        is_emergency_candidate=True
    ),

    # General & Constitutional
    SymptomDefinition(
        id="sym_fever",
        name="Fever",
        system="GENERAL",
        description="Elevation in body temperature above standard baseline (38.0°C / 100.4°F).",
        synonyms=["high temp", "pyrexia", "feverish", "shivering", "chills and sweats"],
        allowed_locations=["loc_head_entire"],
        primary_fact_name="symptom.fever",
        character_options=["Low-grade (37.5-38.3°C)", "High-grade (>38.5°C)", "Intermittent Spikes"]
    ),
    SymptomDefinition(
        id="sym_fatigue",
        name="Fatigue & Body Weakness",
        system="GENERAL",
        description="Persistent feeling of tiredness, low vitality, or generalized exhaustion.",
        synonyms=["exhaustion", "lethargy", "tiredness", "body weakness", "fatigued"],
        allowed_locations=["loc_head_entire"],
        primary_fact_name="symptom.mild_fatigue",
        character_options=["Mild Tiredness", "Severe Debilitating Exhaustion"]
    ),
    SymptomDefinition(
        id="sym_chest_pain",
        name="Chest Pain",
        system="GENERAL",
        description="Discomfort, heaviness, or sharp ache in the thoracic cavity.",
        synonyms=["chest pressure", "tight chest", "crushing chest pain", "heart pain"],
        allowed_locations=["loc_chest_center", "loc_chest_left", "loc_chest_right"],
        primary_fact_name="symptom.chest_pain",
        character_options=["Crushing / Pressure", "Sharp / Stabbing on inhale", "Dull Ache"],
        common_triggers=["Physical Exertion", "Emotional Stress", "Deep Breath"],
        is_emergency_candidate=True
    )
]

def find_symptom_by_text(query: str) -> List[SymptomDefinition]:
    """Finds symptom definitions matching text query by id, name, or synonyms."""
    q = query.lower().strip()
    matches = []
    for s in SYMPTOM_CATALOGUE:
        if q in s.id.lower() or q in s.name.lower():
            matches.append(s)
            continue
        if any(q in syn.lower() or syn.lower() in q for syn in s.synonyms):
            matches.append(s)
    return matches

def get_symptom_by_id(sym_id: str) -> Optional[SymptomDefinition]:
    for s in SYMPTOM_CATALOGUE:
        if s.id == sym_id:
            return s
    return None
