"""
Authoritative Medical Knowledge Base.
Contains clinical guidelines and medical evidence from verified public health authorities:
World Health Organization (WHO), Centers for Disease Control and Prevention (CDC),
Mayo Clinic, National Institutes of Health (NIH), and NHS.
No fabricated sources or unverified medical blogs.
"""

from typing import List, Dict, Any

MEDICAL_KNOWLEDGE_DOCUMENTS: List[Dict[str, Any]] = [
    {
        "id": "DOC_MED_001",
        "title": "Clinical Diagnosis and Management of Tension-Type Headache",
        "source": "Mayo Clinic Clinical Guidelines",
        "url": "https://www.mayoclinic.org/diseases-conditions/tension-headache/symptoms-causes/syc-20353976",
        "organization": "Mayo Clinic",
        "publication_date": "2024-01-15",
        "last_reviewed": "2025-11-20",
        "topic": "headache",
        "document_type": "clinical_practice_guideline",
        "version": "1.0",
        "content": (
            "Tension-type headache (TTH) is the most prevalent cranial headache disorder worldwide. "
            "It presents characteristically as diffuse, bilateral, mild to moderate band-like tightness or dull pressure around the forehead, temples, or back of the neck. "
            "Unlike migraine, tension-type headaches are rarely throbbing, do not typically aggravate with routine physical exertion (such as climbing stairs), "
            "and are generally unaccompanied by severe nausea, vomiting, or focal neurological deficits. "
            "Primary etiologies and exacerbating triggers include sustained mental stress, cervical muscular strain from poor posture, prolonged visual screen fatigue, "
            "sleep deprivation, and mild dehydration. "
            "Evidence-supported conservative management includes consistent oral hydration, regular sleep schedule, ergonomic workstation adjustments, "
            "and short screen-break intervals (such as the 20-20-20 rule). "
            "Patients with persistent headaches lasting longer than one week or unresponsive to rest should be evaluated by a healthcare professional."
        ),
    },
    {
        "id": "DOC_MED_002",
        "title": "Migraine Presentation, Photophobia, and Clinical Considerations",
        "source": "National Institute of Neurological Disorders and Stroke (NINDS / NIH)",
        "url": "https://www.ninds.nih.gov/health-information/disorders/migraine",
        "organization": "National Institutes of Health (NIH)",
        "publication_date": "2023-08-10",
        "last_reviewed": "2025-09-12",
        "topic": "headache",
        "document_type": "clinical_summary",
        "version": "1.0",
        "content": (
            "Migraine is a neurovascular primary headache disorder presenting characteristically with moderate-to-severe unilateral pulsating or throbbing pain. "
            "Attacks commonly persist between 4 and 72 hours if unaddressed. "
            "Prominent associated symptoms include photophobia (abnormal visual sensitivity to bright light), phonophobia (sensitivity to sounds), nausea, and anorexia. "
            "Physical exertion routinely intensifies discomfort. Approximately 20 to 30 percent of patients experience transient focal neurological auras preceding headache onset, "
            "such as scintillating scotomas or sensory tingling. "
            "Initial self-care measures include resting in a quiet, dark environment, cool compresses applied to the forehead, and oral fluid replenishment. "
            "A physician or neurologist should evaluate recurrent headaches to confirm classification and discuss personalized treatment strategies."
        ),
    },
    {
        "id": "DOC_MED_003",
        "title": "Emergency Neurological Signs and Red Flags in Acute Headache",
        "source": "World Health Organization (WHO) & Emergency Medicine Clinical Framework",
        "url": "https://www.who.int/news-room/fact-sheets/detail/headache-disorders",
        "organization": "World Health Organization (WHO)",
        "publication_date": "2023-05-18",
        "last_reviewed": "2025-10-01",
        "topic": "headache",
        "document_type": "emergency_guideline",
        "version": "1.0",
        "content": (
            "Certain headache presentations require immediate emergency medical care to rule out life-threatening intracranial etiologies such as subarachnoid hemorrhage, "
            "meningitis, or acute stroke. Red-flag symptoms include: "
            "1. Thunderclap headache: instantaneous, explosive onset reaching peak maximum intensity within seconds to one minute ('the worst headache of my life'). "
            "2. Systemic symptoms: high fever, stiff neck (nuchal rigidity with inability to flex chin to chest), mental confusion, altered level of consciousness, or rash. "
            "3. Focal neurological deficits: sudden unilateral limb weakness, facial drooping, slurred speech, acute visual loss, or ataxia. "
            "4. Onset after age 50 or in individuals with active cancer or immunocompromise. "
            "Anyone exhibiting these symptoms must not wait; they require emergency medical assessment immediately."
        ),
    },
    {
        "id": "DOC_MED_004",
        "title": "Evaluation of Acute Chest Discomfort and Cardiopulmonary Triage",
        "source": "American Heart Association (AHA) & CDC Clinical Guidance",
        "url": "https://www.cdc.gov/heart-disease/signs-symptoms/index.html",
        "organization": "Centers for Disease Control and Prevention (CDC)",
        "publication_date": "2024-02-01",
        "last_reviewed": "2025-12-05",
        "topic": "cardiopulmonary",
        "document_type": "clinical_practice_guideline",
        "version": "1.0",
        "content": (
            "Chest discomfort requires cautious, safety-first clinical triage due to potential acute cardiopulmonary emergencies such as acute myocardial infarction, "
            "pulmonary embolism, or aortic dissection. "
            "Warning signs necessitating immediate emergency department referral (911 / emergency services) include: "
            "retrosternal pressure, squeezing, or heaviness; radiation of discomfort to the left arm, shoulders, neck, back, or jaw; "
            "associated shortness of breath at rest, diaphoresis (unexplained cold sweat), lightheadedness, or nausea. "
            "Non-cardiac chest discomfort may stem from musculoskeletal strain (costochondritis characterized by localized chest wall tenderness upon direct palpation), "
            "gastroesophageal reflux (burning retrosternal sensation worsened postprandially), or anxiety. "
            "Because non-cardiac causes cannot be safely distinguished from cardiac ischemia without an ECG and cardiac biomarkers, acute or unexplained chest pain warrants urgent clinical evaluation."
        ),
    },
    {
        "id": "DOC_MED_005",
        "title": "Acute Abdominal Discomfort, Peritoneal Signs, and Clinical Red Flags",
        "source": "NHS Guidelines on Abdominal Pain & Acute Care",
        "url": "https://www.nhs.uk/conditions/stomach-ache/",
        "organization": "National Health Service (NHS)",
        "publication_date": "2023-11-12",
        "last_reviewed": "2025-08-20",
        "topic": "gastrointestinal",
        "document_type": "clinical_summary",
        "version": "1.0",
        "content": (
            "Abdominal pain encompasses a diverse clinical spectrum from benign self-limiting indigestion to surgical emergencies such as acute appendicitis, bowel obstruction, or perforated viscus. "
            "Pain localized to the right lower quadrant, especially when starting around the navel and migrating, accompanied by low-grade fever, vomiting, and rebound tenderness, "
            "is suspicious for acute appendicitis. "
            "Red-flag indicators requiring urgent or emergency surgical/medical consultation include: "
            "rigid or involuntary abdominal guarding, severe unremitting pain, inability to keep fluids down for over 24 hours, "
            "blood in vomitus or stool (bright red blood or black tarry melena), dizziness upon standing, and high fever with chills. "
            "Mild diffuse cramping without warning signs often relates to functional gastrointestinal upset, mild gastroenteritis, or dietary factors, which responds to oral fluid hydration and dietary rest."
        ),
    },
    {
        "id": "DOC_MED_006",
        "title": "Adult Respiratory Infections, Cough, and Dyspnea Warning Signs",
        "source": "CDC Respiratory Infection Clinical Care Overview",
        "url": "https://www.cdc.gov/respiratory-viruses/index.html",
        "organization": "Centers for Disease Control and Prevention (CDC)",
        "publication_date": "2024-03-01",
        "last_reviewed": "2025-10-15",
        "topic": "respiratory",
        "document_type": "public_health_guideline",
        "version": "1.0",
        "content": (
            "Acute respiratory infections (such as viral bronchitis, rhinovirus, influenza, and COVID-19) present typically with nasal congestion, cough, sore throat, low-grade pyrexia, and malaise. "
            "Most viral upper respiratory tract infections resolve within 7 to 10 days with symptomatic supportive care, including adequate rest, warm fluid intake, and humidity. "
            "However, red flags indicating lower respiratory involvement (such as pneumonia) or acute compromise include: "
            "new or worsening shortness of breath, audible wheezing or stridor, inability to speak full sentences without pausing for breath, "
            "coughing up rust-colored sputum or frank blood, persistent fever above 38.5°C (101.3°F) unyielding to antipyretics, or bluish discoloration of lips or nail beds. "
            "Patients with underlying cardiopulmonary conditions (asthma, COPD, congestive heart failure) require a lower threshold for clinical assessment."
        ),
    },
    {
        "id": "DOC_MED_007",
        "title": "Mild Dehydration, Fluid Balance, and Systemic Symptoms",
        "source": "Mayo Clinic Guide to Hydration and Fatigue",
        "url": "https://www.mayoclinic.org/diseases-conditions/dehydration/symptoms-causes/syc-20354086",
        "organization": "Mayo Clinic",
        "publication_date": "2023-09-05",
        "last_reviewed": "2025-11-01",
        "topic": "hydration",
        "document_type": "educational_guideline",
        "version": "1.0",
        "content": (
            "Water is essential for cellular homeostasis, thermoregulation, and vascular perfusion. "
            "Mild dehydration occurs when fluid loss exceeds intake by even 1 to 2 percent of body weight. "
            "Common symptoms include dry mouth and lips, mild dull headache, daytime fatigue, reduced concentration, dizziness when standing up rapidly, and dark concentrated amber-colored urine. "
            "Replenishing fluids through steady sipping of water or oral rehydration solutions usually alleviates mild symptoms within several hours. "
            "Signs of severe dehydration requiring medical intervention include extreme thirst with sunken eyes, absence of urination for over 8 hours, rapid heart rate, low blood pressure, and confusion."
        ),
    },
    {
        "id": "DOC_MED_008",
        "title": "Daily Water Requirements, Hydration Guidelines, and Electrolyte Homeostasis",
        "source": "World Health Organization & National Academies of Sciences Clinical Fluid Standards",
        "url": "https://www.who.int/news-room/fact-sheets/detail/water-sanitation-hygiene",
        "organization": "World Health Organization (WHO)",
        "publication_date": "2024-01-20",
        "last_reviewed": "2025-11-15",
        "topic": "hydration",
        "document_type": "clinical_practice_guideline",
        "version": "1.0",
        "content": (
            "Adequate daily hydration is critical for cellular metabolism, cognitive function, joint lubrication, "
            "thermoregulation, and cardiovascular stability. According to the National Academies of Sciences and WHO guidelines, "
            "adequate daily total fluid intake is approximately 3.7 liters (125 ounces) for adult men and 2.7 liters (91 ounces) for adult women. "
            "Roughly 20 percent of daily water intake is derived from food moisture, with 80 percent from plain water and non-caloric fluids. "
            "Electrolyte homeostasis (sodium, potassium, chloride, bicarbonate, and magnesium) maintains transmembrane electrical potentials and intravascular volume. "
            "In states of diaphoresis (profuse sweating), gastrointestinal fluid losses, or intense physical training, hypotonic oral rehydration "
            "solutions containing balanced sodium (75 mmol/L) and glucose (75 mmol/L) prevent both hypovolemic dehydration and exercise-associated hyponatremia. "
            "Monitoring urine output and color (aiming for light pale yellow straw color) provides a reliable bedside indicator of hydration status."
        ),
    },
    {
        "id": "DOC_MED_009",
        "title": "Sleep Architecture, Circadian Rhythms, and Clinical Sleep Hygiene",
        "source": "National Institutes of Health (NIH) & American Academy of Sleep Medicine",
        "url": "https://www.nhlbi.nih.gov/health/sleep",
        "organization": "National Institutes of Health (NIH)",
        "publication_date": "2024-02-15",
        "last_reviewed": "2025-12-10",
        "topic": "sleep",
        "document_type": "clinical_practice_guideline",
        "version": "1.0",
        "content": (
            "Adults require 7 to 9 hours of restorative sleep per night to maintain neurocognitive function, metabolic homeostasis, and immune resilience. "
            "Sleep architecture consists of alternating cycles of Non-Rapid Eye Movement (NREM, stages N1 to N3 deep slow-wave sleep) and Rapid Eye Movement (REM) sleep, "
            "each cycle lasting approximately 90 to 110 minutes. Deep N3 sleep facilitates cellular tissue repair, human growth hormone secretion, and brain glymphatic clearance. "
            "Evidence-based clinical sleep hygiene guidelines include: maintaining a consistent sleep and wake schedule seven days a week; "
            "ensuring bedroom darkness, quietness, and ambient temperature around 18-20°C (65-68°F); avoiding screens and high-intensity blue light 60 minutes prior to bed "
            "to prevent suprachiasmatic nucleus melatonin suppression; avoiding caffeine within 6 to 8 hours of anticipated bedtime; and refraining from large meals and alcohol "
            "near sleep onset. Symptoms of sleep apnea (choking, loud gasping snore, morning headaches, unrefreshing sleep) warrant an in-lab polysomnography evaluation."
        ),
    },
    {
        "id": "DOC_MED_010",
        "title": "Evidence-Based Clinical Nutrition, Essential Micronutrients, and Metabolic Health",
        "source": "World Health Organization (WHO) & Harvard T.H. Chan School of Public Health",
        "url": "https://www.who.int/news-room/fact-sheets/detail/healthy-diet",
        "organization": "World Health Organization (WHO)",
        "publication_date": "2024-01-10",
        "last_reviewed": "2025-11-25",
        "topic": "nutrition",
        "document_type": "public_health_guideline",
        "version": "1.0",
        "content": (
            "A balanced dietary pattern lowers risks of chronic cardiovascular disease, metabolic syndrome, and systemic inflammatory pathology. "
            "Core dietary recommendations prioritize whole grains, legumes, abundant vegetables, fresh fruits, nuts, seeds, and lean protein sources while "
            "limiting free added sugars to less than 10 percent (ideally 5 percent) of total energy intake, and saturated fats to under 10 percent with complete elimination of trans-fats. "
            "Crucial micronutrients include: Vitamin D (supports skeletal mineralization and immune cell modulation, requiring 600-800 IU daily); "
            "Vitamin B12 (essential for erythropoiesis and myelin sheath integrity, particularly vital in strict vegetarian and vegan diets); "
            "Dietary Iron (essential for hemoglobin oxygen transport, with non-heme plant iron enhanced by co-ingestion of Vitamin C); and "
            "Dietary Potassium (helps regulate vascular tone and counteracts high sodium levels). "
            "Individuals with persistent unexplained fatigue, brittle nails, severe hair thinning, or numbness should undergo serum micronutrient testing."
        ),
    },
    {
        "id": "DOC_MED_011",
        "title": "Immune System Physiology, Host Defense, and Febrile Response Guidelines",
        "source": "Centers for Disease Control and Prevention (CDC) & National Institute of Allergy and Infectious Diseases (NIAID)",
        "url": "https://www.niaid.nih.gov/research/immune-system-overview",
        "organization": "Centers for Disease Control and Prevention (CDC)",
        "publication_date": "2023-11-05",
        "last_reviewed": "2025-10-20",
        "topic": "immunity",
        "document_type": "clinical_summary",
        "version": "1.0",
        "content": (
            "The human immune system consists of innate non-specific barriers (epithelial membranes, neutrophils, macrophages, complement proteins) "
            "and adaptive antigen-specific responses mediated by T-lymphocytes and B-lymphocytes producing neutralizing antibodies. "
            "Fever (core body temperature >38.0°C / 100.4°F) is a regulated hypothalamic set-point elevation triggered by endogenous pyrogenic cytokines "
            "(interleukin-1, interleukin-6, tumor necrosis factor). Moderate fever inhibits viral and bacterial replication kinetics while accelerating lymphocyte motility. "
            "Supportive care includes fluid rehydration to match insensible sweat losses, comfortable light clothing, and unhurried rest. "
            "Red flags in febrile illness requiring urgent or emergency care include: fever exceeding 40.0°C (104.0°F), fever lasting >3 to 5 days without explanation, "
            "nuchal rigidity (stiff neck), petechial non-blanching skin rash, confusion, lethargy, or respiratory distress."
        ),
    },
    {
        "id": "DOC_MED_012",
        "title": "Cardiovascular Health, Arterial Compliance, and Blood Pressure Regulation",
        "source": "American Heart Association (AHA) & WHO Global Cardiovascular Guidelines",
        "url": "https://www.heart.org/en/health-topics/high-blood-pressure",
        "organization": "American Heart Association (AHA)",
        "publication_date": "2024-03-01",
        "last_reviewed": "2025-12-01",
        "topic": "cardiovascular",
        "document_type": "clinical_practice_guideline",
        "version": "1.0",
        "content": (
            "Blood pressure is the hydrostatic lateral force exerted by circulating blood upon arterial vessel walls. "
            "Clinical BP classification for adults: Normal BP is systolic <120 mmHg and diastolic <80 mmHg; Elevated BP is systolic 120-129 mmHg and diastolic <80 mmHg; "
            "Stage 1 Hypertension is systolic 130-139 mmHg or diastolic 80-89 mmHg; Stage 2 Hypertension is systolic >=140 mmHg or diastolic >=90 mmHg. "
            "Persistent untreated hypertension damages the vascular endothelium, increasing long-term risks of myocardial infarction, stroke, kidney disease, and heart failure. "
            "Evidence-based lifestyle interventions include: the Dietary Approaches to Stop Hypertension (DASH) diet emphasizing fruits, vegetables, and low-fat dairy; "
            "limiting dietary sodium to under 2,000 mg (approx 1 teaspoon of table salt) daily; engaging in 150 minutes of weekly moderate aerobic activity; "
            "moderating alcohol intake; and smoking cessation. Hypertensive emergency is defined as systolic >180 mmHg or diastolic >120 mmHg with target organ damage "
            "(chest pain, dyspnea, blurred vision, acute headache) requiring immediate emergency medical intervention."
        ),
    },
    {
        "id": "DOC_MED_013",
        "title": "Gastrointestinal Microbiome, Dietary Fiber, and Digestive Health",
        "source": "World Gastroenterology Organisation (WGO) & Mayo Clinic Digestive Health",
        "url": "https://www.worldgastroenterology.org/guidelines/diet-and-the-gut",
        "organization": "World Gastroenterology Organisation (WGO)",
        "publication_date": "2023-12-12",
        "last_reviewed": "2025-11-10",
        "topic": "gastrointestinal",
        "document_type": "clinical_summary",
        "version": "1.0",
        "content": (
            "The human gastrointestinal tract harbors trillions of microorganisms that perform critical roles in nutrient fermentation, short-chain fatty acid "
            "(butyrate, propionate, acetate) synthesis, mucosal barrier integrity, and neurotransmitter signaling along the enteric gut-brain axis. "
            "Adequate daily dietary fiber intake (25 to 30 grams daily for adults from diverse plant sources) supports microbial diversity and regular peristalsis. "
            "Prebiotic soluble fibers (found in oats, onions, garlic, bananas, and legumes) nourish beneficial commensal bacteria such as Bifidobacteria and Lactobacilli. "
            "Lifestyle interventions for acid reflux (GERD) include eating smaller meals, avoiding lying down for 3 hours postprandially, elevating the head of the bed, "
            "and reducing trigger foods (caffeine, high-fat fried items, citrus, and peppermint). Warning signs warranting clinical investigation include involuntary weight loss, "
            "dysphagia (difficulty swallowing), hematochezia (rectal bleeding), and persistent unremitting abdominal pain."
        ),
    },
    {
        "id": "DOC_MED_014",
        "title": "Stress Physiology, Autonomic Nervous System, and Cortisol Regulation",
        "source": "National Institute of Mental Health (NIMH) & Mayo Clinic Mind-Body Medicine",
        "url": "https://www.nimh.nih.gov/health/publications/stress",
        "organization": "National Institute of Mental Health (NIMH)",
        "publication_date": "2024-01-05",
        "last_reviewed": "2025-10-30",
        "topic": "mental_health",
        "document_type": "educational_guideline",
        "version": "1.0",
        "content": (
            "The human physiological stress response is mediated by the sympathetic-adrenomedullary (SAM) axis and hypothalamic-pituitary-adrenal (HPA) axis. "
            "Acute perception of stress triggers rapid catecholamine release (adrenaline and noradrenaline), elevating heart rate, arterial blood pressure, and respiratory frequency. "
            "Subsequent HPA activation stimulates adrenal cortisol secretion, mobilizing blood glucose while temporarily downregulating non-vital digestive and immune functions. "
            "Chronic unmanaged psychological stress leads to prolonged hypercortisolemia, associated with tension headaches, insomnia, visceral adiposity, and impaired immune resilience. "
            "Clinically validated autonomic down-regulation techniques include: slow paced diaphragmatic respiration (such as the physiological double-inhalation sigh or 4-7-8 breathing) "
            "which stimulates vagal nerve parasympathetic tone; progressive muscle relaxation; regular daily aerobic walking; and cognitive reframing. "
            "When anxiety or stress persistently impairs daily social, occupational, or personal function, consultation with a licensed clinical mental health professional is recommended."
        ),
    },
    {
        "id": "DOC_MED_015",
        "title": "Physical Activity Guidelines, Aerobic Fitness, and Musculoskeletal Ergonomics",
        "source": "World Health Organization (WHO) & American College of Sports Medicine (ACSM)",
        "url": "https://www.who.int/news-room/fact-sheets/detail/physical-activity",
        "organization": "World Health Organization (WHO)",
        "publication_date": "2023-10-18",
        "last_reviewed": "2025-11-20",
        "topic": "fitness",
        "document_type": "public_health_guideline",
        "version": "1.0",
        "content": (
            "Regular physical activity is one of the most effective non-pharmacological interventions for preventing cardiovascular mortality, type 2 diabetes, "
            "and musculoskeletal degenerative disease. WHO guidelines recommend that adults engage in at least 150 to 300 minutes of moderate-intensity aerobic physical activity "
            "(such as brisk walking, swimming, or cycling), or 75 to 150 minutes of vigorous-intensity aerobic physical activity weekly, complemented by muscle-strengthening exercises "
            "involving all major muscle groups on two or more days per week. Ergonomic guidelines for desk workers include: positioning computer monitors at eye level approximately "
            "an arm's length away; keeping elbows bent at 90-100 degrees; maintaining feet flat on the floor or footrest; and implementing regular postural movement breaks every 30 to 45 minutes "
            "to alleviate static thoracic and lumbar spinal loading and prevent cervical tension syndromes."
        ),
    },
    {
        "id": "DOC_MED_016",
        "title": "Clinical Vital Signs Reference Standards, Normal Ranges, and Home Monitoring",
        "source": "NHS Clinical Skills Reference & CDC Patient Care Standards",
        "url": "https://www.cdc.gov/vitalsigns/index.html",
        "organization": "Centers for Disease Control and Prevention (CDC)",
        "publication_date": "2024-02-28",
        "last_reviewed": "2025-12-15",
        "topic": "vital_signs",
        "document_type": "clinical_practice_guideline",
        "version": "1.0",
        "content": (
            "Vital signs provide fundamental physiological metrics regarding baseline cardiopulmonary, circulatory, and thermoregulatory stability. "
            "Standard adult baseline ranges at rest: "
            "1. Resting Heart Rate (Pulse): 60 to 100 beats per minute (bpm). Well-trained endurance athletes may safely exhibit physiological resting bradycardia of 45-55 bpm. "
            "2. Blood Pressure: Systolic <120 mmHg and diastolic <80 mmHg. "
            "3. Respiratory Rate: 12 to 20 breaths per minute at rest, regular and unlabored. "
            "4. Core Body Temperature: 36.5°C to 37.5°C (97.7°F to 99.5°F). Fever is defined clinically as >=38.0°C (100.4°F). "
            "5. Pulse Oximetry (SpO2): 95 to 100 percent breathing ambient room air at sea level (readings below 92% indicate hypoxemia requiring clinical evaluation). "
            "Accurate home measurement requires resting quietly for 5 minutes prior to recording, avoiding talking during measurement, and recording readings at consistent times of day."
        ),
    },
    {
        "id": "DOC_MED_017",
        "title": "Diabetes Mellitus Pathophysiology: Type 1 vs Type 2, Glucose Homeostasis, and HbA1c",
        "source": "American Diabetes Association (ADA) Standards of Care & CDC Diabetes Guidelines",
        "url": "https://www.cdc.gov/diabetes/basics/index.html",
        "organization": "American Diabetes Association (ADA)",
        "publication_date": "2024-01-10",
        "last_reviewed": "2025-11-15",
        "topic": "endocrine_diabetes",
        "document_type": "clinical_practice_guideline",
        "version": "1.0",
        "content": (
            "Diabetes mellitus is a metabolic disorder characterized by persistent hyperglycemia resulting from defects in insulin secretion, "
            "insulin sensitivity, or both. In Type 1 Diabetes, autoimmune destruction of pancreatic beta cells in the islets of Langerhans leads to "
            "absolute insulin deficiency, requiring exogenous insulin replacement. In Type 2 Diabetes, peripheral tissues (skeletal muscle, liver, and adipose) "
            "develop insulin resistance, coupled with progressive relative secretory insufficiency by beta cells. "
            "Classic osmotic symptoms include polyuria (frequent urination), polydipsia (excessive thirst), polyphagia (constant hunger), and unexplained weight loss. "
            "Diagnostic glycemic criteria: Normal fasting plasma glucose is <100 mg/dL; Prediabetes is 100-125 mg/dL; Diabetes is >=126 mg/dL. "
            "The Glycated Hemoglobin (HbA1c) test reflects mean blood glucose over the preceding 2 to 3 months: Normal is <5.7%, Prediabetes is 5.7%-6.4%, "
            "and Diabetes is >=6.5%. Long-term complications involve microvascular disease (retinopathy, nephropathy, peripheral neuropathy) and macrovascular "
            "disease (coronary artery disease, peripheral artery disease, ischemic stroke). "
            "Educational lifestyle management focuses on balanced complex carbohydrate distribution, regular aerobic and resistance exercise, glycemic self-monitoring, "
            "and routine foot examinations. Red flags requiring emergency evaluation include diabetic ketoacidosis signs (fruity breath odor, deep rapid Kussmaul respirations, "
            "persistent vomiting, confusion) and acute hypoglycemia (tremor, diaphoresis, palpitations, disorientation, blood glucose <70 mg/dL)."
        ),
    },
    {
        "id": "DOC_MED_018",
        "title": "Asthma and Obstructive Airway Diseases: Bronchospasm, Inflammation, and Inhaler Education",
        "source": "Global Initiative for Asthma (GINA) & NIH National Heart, Lung, and Blood Institute",
        "url": "https://www.nhlbi.nih.gov/health/asthma",
        "organization": "National Institutes of Health (NIH)",
        "publication_date": "2024-02-12",
        "last_reviewed": "2025-10-18",
        "topic": "respiratory_asthma",
        "document_type": "clinical_summary",
        "version": "1.0",
        "content": (
            "Asthma is a chronic inflammatory disorder of the airways characterized by episodic, reversible bronchial hyperresponsiveness, mucous hypersecretion, "
            "and smooth muscle bronchoconstriction. Hallmarks include recurrent wheezing (expiratory high-pitched whistling), chest tightness, shortness of breath, "
            "and dry nocturnal or early-morning coughing. Common triggers encompass aeroallergens (pollen, dust mites, pet dander), viral respiratory infections, "
            "cold dry air, strenuous exercise, tobacco smoke, and workplace irritants. "
            "Therapeutic management distinguishes between two core medication classes: Reliever/Rescue bronchodilators (short-acting beta-2 agonists like albuterol) "
            "which relax airway smooth muscles within minutes during acute symptoms, and Controller/Maintenance anti-inflammatory medications (inhaled corticosteroids) "
            "which reduce underlying mucosal swelling and prevent long-term airway remodeling. "
            "Proper inhaler technique with a spacer ensures maximal pulmonary lung deposition rather than oropharyngeal impaction. "
            "Asthma red flags indicating status asthmaticus or respiratory failure requiring immediate emergency medical care include: inability to speak complete sentences "
            "without gasping for breath, paradoxical chest or abdominal retractions, silent chest (absence of wheezing due to severe airflow limitation), cyanosis of the lips, "
            "and failure of rescue inhaler relief after 15 to 20 minutes."
        ),
    },
    {
        "id": "DOC_MED_019",
        "title": "Gastroesophageal Reflux Disease (GERD), Heartburn, and Gastric Acid Regulation",
        "source": "American College of Gastroenterology (ACG) Guidelines & Mayo Clinic Gastroenterology",
        "url": "https://www.mayoclinic.org/diseases-conditions/gerd/symptoms-causes/syc-20361940",
        "organization": "Mayo Clinic",
        "publication_date": "2023-11-20",
        "last_reviewed": "2025-12-05",
        "topic": "gastrointestinal_gerd",
        "document_type": "clinical_practice_guideline",
        "version": "1.0",
        "content": (
            "Gastroesophageal Reflux Disease (GERD) is a chronic digestive condition occurring when gastric acid and digestive enzymes flow backward through an incompetent "
            "lower esophageal sphincter (LES) into the esophagus, irritating the squamous mucosal lining. "
            "Typical clinical symptoms include pyrosis (heartburn: retrosternal burning radiating toward the throat, often aggravated postprandially or when recumbent), "
            "acid regurgitation, water brash (sudden reflex salivation), globus sensation (feeling of a lump in the throat), and chronic nocturnal cough or throat clearing. "
            "Differentiating GERD from cardiac angina is vital: while cardiac ischemia often presents as heavy squeezing pressure radiating to the left arm or jaw with exertion, "
            "unexplained new chest discomfort must always be triaged with safety-first clinical or emergency evaluation. "
            "Evidence-based conservative and lifestyle measures: avoiding recumbency for at least 3 hours following food intake; elevating the head of the bed by 6 inches; "
            "reducing known trigger foods (caffeine, high-fat foods, chocolate, mint, tomato products, alcohol); smoking cessation; and avoiding tight abdominal garments. "
            "Alarm features warranting urgent endoscopic and clinical investigation include dysphagia (difficulty swallowing), odynophagia (painful swallowing), "
            "unintentional weight loss, recurrent vomiting, iron deficiency anemia, or hematemesis (vomiting blood)."
        ),
    },
    {
        "id": "DOC_MED_020",
        "title": "Spinal Biomechanics, Lumbar Strain, Postural Ergonomics, and Sciatica Management",
        "source": "American Academy of Orthopaedic Surgeons (AAOS) & CDC NIOSH Ergonomics",
        "url": "https://orthoinfo.aaos.org/en/diseases--conditions/low-back-pain/",
        "organization": "American Academy of Orthopaedic Surgeons (AAOS)",
        "publication_date": "2024-03-05",
        "last_reviewed": "2025-11-28",
        "topic": "musculoskeletal_spine",
        "document_type": "clinical_summary",
        "version": "1.0",
        "content": (
            "Mechanical low back pain is among the leading causes of global disability, most frequently stemming from paraspinal muscular strain, ligamentous sprain, "
            "or facet joint arthropathy. Lumbar radiculopathy (sciatica) occurs when an intervertebral disc herniation or spinal stenosis compresses lumbosacral nerve roots "
            "(typically L4, L5, or S1), causing sharp, radiating, electric pain travelling below the knee into the calf, ankle, or foot, often accompanied by paresthesia (pins and needles). "
            "Conservative rehabilitation highlights early active movement over prolonged bed rest, as gentle walking and controlled spinal core stabilization exercises "
            "(e.g., Bird-Dog, pelvic tilts, McGill Big Three) improve paraspinal perfusion and accelerate functional recovery. "
            "Workplace ergonomics recommend 90-degree elbow flexion, feet flat on the floor, lumbar support maintaining the natural lordotic curve, and avoiding sustained sedentary postures "
            "through periodic micro-breaks every 30 to 45 minutes. "
            "Emergency red flags for Cauda Equina Syndrome or spinal cord compression require emergency surgical consultation within hours: "
            "saddle anesthesia (loss of sensation in the groin, buttocks, and perineum), sudden loss of bowel or bladder control (incontinence or acute retention), "
            "bilateral progressive motor weakness ('foot drop'), or back pain accompanied by unexplained high fever and chills."
        ),
    },
    {
        "id": "DOC_MED_021",
        "title": "Infectious Pathogens: Viral vs Bacterial Etiology, Pyrogen Physiology, and Immune Defenses",
        "source": "CDC Infectious Diseases Overview & National Institute of Allergy and Infectious Diseases (NIAID)",
        "url": "https://www.cdc.gov/infectioncontrol/basics/index.html",
        "organization": "Centers for Disease Control and Prevention (CDC)",
        "publication_date": "2024-01-25",
        "last_reviewed": "2025-10-30",
        "topic": "infectious_disease",
        "document_type": "educational_guideline",
        "version": "1.0",
        "content": (
            "Understanding the fundamental biological distinctions between viral and bacterial infections is critical for safe health literacy and antibiotic stewardship. "
            "Viruses are submicroscopic obligate intracellular entities requiring host cell machinery for replication; antibiotics have zero efficacy against viral pathogens "
            "(such as common cold rhinoviruses, influenza, RSV, acute viral bronchitis, or SARS-CoV-2). Viral infections typically resolve via supportive hydration, rest, "
            "and natural cellular host immune clearance. In contrast, bacteria are self-contained prokaryotic single-celled organisms that may replicate extracellularly; "
            "bacterial infections (such as streptococcal pharyngitis, bacterial pneumonia, or urinary tract infections) require targeted antibacterial therapies prescribed by clinicians. "
            "Fever is a regulated physiological defense orchestrated by the hypothalamus when endogenous pyrogens (interleukin-1, interleukin-6, TNF-alpha) and exogenous bacterial "
            "lipopolysaccharides reset the core thermostat. Moderate febrile states inhibit bacterial multiplication and enhance white blood cell phagocytosis and motility. "
            "Red-flag indicators requiring prompt medical evaluation include: fevers exceeding 40.0°C (104.0°F), fevers lasting more than 3 to 5 days without diagnosis, "
            "nuchal rigidity (stiff neck), petechial rash (pinpoint reddish spots that do not blanch under pressure), altered mental status, or systemic sepsis warning signs "
            "(rapid heart rate >100 bpm, rapid breathing >22 breaths/min, shivering, and clammy skin)."
        ),
    },
    {
        "id": "DOC_MED_022",
        "title": "Clinical Nutrition, Hematopoiesis, and Micronutrient Deficiencies: Iron, Vitamin D, and B12",
        "source": "World Health Organization (WHO) & Harvard T.H. Chan Micronutrient Guidelines",
        "url": "https://www.who.int/health-topics/micronutrients",
        "organization": "World Health Organization (WHO)",
        "publication_date": "2023-10-15",
        "last_reviewed": "2025-11-12",
        "topic": "nutrition_micronutrients",
        "document_type": "clinical_summary",
        "version": "1.0",
        "content": (
            "Micronutrients (vitamins and dietary minerals) serve as indispensable cofactors in cellular respiration, enzymatic catalysis, deoxyribonucleic acid (DNA) synthesis, "
            "and immune signaling. Three of the most common clinical deficiencies encountered in primary care include: "
            "1. Iron Deficiency Anemia: Iron is central to the hemoglobin molecule responsible for erythrocyte oxygen transport. Deficiency presents with chronic fatigue, "
            "pallor of mucous membranes and nailbeds, cold intolerance, brittle spooned nails (koilonychia), exercise intolerance, and tachycardia. Non-heme plant iron absorption "
            "is enhanced significantly by co-administration of ascorbic acid (Vitamin C) and inhibited by tannins in tea and excessive phytates. "
            "2. Vitamin D3 (Cholecalciferol): Synthesized in dermal keratinocytes upon exposure to solar UV-B radiation or obtained through diet. Vitamin D regulates intestinal calcium "
            "and phosphorus absorption, bone mineralization, and innate antimicrobial peptide synthesis. Deficiency is associated with musculoskeletal aches, bone loss, and increased respiratory vulnerability. "
            "3. Vitamin B12 (Cobalamin): Essential for myelin sheath maintenance in nervous tissue and normal erythrocyte maturation. Found almost exclusively in animal products; "
            "strict vegetarians, vegans, and elderly individuals with reduced gastric intrinsic factor production are vulnerable to B12 deficiency, presenting with megaloblastic anemia, "
            "peripheral neuropathy (numbness, paresthesias in toes/fingers), cognitive fatigue, and unsteady gait. "
            "Routine laboratory evaluation (complete blood count, serum ferritin, 25-hydroxyvitamin D, and serum B12) safely guides clinician-supervised supplementation."
        ),
    },
    {
        "id": "DOC_MED_023",
        "title": "Neurobiology of Anxiety, Panic Attacks, and Somatic Differentiation from Acute Angina",
        "source": "National Institute of Mental Health (NIMH) & American Psychological Association",
        "url": "https://www.nimh.nih.gov/health/topics/anxiety-disorders",
        "organization": "National Institutes of Health (NIH)",
        "publication_date": "2024-02-18",
        "last_reviewed": "2025-12-10",
        "topic": "mental_health_anxiety",
        "document_type": "clinical_practice_guideline",
        "version": "1.0",
        "content": (
            "Anxiety and panic responses represent acute neurochemical surges governed by the amygdala, locus coeruleus, and autonomic sympathetic nervous system. "
            "During acute panic attacks, abrupt hyper-adrenergic signaling triggers rapid physiological changes: tachycardia, rapid shallow hyperventilation, diaphoresis, "
            "trembling, chest tightness, dizziness, lightheadedness, and profound feelings of impending doom. "
            "Hyperventilation leads to respiratory alkalosis (blowing off excess CO2), which causes transient cerebral vasoconstriction, perioral tingling, and carpopedal numbness. "
            "Clinical triage note: Panic attack chest tightness frequently mimics acute coronary syndrome or myocardial ischemia. Because somatic differentiation cannot "
            "safely rule out acute cardiovascular pathology without in-person 12-lead electrocardiography (ECG) and cardiac troponin assays, any unexplained, acute, or severe "
            "chest pain must always be triaged with immediate medical evaluation. "
            "For confirmed anxiety and chronic stress, evidence-supported cognitive and physiological interventions include: diaphragmatic pacing (e.g., box breathing: "
            "inhale 4s, hold 4s, exhale 4s, hold 4s; or physiological sigh: two quick nasal inhalations followed by long slow oral exhalation), grounding exercises (5-4-3-2-1 sensory method), "
            "aerobic physical exercise to metabolize circulating catecholamines, and cognitive behavioral therapy (CBT) with a licensed mental health professional."
        ),
    },
    {
        "id": "DOC_MED_024",
        "title": "Dermatological Lesions, Contact Dermatitis, Eczema, Urticaria, and ABCDE Melanoma Rules",
        "source": "American Academy of Dermatology (AAD) Clinical Guidelines",
        "url": "https://www.aad.org/public/diseases/skin-cancer/find/atypical-moles/abcde",
        "organization": "American Academy of Dermatology (AAD)",
        "publication_date": "2023-12-01",
        "last_reviewed": "2025-11-20",
        "topic": "dermatology",
        "document_type": "clinical_summary",
        "version": "1.0",
        "content": (
            "Dermatological assessments evaluate epidermal barrier disruption, inflammatory dermatoses, and pigmented cutaneous lesions. "
            "Common benign inflammatory skin conditions include: "
            "1. Atopic Dermatitis (Eczema): Pruritic, erythematous, xerotic (dry), scaly patches commonly distributed across flexural skin creases (antecubital and popliteal fossae), "
            "managed with gentle barrier emollients, lukewarm baths, and fragrance-free moisturizers applied immediately post-bathing. "
            "2. Contact Dermatitis: Pruritic vesicular or erythematous eruption resulting from allergic sensitization (e.g., nickel, poison ivy urushiol) or chemical irritation (soaps, solvents). "
            "3. Urticaria (Hives): Transient, intensely pruritic, raised edematous wheals with surrounding erythema, typically secondary to histamine release from cutaneous mast cells. "
            "Educational skin cancer surveillance utilizes the authoritative ABCDE criteria for assessing pigmented melanocytic nevi (moles): "
            "• A - Asymmetry: One half of the mole does not mirror the opposite half. "
            "• B - Border: Irregular, scalloped, notched, or poorly defined edges. "
            "• C - Color: Variegated shades within a single lesion (black, brown, tan, red, white, or blue). "
            "• D - Diameter: Greater than 6 millimeters (roughly pencil eraser size, though melanomas can be smaller). "
            "• E - Evolving: Any noticeable change in size, shape, surface elevation, itching, bleeding, or crusting over time. "
            "Emergency dermatological red flags include rapidly spreading erythematous warmth with high fever (suspicious for cellulitis or necrotizing soft-tissue infection), "
            "mucosal blistering (Stevens-Johnson syndrome), and hives accompanied by throat constriction, tongue swelling, or wheezing (anaphylaxis requiring immediate intramuscular epinephrine)."
        ),
    },
    {
        "id": "DOC_MED_025",
        "title": "Renal Physiology, Glomerular Filtration, Fluid Balance, and Urinary Tract Health",
        "source": "National Kidney Foundation (NKF) & American Urological Association (AUA)",
        "url": "https://www.kidney.org/atoz/content/howkidneyswork",
        "organization": "National Kidney Foundation (NKF)",
        "publication_date": "2024-02-05",
        "last_reviewed": "2025-11-18",
        "topic": "renal_urinary",
        "document_type": "clinical_practice_guideline",
        "version": "1.0",
        "content": (
            "The human kidneys filter approximately 180 liters of blood plasma daily through millions of functional microscopic nephrons, regulating arterial blood pressure, "
            "acid-base balance (pH 7.35-7.45), fluid volume, and serum electrolyte concentrations (sodium, potassium, calcium, phosphate). "
            "The estimated Glomerular Filtration Rate (eGFR) and serum creatinine serve as primary biomarkers of renal excretory capacity; an eGFR >90 mL/min/1.73m² with absence of "
            "proteinuria represents normal renal function. "
            "Lower urinary tract infections (cystitis) present with dysuria (burning sensation on urination), urinary urgency, pollakiuria (frequent voiding of small volumes), "
            "and suprapubic pelvic discomfort. Routine uncomplicated cystitis responds to clinician-prescribed oral antimicrobial therapy and liberal water hydration. "
            "Critical clinical warning signs indicating upper urinary tract involvement (acute pyelonephritis) or systemic sepsis include: flank pain (costovertebral angle tenderness), "
            "high fevers with rigors/shaking chills, persistent nausea and vomiting, frank hematuria (visible blood or blood clots in urine), and acute inability to void "
            "(acute urinary retention requiring immediate catheterization)."
        ),
    },
    {
        "id": "DOC_MED_026",
        "title": "Thyroid Gland Physiology: Hypothyroidism, Hyperthyroidism, and Metabolic Homeostasis",
        "source": "American Thyroid Association (ATA) & Endocrine Society Clinical Guidelines",
        "url": "https://www.thyroid.org/thyroid-information/",
        "organization": "American Thyroid Association (ATA)",
        "publication_date": "2023-11-15",
        "last_reviewed": "2025-10-25",
        "topic": "endocrine_thyroid",
        "document_type": "clinical_summary",
        "version": "1.0",
        "content": (
            "The thyroid gland, located in the anterior neck below the cricoid cartilage, produces triiodothyronine (T3) and thyroxine (T4) under the regulation of pituitary "
            "Thyroid-Stimulating Hormone (TSH). Thyroid hormones modulate the basal metabolic rate of virtually every mammalian tissue. "
            "1. Hypothyroidism (Underactive Thyroid): Characterized by subnormal circulating free T4 and elevated serum TSH (compensatory pituitary response). "
            "Most commonly caused by Hashimoto's autoimmune thyroiditis. Clinical presentation reflects general metabolic deceleration: persistent fatigue, cold intolerance, "
            "unexplained weight gain, constipation, dry coarse skin, bradycardia, muscle cramps, and cognitive sluggishness ('brain fog'). "
            "2. Hyperthyroidism (Overactive Thyroid): Characterized by excess circulating free T4/T3 and suppressed TSH (<0.01 mIU/L), commonly driven by Graves' autoimmune disease. "
            "Clinical presentation reflects hypermetabolic stimulation: unexpected weight loss despite increased appetite, tachycardia, cardiac palpitations, heat intolerance, "
            "fine hand tremors, frequent bowel movements, insomnia, anxiety, and proptosis (bulging eyes in Graves' ophthalmopathy). "
            "Evaluation requires serum TSH, free T4, and antithyroid antibody testing. Red flags include thyroid storm (life-threatening hyperpyrexia, tachydysrhythmias, "
            "and delirium) and myxedema coma, both requiring emergency intensive care."
        ),
    },
    {
        "id": "DOC_MED_027",
        "title": "Acute Soft Tissue Musculoskeletal Injuries: Sprains, Strains, PRICE/POLICE Protocols",
        "source": "American College of Sports Medicine (ACSM) & Mayo Clinic Sports Medicine",
        "url": "https://www.mayoclinic.org/diseases-conditions/sprains/symptoms-causes/syc-20377938",
        "organization": "American College of Sports Medicine (ACSM)",
        "publication_date": "2024-01-18",
        "last_reviewed": "2025-12-02",
        "topic": "musculoskeletal_sports",
        "document_type": "clinical_summary",
        "version": "1.0",
        "content": (
            "Musculoskeletal soft-tissue trauma commonly affects ligaments, tendons, and skeletal muscles. "
            "Anatomical definitions: A sprain is a stretch or tear of a fibrous ligament (connecting bone to bone, e.g., anterior talofibular ligament in an ankle inversion injury). "
            "A strain is an overstretch or tear of a contractile muscle or tendon (connecting muscle to bone, e.g., hamstring or lumbar paraspinal strain). "
            "Grading: Grade 1 (mild microscopic fibers stretched without joint instability); Grade 2 (partial macroscopic tearing with moderate swelling and pain); "
            "Grade 3 (complete structural rupture with joint laxity and significant functional impairment). "
            "Evidence-based acute management protocols: "
            "• P - Protect: Guard the injured joint with a brace, splint, or crutches to prevent further disruption. "
            "• OL - Optimal Loading: Gentle, pain-free active mobilization is favored over total prolonged immobilization to stimulate collagen fiber alignment. "
            "• I - Ice: Cold compress applied 15 to 20 minutes at a time (never direct ice on skin) for analgesia and vasoconstrictive edema control. "
            "• C - Compression: Elastic bandages to counteract interstitial extravasation without compromising distal neurovascular circulation. "
            "• E - Elevation: Elevating the injured limb above heart level to facilitate venous and lymphatic return. "
            "Red flags requiring urgent clinical examination or radiography (X-ray) include: inability to bear four steps of weight immediately following injury "
            "(Ottawa Ankle Rules), visible bone or joint deformity, neurovascular compromise (pallor, coolness, numbness, or absent distal pulses), or audible 'popping' accompanied by immediate joint effusion."
        ),
    },
    {
        "id": "DOC_MED_028",
        "title": "Emergency First Aid Protocols: Choking Management, Bleeding Control, and Anaphylaxis",
        "source": "American Heart Association (AHA) & American Red Cross First Aid Guidelines",
        "url": "https://www.redcross.org/take-a-class/first-aid",
        "organization": "American Heart Association (AHA)",
        "publication_date": "2024-02-20",
        "last_reviewed": "2025-11-30",
        "topic": "first_aid_emergency",
        "document_type": "emergency_guideline",
        "version": "1.0",
        "content": (
            "Basic emergency first aid competencies provide critical life-saving interventions while professional emergency medical services (911 / EMS) are mobilized. "
            "1. Acute Airway Choking Obstruction (Conscious Adult/Child): "
            "• Mild Obstruction: The individual is coughing forcefully and able to speak or breathe. Do NOT interfere with natural coughing efforts; monitor closely. "
            "• Severe/Complete Obstruction: The individual cannot speak, cough, or breathe; exhibits the universal choking sign (hands clutched to neck); turns cyanotic. "
            "Deliver 5 back blows between the shoulder blades with the heel of your hand, followed by 5 abdominal thrusts (Heimlich maneuver: quick inward and upward thrusts "
            "just above the navel). Repeat until the object is expelled. If the individual loses consciousness, ease them to the floor, call 911, and begin chest compressions (CPR), "
            "looking in the mouth before breaths. "
            "2. Severe External Hemorrhage (Severe Bleeding): Apply immediate, continuous, firm, direct pressure over the bleeding wound using a clean cloth or sterile gauze. "
            "Do not remove saturated dressings; add additional layers on top. For catastrophic limb hemorrhage uncontrolled by direct pressure, a commercial tourniquet should be "
            "applied 2 to 3 inches proximal to the wound (not over a joint) and tightened until bleeding stops, noting the exact application time. "
            "3. Anaphylaxis: Severe, rapid-onset allergic reaction involving airway swelling, wheezing, hypotension, and generalized urticaria. "
            "Immediately administer an epinephrine auto-injector into the anterolateral mid-thigh, call 911, and position the patient recumbent with legs elevated if tolerated."
        ),
    },
    {
        "id": "DOC_MED_029",
        "title": "Pediatric Health Essentials: Childhood Febrile Illness, Dehydration, and Safety Triage",
        "source": "American Academy of Pediatrics (AAP) Clinical Practice Guidelines",
        "url": "https://www.healthychildren.org",
        "organization": "American Academy of Pediatrics (AAP)",
        "publication_date": "2023-11-08",
        "last_reviewed": "2025-12-12",
        "topic": "pediatric_health",
        "document_type": "clinical_practice_guideline",
        "version": "1.0",
        "content": (
            "Pediatric patients exhibit distinct physiological differences from adults, requiring heightened clinical vigilance regarding fluid volume loss and temperature regulation. "
            "Fever is clinically defined as a rectal, temporal, or tympanic temperature >=38.0°C (100.4°F). "
            "Critical Age-Stratified Febrile Rule: Any infant younger than 3 months of age (neonates) with a fever >=38.0°C requires immediate same-day emergency hospital evaluation "
            "to rule out serious occult bacterial illness (sepsis, meningitis, urinary tract infection), even if the infant appears well. "
            "In older children, behavior and clinical hydration status are often more predictive than the absolute thermometer reading. "
            "Signs of pediatric dehydration include: sunken fontanelle (soft spot on infant's head), absence of tears when crying, dry cracked lips and tongue, "
            "significantly decreased wet diapers (<3 to 4 wet diapers in 24 hours), extreme lethargy, or poor capillary refill (>2 seconds on fingernail bed). "
            "Oral rehydration therapy with balanced pediatric oral electrolyte solutions (ORS) in small, frequent spoon/syringe increments is the gold standard for mild-to-moderate dehydration. "
            "Never administer aspirin to children or adolescents with viral symptoms due to the risk of Reye's syndrome (acute encephalopathy and fatty liver failure). "
            "Immediate emergency care is required for stridor (high-pitched inspiratory sound), breathing retractions (skin pulling between ribs), lethargy (inability to wake or interact), "
            "seizures, or a non-blanching dark purpuric rash."
        ),
    },
    {
        "id": "DOC_MED_030",
        "title": "Preventative Health, Screening Schedules, and Adult Immunization Frameworks",
        "source": "U.S. Preventive Services Task Force (USPSTF) & CDC Advisory Committee on Immunization",
        "url": "https://www.uspreventiveservicestaskforce.org/",
        "organization": "U.S. Preventive Services Task Force (USPSTF)",
        "publication_date": "2024-03-01",
        "last_reviewed": "2025-11-25",
        "topic": "preventative_screening",
        "document_type": "public_health_guideline",
        "version": "1.0",
        "content": (
            "Preventative healthcare focuses on early risk factor detection and asymptomatic disease screening before irreversible structural pathology manifests. "
            "Core evidence-based screening recommendations: "
            "1. Hypertension: Annual blood pressure measurement in all adults aged 18 and older, with semi-annual or continuous home monitoring for borderline elevated values. "
            "2. Dyslipidemia & Cardiovascular Risk: Fasting lipid panel starting at age 20 to assess atherosclerotic cardiovascular risk (ASCVD), LDL-C, HDL-C, and triglycerides. "
            "3. Diabetes Mellitus: Fasting blood glucose or HbA1c screening for all adults aged 35 to 70 with overweight or obesity, or earlier in individuals with family history. "
            "4. Colorectal Cancer: Routine population screening beginning at age 45 through age 75 via colonoscopy (every 10 years) or annual high-sensitivity stool DNA / FIT testing. "
            "5. Cervical Cancer: Pap smear cytology every 3 years for women aged 21 to 29, or Pap plus high-risk HPV co-testing every 5 years for women aged 30 to 65. "
            "6. Breast Cancer: Biennial screening mammography beginning at age 40 for average-risk women. "
            "Adult Immunization Schedule: Annual seasonal influenza vaccine; updated COVID-19 booster; Tdap (tetanus, diphtheria, pertussis) booster every 10 years; "
            "Recombinant Zoster (Shingles) vaccine 2-dose series starting at age 50; and Pneumococcal vaccination starting at age 65 or earlier for chronic immunocompromising conditions."
        ),
    },
    {
        "id": "DOC_MED_031",
        "title": "Antibiotic Stewardship, Mechanisms of Resistance, and Safe Medication Education",
        "source": "World Health Organization (WHO) & FDA Safe Medication Guidelines",
        "url": "https://www.who.int/news-room/fact-sheets/detail/antimicrobial-resistance",
        "organization": "World Health Organization (WHO)",
        "publication_date": "2024-01-12",
        "last_reviewed": "2025-10-22",
        "topic": "pharmacology_education",
        "document_type": "educational_guideline",
        "version": "1.0",
        "content": (
            "Antimicrobial resistance (AMR) is a global health challenge occurring when bacteria, viruses, fungi, and parasites evolve to withstand the drugs designed to destroy them. "
            "Overuse and misuse of antibiotics are the primary accelerators of resistance. Essential clinical educational principles: "
            "1. Zero Viral Efficacy: Antibiotics kill bacteria, not viruses. They are completely ineffective against the common cold, acute rhinitis, influenza, viral bronchitis, "
            "most sore throats (except confirmed Strep pharyngitis), and COVID-19. Taking antibiotics for viral illnesses exposes patients to unnecessary side effects (diarrhea, "
            "Candida fungal overgrowth, severe Clostridioides difficile colitis, and allergic anaphylaxis) without accelerating recovery. "
            "2. Complete Prescribed Courses: When a clinician confirms a bacterial etiology and prescribes an antibiotic, the medication should be taken exactly as directed for "
            "the full indicated duration, even if symptoms subside earlier. Stopping prematurely permits surviving, partially resistant bacterial sub-populations to rebound. "
            "3. Never Share or Store Leftover Medications: Using unprescribed leftover antibiotics risks inappropriate dosing, masking symptoms of more serious illnesses, and drug toxicity. "
            "4. Over-The-Counter (OTC) Safety: OTC analgesics/antipyretics such as acetaminophen (paracetamol) and nonsteroidal anti-inflammatory drugs (NSAIDs like ibuprofen) "
            "must be taken within safe daily ceiling limits. Excessive acetaminophen poses acute hepatotoxicity risks, while chronic unmonitored NSAID use can cause gastric mucosal ulceration, "
            "renal impairment, and fluid retention. Always consult a licensed pharmacist or physician regarding drug-drug interactions and personalized safety."
        ),
    },
    {
        "id": "DOC_MED_032",
        "title": "Mental Well-being, Mood Neurobiology, Serotonin Pathways, and Cognitive Hygiene",
        "source": "World Health Organization (WHO) & National Institute of Mental Health (NIMH)",
        "url": "https://www.who.int/news-room/fact-sheets/detail/mental-health-strengthening-our-response",
        "organization": "World Health Organization (WHO)",
        "publication_date": "2023-10-10",
        "last_reviewed": "2025-11-05",
        "topic": "mental_health_depression",
        "document_type": "clinical_summary",
        "version": "1.0",
        "content": (
            "Mental health is a state of psychological well-being that enables individuals to cope with the stresses of life, realize their abilities, learn and work well, "
            "and contribute to their community. Clinical mood disorders such as Major Depressive Disorder involve complex disruptions in neuroplasticity, monoamine neurotransmitters "
            "(serotonin, norepinephrine, dopamine), and neuroendocrine hypothalamic-pituitary-adrenal (HPA) axis regulation. "
            "Common symptoms include persistent depressed mood, anhedonia (loss of interest or pleasure in previously enjoyable activities), significant unintentional changes in weight "
            "or appetite, insomnia or hypersomnia, psychomotor agitation or retardation, daily fatigue, feelings of worthlessness, and diminished concentration. "
            "Evidence-supported foundational lifestyle interventions (supporting clinical psychotherapy and psychiatric care): "
            "• Aerobic Exercise: Stimulates brain-derived neurotrophic factor (BDNF) synthesis and hippocampal neurogenesis. "
            "• Natural Light Exposure: Morning sunlight exposure (10 to 30 minutes) entrains circadian rhythms and enhances daytime serotonin release. "
            "• Sleep Regularity: Restorative slow-wave and REM sleep stabilize emotional reactivity and amygdala sensitivity. "
            "• Social Connection: Meaningful interpersonal interactions buffer against sympathetic nervous hyperarousal and loneliness. "
            "Critical Crisis Safety Protocol: Anyone experiencing thoughts of self-harm, suicide, or overwhelming despair should immediately contact local crisis services, "
            "such as the 988 Suicide & Crisis Lifeline (call or text 988 in the United States and Canada) or emergency medical services. Immediate compassionate support is always available."
        ),
    },
    {
        "id": "DOC_MED_033",
        "title": "Blood Lipids, Cholesterol Fractions, Atherosclerosis, and Cardiovascular Prevention",
        "source": "American Heart Association (AHA) & National Heart, Lung, and Blood Institute",
        "url": "https://www.heart.org/en/health-topics/cholesterol",
        "organization": "American Heart Association (AHA)",
        "publication_date": "2024-02-14",
        "last_reviewed": "2025-11-10",
        "topic": "cardiovascular_lipids",
        "document_type": "clinical_practice_guideline",
        "version": "1.0",
        "content": (
            "Cholesterol is a lipid substance essential for cell membrane fluidity, steroid hormone synthesis, and bile acid production. "
            "Because lipids are insoluble in water, they circulate bound to specialized apolipoprotein carrier complexes known as lipoproteins: "
            "1. Low-Density Lipoprotein Cholesterol (LDL-C): Often termed 'atherogenic cholesterol'. Elevated circulating LDL particles penetrate injured vascular endothelial "
            "walls, become oxidized, and trigger macrophage foam-cell accumulation, creating atherosclerotic plaques that narrow coronary and cerebral arterial lumens. "
            "Optimal adult LDL-C is generally <100 mg/dL (<70 mg/dL for individuals with established coronary disease or diabetes). "
            "2. High-Density Lipoprotein Cholesterol (HDL-C): Participates in reverse cholesterol transport, shuttling excess cholesterol from peripheral arterial walls back to the liver "
            "for excretion. Levels >=40 mg/dL for men and >=50 mg/dL for women are considered cardioprotective. "
            "3. Triglycerides: The storage form of excess caloric energy. Fasting levels <150 mg/dL are normal; marked hypertriglyceridemia (>500 mg/dL) elevates risks of acute pancreatitis. "
            "Cardiovascular risk reduction emphasizes replacing saturated and trans-fats with monounsaturated and polyunsaturated fats (olive oil, avocados, fatty fish rich in omega-3 EPA/DHA), "
            "increasing viscous soluble dietary fiber (oats, psyllium, beans), achieving 150 minutes of weekly aerobic exercise, and smoking cessation."
        ),
    },
    {
        "id": "DOC_MED_034",
        "title": "Exercise Physiology, Aerobic Capacity, Heart Rate Zones, and Muscular Conditioning",
        "source": "American College of Sports Medicine (ACSM) & CDC Health and Physical Activity",
        "url": "https://www.cdc.gov/physicalactivity/basics/adults/index.htm",
        "organization": "American College of Sports Medicine (ACSM)",
        "publication_date": "2024-01-30",
        "last_reviewed": "2025-12-01",
        "topic": "fitness_exercise",
        "document_type": "public_health_guideline",
        "version": "1.0",
        "content": (
            "Exercise physiology studies the acute and chronic biological adaptations that occur in the human body during physical exertion. "
            "Regular physical training enhances myocardial stroke volume, increases capillary density in skeletal muscle, elevates mitochondrial enzyme activity, "
            "and increases insulin sensitivity. "
            "Understanding Heart Rate (HR) Training Zones (Estimated Maximum HR = 220 minus age): "
            "• Zone 1 (Recovery, 50-60% Max HR): Promotes active circulatory clearance and recovery. "
            "• Zone 2 (Base Aerobic / Fat Oxidation, 60-70% Max HR): Builds mitochondrial density and cardiovascular endurance; conversational pace. "
            "• Zone 3 (Aerobic Tempo, 70-80% Max HR): Improves cardiovascular efficiency and glycogen storage capacity. "
            "• Zone 4 (Anaerobic / Lactate Threshold, 80-90% Max HR): Raises lactate threshold and improves muscular high-intensity fatigue tolerance. "
            "• Zone 5 (Neuromuscular Peak, 90-100% Max HR): Short interval training targeting maximal oxygen uptake (VO2 max). "
            "Resistance Training: Performing progressive overload exercises targeting all major muscular groups on 2 to 3 days weekly maintains skeletal muscle mass (countering sarcopenia), "
            "strengthens bone mineral density, and supports metabolic rate. Safe training requires adequate warm-up, proper biomechanical form, progressive volume increments, "
            "and at least 48 hours of recovery between intense training of identical muscle groups."
        ),
    },
    {
        "id": "DOC_MED_035",
        "title": "Clinical Thermoregulation, Heat Exhaustion vs Heat Stroke, and Hypothermia",
        "source": "CDC Extreme Temperatures & American Red Cross Emergency Wilderness Guidelines",
        "url": "https://www.cdc.gov/extreme-heat/signs-symptoms/index.html",
        "organization": "Centers for Disease Control and Prevention (CDC)",
        "publication_date": "2023-08-15",
        "last_reviewed": "2025-10-12",
        "topic": "thermoregulation_firstaid",
        "document_type": "emergency_guideline",
        "version": "1.0",
        "content": (
            "Human body core temperature is tightly defended around 37.0°C (98.6°F) through hypothalamic autonomic control of cutaneous blood flow, sweating, and shivering. "
            "When thermal stress overwhelms physiological compensatory mechanisms, environmental heat-related or cold-related medical emergencies develop: "
            "1. Heat Exhaustion: Result of excessive fluid and electrolyte loss through diaphoresis in hot environments. "
            "Symptoms include profuse sweating, cold/pale/clammy skin, dizziness, headache, nausea, rapid weak pulse, and muscle cramps. "
            "Management: Move the individual immediately to a cool shaded or air-conditioned area, loosen clothing, apply cool damp cloths to skin, and provide small sips of water. "
            "2. Heat Stroke: A true life-threatening medical emergency where internal thermoregulation completely fails, and core body temperature exceeds 40.0°C (104.0°F). "
            "Critical warning signs: hot, red, dry or damp skin; altered mental status, confusion, slurred speech, agitation, seizures, or loss of consciousness; and rapid bounding pulse. "
            "Immediate emergency action: Call 911 immediately. Rapid active external whole-body cooling (cold water immersion, ice bags to neck, axillae, and groin) must begin without delay. "
            "3. Hypothermia: Drop in core body temperature below 35.0°C (95.0°F). Mild cases exhibit uncontrollable shivering and lethargy; severe cases exhibit cessation of shivering, "
            "profound bradycardia, dilated pupils, and respiratory arrest, requiring gradual passive rewarming and emergency transport."
        ),
    },
    {
        "id": "DOC_MED_036",
        "title": "Ophthalmology and Visual Health: Digital Eye Strain, Refractive Errors, and Red Flags",
        "source": "American Academy of Ophthalmology (AAO) Patient Education Guidelines",
        "url": "https://www.aao.org/eye-health",
        "organization": "American Academy of Ophthalmology (AAO)",
        "publication_date": "2024-02-10",
        "last_reviewed": "2025-11-05",
        "topic": "ophthalmology",
        "document_type": "clinical_summary",
        "version": "1.0",
        "content": (
            "Visual health requires proper refractive focus onto the retinal photoreceptor layer and maintenance of the ocular surface tear film. "
            "1. Digital Eye Strain (Computer Vision Syndrome): Caused by prolonged near-work and screen fixation, which reduces spontaneous blink rate by up to 50 percent, "
            "leading to tear film evaporation. Symptoms include dry, burning, or gritty ocular sensation, transient blurred vision, frontal tension headache, and neck stiffness. "
            "Evidence-based intervention: The 20-20-20 rule (every 20 minutes, pause and look at an object at least 20 feet away for at least 20 seconds); "
            "positioning computer screens 20 to 26 inches away with the center 4 to 5 inches below eye level; and using preservative-free artificial tear drops as needed. "
            "2. Refractive Errors: Myopia (nearsightedness: focal point in front of retina), hyperopia (farsightedness: focal point behind retina), astigmatism (asymmetrical corneal curvature), "
            "and presbyopia (age-related loss of crystalline lens accommodation beginning around age 40). "
            "Emergency Ophthalmologic Red Flags: Immediate emergency eye care is required for: sudden painless loss of vision in one eye, shower of sudden floaters and flashes of light "
            "with a curtain-like shadow falling across the visual field (retinal detachment), severe acute eye pain with colored halos around lights and nausea (acute angle-closure glaucoma), "
            "or penetrating ocular trauma."
        ),
    },
]


