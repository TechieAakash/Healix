# HEALIX — Intelligent Symptom Assessment & Clinical Guidance Platform

[![Python](https://img.shields.io/badge/Python-3.12%2B-blue.svg?logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110%2B-009688.svg?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/React-18.3-61DAFB.svg?logo=react&logoColor=black)](https://react.dev/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.4-3178C6.svg?logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind_CSS-3.4-38B2AC.svg?logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)
[![Playwright](https://img.shields.io/badge/E2E_Testing-Playwright-45ba4b.svg?logo=playwright&logoColor=white)](https://playwright.dev/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> **Understand your symptoms. Receive evidence-informed guidance. Transparent, deterministic, and audit-verified.**

---

## 1. Executive Overview

**Healix** is a full-stack, AI-assisted symptom assessment and clinical decision-support platform. It transforms ambiguous natural-language complaints into structured, audit-ready clinical observations through a **deterministic 5-valued production rule expert system** paired with an **adaptive follow-up questioning engine**.

Commercial healthcare bots often delegate critical clinical judgment to stochastic black-box Large Language Models (LLMs)—introducing severe risks of clinical hallucination, non-deterministic reasoning, and unprovable triage recommendations. **Healix solves this by enforcing a strict separation of concerns:**

1. **Deterministic Rule Engine (The Decider):** Medical inference, emergency red-flag identification, conflict resolution, and triage classification are handled by pure, mathematically provable rule logic operating over a structured clinical knowledge base.
2. **Generative AI (The Communicator):** Google Gemini is utilized strictly for natural language symptom extraction and patient-friendly narrative synthesis—always grounded within the verified facts deduced by the rule engine.

```
┌─────────────────────────────────┐       ┌─────────────────────────────────┐
│  NATURAL LANGUAGE INTAKE        │ ────► │  STRUCTURED CLINICAL PROFILE    │
│  "Severe right temple headache, │       │  Anatomy: Right Temple          │
│   throbbing, nausea, 2 days"    │       │  Onset: Gradual | Severity: 7/10│
└─────────────────────────────────┘       └─────────────────────────────────┘
                                                           │
                                                           ▼
┌─────────────────────────────────┐       ┌─────────────────────────────────┐
│  GEMINI NARRATIVE SUMMARY       │ ◄──── │  DETERMINISTIC INFERENCE ENGINE │
│  Clear, patient-friendly advice │       │  5-Valued Logic Evaluation      │
│  Grounded in verified rules     │       │  Emergency Safety Interceptor   │
│  Cryptographic SHA-256 Stamp    │       │  18+ Evidence-Based Pathways    │
└─────────────────────────────────┘       └─────────────────────────────────┘
```

---

## 2. Key Capabilities & Innovations

### 🩺 Hero Feature: Intelligent Symptom Analyzer
* **Natural-Language Extraction:** Users describe their symptoms in plain English. Healix extracts anatomical locations, duration, frequency, onset velocity, aggravating triggers, relieving factors, and associated red flags.
* **Interactive Anatomical Body Region Selector:** Targeted anatomical specificity (e.g., forehead, temples, occipital, epigastric, lower quadrants) rather than treating all symptoms generically.
* **Predefined Versioned Symptom Catalog:** Searchable clinical taxonomy spanning neurological, respiratory, gastrointestinal, musculoskeletal, and constitutional conditions.

### 🧠 Adaptive Clarifying Question Engine
* **Dynamic Follow-Up:** Evaluates currently asserted facts and queries an adaptive question bank for missing clinically discriminative properties.
* **Negation-as-Failure Semantics:** Unasked questions are tracked as `NOT_ASKED` (not falsely presumed negative).
* **Emergency Red-Flag Short-Circuit:** Priority 1000 rules detect acute clinical emergencies (e.g., Thunderclap Headache, Meningism Triad, Acute Coronary Syndrome) immediately displaying emergency dispatch guidance (`112 / 911`).

### 🔒 Audit-Verified Clinical Reports
* **SHA-256 Cryptographic Checksum:** Every generated consultation summary produces a unique cryptographic fingerprint sealing the clinical findings, verified rules, and triage level against tampering.
* **Audit QR Code & Print/PDF Formatting:** Clean, A4-styled print layout engineered for sharing with physicians during primary care consultations.

### 📈 Longitudinal Health Timeline
* **Chronological Health Log:** Tracks assessments over time with an interactive severity trend curve.
* **Ad-Hoc Health Notes:** Enables users to log intermediate observations, medication effects, and daily symptom changes.

### 👁️ Inclusive & Accessible Design
* **Dual Theme Architecture:** Fully designed **Dark** (`#090D0C` void with restrained emerald accents) and **Light** (calming, medical-grade slate-teal) modes.
* **Low-Vision & Screen-Reader Support:** 3-tier dynamic font scaling (`sm`, `base`, `lg`), high-contrast focus rings, semantic ARIA roles, and native input accessibility.

---

## 3. System Architecture

```
healix/
├── backend/
│   ├── app/
│   │   ├── api/v1/endpoints/       # REST routes (assessments, rules, symptoms, reports, timeline)
│   │   ├── clinical_engine/        # Adaptive question bank & clinical taxonomy
│   │   ├── core/                   # Security, async database engine, config
│   │   ├── db/                     # SQLAlchemy models (User, Assessment, Report, Fact, Observation)
│   │   ├── engine/                 # Core Deterministic Expert System
│   │   │   ├── facts.py            # 5-Valued Clinical Logic (TRUE, FALSE, UNKNOWN, NOT_ASKED, N/A)
│   │   │   ├── matching.py         # Negation-as-failure rule condition matcher
│   │   │   ├── forward_chaining.py # Forward inference deductive engine
│   │   │   ├── backward_chaining.py# Goal-driven diagnostic backtracking
│   │   │   ├── conflict_resolution.py # Specificity, priority, and recency arbitrator
│   │   │   ├── explainability.py   # Trace generation & rule audit logs
│   │   │   └── knowledge_base/     # 18+ Evidence-based clinical rules
│   │   ├── repositories/           # Async database repositories
│   │   ├── schemas/                # Pydantic V2 request & response schemas
│   │   └── services/               # Assessment orchestration & Gemini narrative service
│   ├── tests/                      # Pytest unit & integration test suite (16 tests)
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/             # Reusable UI widgets & symptom input forms
│   │   │   ├── Navbar.tsx          # Navigation, theme toggle, and font-scale selector
│   │   │   └── symptom-analyzer/   # NLP input, body selector, adaptive questions
│   │   ├── context/                # Theme & accessibility state provider
│   │   ├── pages/                  # Landing, Assessment, Results, Timeline, Reports, Auth
│   │   ├── services/               # REST API client
│   │   └── types/                  # TypeScript interface definitions
│   ├── test_all_features.mjs       # Headless Playwright browser end-to-end test suite
│   ├── tailwind.config.js          # Design tokens & color variables
│   └── package.json
├── docs/                           # Architectural, algorithmic & database documentation
├── docker-compose.yml              # Containerized multi-service deployment
└── start_dev.sh                    # Automated 1-click development runner
```

---

## 4. Quickstart & Local Installation

### Prerequisites
* **Python:** 3.12 or newer
* **Node.js:** v20 or newer
* **npm:** v10 or newer

### 1-Click Launch (Recommended)
Clone the repository and run the startup script:

```bash
# Clone the repository
git clone https://github.com/TechieAakash/Healix.git
cd Healix

# Make startup script executable and run
chmod +x start_dev.sh
./start_dev.sh
```

The script will automatically configure Python virtual environments, install dependencies, initialize the database schema, and launch both servers:

* **Frontend UI:** [http://127.0.0.1:5173](http://127.0.0.1:5173)
* **Backend API & OpenAPI Docs:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
* **Health Check Endpoint:** [http://127.0.0.1:8000/health](http://127.0.0.1:8000/health)

---

### Manual Setup

#### 1. Backend Service
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run pytest verification suite (16 tests)
PYTHONPATH=. pytest tests/ -v

# Start FastAPI Uvicorn server
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

#### 2. Frontend Application
```bash
cd frontend
npm install

# Typecheck and build verification
npm run build

# Start Vite dev server
npm run dev -- --host 127.0.0.1 --port 5173
```

---

### Docker Deployment
Run the complete stack with Docker Compose:

```bash
docker-compose up --build
```

---

## 5. Demo Credentials

For quick evaluation without manual registration:

| Parameter | Demo Credential |
|:---|:---|
| **Email** | `demo@healix.ai` |
| **Password** | `HealixDemo2026!` |
| **One-Click** | Click **"⚡ Fill 1-Click Demo Credentials"** on the Sign-In modal |

---

## 6. Testing & Quality Assurance

### Backend Unit & Integration Tests
Healix features full automated test coverage over rule matching, 5-valued logic truth tables, occurs-check unification, and forward-chaining clinical scenarios:

```bash
cd backend
source venv/bin/activate
PYTHONPATH=. pytest tests/ -v
```

```
============================== test session starts ==============================
tests/test_ai_lab.py::test_a_star_search_optimal PASSED                   [  6%]
tests/test_ai_lab.py::test_hill_climbing_search PASSED                    [ 12%]
tests/test_ai_lab.py::test_resolution_refutation PASSED                   [ 18%]
tests/test_ai_lab.py::test_bayesian_network_inference PASSED              [ 25%]
tests/test_ai_lab.py::test_dempster_shafer_combination PASSED             [ 31%]
tests/test_ai_lab.py::test_alpha_beta_pruning PASSED                      [ 37%]
tests/test_ai_lab.py::test_goal_stack_planning PASSED                     [ 43%]
tests/test_ai_lab.py::test_id3_decision_tree_learning PASSED              [ 50%]
tests/test_api.py::test_full_api_integration PASSED                       [ 56%]
tests/test_engine.py::test_fact_5_valued_logic PASSED                     [ 62%]
tests/test_engine.py::test_unification_algorithm_with_occurs_check PASSED  [ 68%]
tests/test_engine.py::test_conflict_resolution_priority_and_specificity PASSED [ 75%]
tests/test_engine.py::test_forward_chaining_migraine_scenario PASSED      [ 81%]
tests/test_engine.py::test_forward_chaining_emergency_red_flag_scenario PASSED [ 87%]
tests/test_engine.py::test_backward_chaining_deduces_missing_facts PASSED  [ 93%]
tests/test_engine.py::test_explainability_trace_and_graph_generation PASSED [100%]
============================== 16 passed in 0.33s ==============================
```

### End-to-End Browser Test Suite (Playwright)
An end-to-end automated browser test verifies real-world user flows in headless Chromium:

```bash
cd frontend
node test_all_features.mjs
```

```
======================================================
             HEALIX BROWSER TEST SUMMARY              
======================================================
✅ Landing Page Initial Load                  : PASSED
✅ Theme Switcher (Dark <-> Light)            : PASSED
✅ Font Scaling (Accessibility)               : PASSED
✅ How It Works Page                          : PASSED
✅ Clinical Standards Page                    : PASSED
✅ User Authentication (Login to Dashboard)   : PASSED
✅ Assessment Step 1 (Describe)               : PASSED
✅ NLP Symptom Extraction                     : PASSED
✅ Assessment Step 2 (Understand)             : PASSED
✅ Assessment Step 3 (Clarify/Adaptive Qs)    : PASSED
✅ Adaptive Question Progression              : PASSED
✅ Assessment Results (Clinical Explanations) : PASSED (Validated Rule Findings)
✅ Clinical Report Generation                 : PASSED (SHA-256 Stamp & QR)
✅ Health Timeline & Chart                    : PASSED
✅ Timeline: Log New Health Note              : PASSED
======================================================
TOTAL: 15 | PASSED: 15 | FAILED: 0
OVERALL RESULT: ALL FEATURES PASSED ✅
======================================================
```

---

## 7. Clinical & Medical Safety Disclaimer

> **IMPORTANT MEDICAL NOTICE**  
> Healix is an assistive clinical decision-support and educational health information platform. It is designed to assist users in structuring their symptoms, understanding potential clinical patterns, and preparing for professional healthcare consultations.  
>  
> **Healix does not provide formal medical diagnoses, write drug prescriptions, or replace the professional clinical judgment of a licensed physician or emergency medical provider.**  
>  
> If you or someone you are assisting is experiencing severe chest pressure, sudden numbness or weakness, difficulty speaking, severe breathing distress, sudden explosive headache, or loss of consciousness, **stop using this software immediately and contact local emergency dispatch (112, 911, or your local emergency number).**

---

## 8. License

Distributed under the MIT License. See `LICENSE` for details.
