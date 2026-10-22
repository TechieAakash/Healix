# Healix AI Syllabus Alignment

Healix demonstrates course methods only where they perform work in the offline assessment flow or its reproducible evaluation. DDXPlus consists of synthetic records; matching metrics are coursework measurements, not evidence of clinical accuracy.

## Syllabus units

| Unit/topic | Live module or function | Test coverage | Evaluation evidence |
|---|---|---|---|
| Unit 1: intelligent systems, problem spaces, production systems | `app/services/triage_service.py`: `WorkingMemory`, `_condition_matches`, `evaluate` forward-chaining loop | `tests/test_production_system.py`, `tests/test_triage.py` | `docs/ai_evaluation.md`: emergency recall; report `reasoning_trace` records fired production rules |
| Unit 2: generate/test, hill climbing, best-first search | `app/services/clinical/question_search.py`: `greedy`, `lookahead`, `choose`; assessment asks only mapper-supported evidence questions | `tests/test_ai_refactor_features.py`; `tests/test_assessments.py` | `docs/ai_evaluation.md`: greedy vs two-step best-first mean questions, top-1, and confident coverage |
| Unit 3: knowledge representation, logic, forward/backward chaining | `app/services/clinical/symptom_ontology.py`: `ISA_PARENTS`, `ancestors`; triage rule facts, forward chaining, and `_backward_chain_questions` | `tests/test_production_system.py` | Rule trace and priority confirmation questions in assessment responses; emergency recall in evaluation |
| Unit 4: reasoning under uncertainty | `app/services/clinical/evidence_mapper.py`: curated DDXPlus mapping and fuzzy membership; `app/services/clinical/ddxplus_ranker.py`: calibrated Naive Bayes with explicit abstention | `tests/test_ai_refactor_features.py` | `docs/ai_evaluation.md`: model factorization, calibration, confidence threshold, evidence-count accuracy, noise robustness, and latency |
| Unit 5: learning, agents, NLU | `app/services/ai/evaluation/id3.py`: offline ID3 comparison; `app/services/ai/assessment_agent.py`: percept → state → action; `app/services/clinical/symptom_engine.py`: deterministic NLU | `tests/test_ai_refactor_features.py`, `tests/test_deterministic_engine.py`, `tests/test_assessments.py` | `docs/ai_evaluation.md`: ID3 and Naive Bayes comparison; curated free-text mapper cases |

## Course outcomes

| Outcome | Healix implementation | Test | Demonstration/evaluation output |
|---|---|---|---|
| CO1: distinguish conventional and intelligent systems | Compare static red-flag rule execution with stateful search/ranking and the goal-based controller | `tests/test_production_system.py`, `tests/test_ai_refactor_features.py` | Rule trace, questions selected from updated evidence, and report/abstain action |
| CO2: design searching techniques to achieve goals | Information-gain and bounded best-first question selection reduce uncertainty about dataset patterns | `tests/test_ai_refactor_features.py` | Search comparison table in evaluation report |
| CO3: analyze AI concepts and applications | Offline NB ranking, ID3, rule inference, NLU, uncertainty and safety boundaries are compared in the report | `tests/test_ai_refactor_features.py`, `tests/test_ai_evaluation.py` | Accuracy, macro metrics, calibration, coverage, noise, and latency in evaluation report |
| CO4: apply knowledge representation methods | Ontology `isa` facts, positive/negative/unknown working-memory state, rule conditions, and fired-rule traces | `tests/test_production_system.py` | “Why this was flagged” trace in the report |
| CO5: understand AI techniques for a domain | The goal agent chooses ask/report/escalate/abstain for the health-information workflow; deterministic safety always wins | `tests/test_ai_refactor_features.py`, `tests/test_assessments.py` | Emergency recall, mapper flow checks, abstention and report behavior |

## Techniques not used

- **Minimax, alpha-beta pruning, and game playing:** the symptom-intake problem has no adversarial opponent or alternating game utility.
- **Tabu search and simulated annealing:** no combinatorial optimization task in the live workflow benefits from stochastic local search; adding them would not improve a user-facing decision.
- **Dempster–Shafer combination:** not added. The simple safety-rule-wins policy has a clearer safety contract and no measured evidence justified a second urgency fusion layer.
- **Hard age/sex constraint filtering:** not added because DDXPlus condition metadata does not specify hard eligibility rules. Dataset correlations are not safe grounds for excluding conditions.
- **General duration-to-condition inference:** not added because DDXPlus has no general symptom-duration field. Duration is kept as fuzzy intake context and never enters disease likelihood or urgency.

## Runtime boundary and data attribution

The assessment runs locally in Python: deterministic safety rules, evidence mapping, optional calibrated synthetic pattern ranking, question search, and local response framing. The ID3 model and full benchmark run only in the offline evaluation script. External LLMs are not required for the main assessment features.

The benchmark uses the English [DDXPlus dataset](https://figshare.com/articles/dataset/DDXPlus_Dataset_English_/22687585) (CC BY 4.0); see the [project repository](https://github.com/mila-iqia/ddxplus) and [dataset paper](https://arxiv.org/abs/2205.09148). The dataset contains synthetic patients and no patient identifiers. Healix does not claim that synthetic benchmark accuracy measures clinical accuracy or real-world safety.
