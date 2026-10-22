# Healix AI Refactor Plan

## Product boundary

Healix is an offline symptom intake and safety-guidance tool. It does not diagnose, prescribe, or replace a clinician. Deterministic safety rules always control urgency and emergency escalation. Dataset models may rank educational pattern matches only; they cannot lower a safety-rule urgency. The local Python response layer may frame generic explanations, but it is not the decision authority.

Every algorithm in this plan must serve a user-facing assessment action, improve a measurable system behavior, or make the result explainable. Do not add algorithms solely to demonstrate course vocabulary. No network calls or heavy ML dependencies are introduced. DDXPlus is synthetic and its results must be labeled as such.

## Phase 0 — dataset and live-flow audit (complete)

- Inspected the checked-in DDXPlus model/training script and the locally available official English train, validation, and test archives.
- Confirmed 49 pathologies, 223 evidence codes (208 binary, 10 categorical, 5 multi-choice; 113 antecedent and 110 symptom codes), and six CSV columns.
- Found 4,901 test rows (3.64%) with an exact age/sex/evidence signature also present in train. The reproducible audit leaves 129,439 distinct train-disjoint test signatures; the full-feature baseline scores 99.70% top-1 on these synthetic signatures. This is not patient-level deduplication because the dataset contains no patient identifiers.
- Integrated a curated evidence mapper and calibrated dataset ranker into reports and question selection. Dataset output remains separate from safety urgency.

## Item 1 — knowledge representation and production system (Units 1 and 3)

**Status: implemented.**

1. Represent each existing safety rule explicitly with a stable ID, condition facts, conclusion, urgency, and source/reference label. Preserve current trigger behavior and rule IDs.
2. Build working memory from extracted/structured symptoms, severity, duration, age group and sex when known, and negated/hypothetical facts. Keep unknown facts distinct from false facts.
3. Run a deterministic forward-chaining loop until no new facts or rule firings are produced. A rule firing may add its conclusion and a trace entry; duplicate conclusions must not loop indefinitely.
4. Add a small `isa` ontology for symptom concepts and parent categories. Use it when mapping extracted concepts and when matching rule conditions so parent concepts match descendants.
5. Add goal-directed backward chaining for `EMERGENCY?`. It must identify only missing facts that could satisfy a configured red-flag rule and turn these into prioritized confirmation questions. Attach a plain-language reason to each question. Already established emergency facts bypass further intake and remain emergency.
6. Return fired-rule trace entries with the assessment result and persisted report, including rule ID, matched facts, conclusion, urgency, and source/reference. Show the trace as a concise “Why this was flagged” section in the report UI.
7. Verify existing triage behavior, negation/hypothetical handling, ontology inheritance, forward chaining, backward-chaining questions and trace persistence with focused tests; then run the complete suite.

## Item 2 — uncertainty and dataset evidence (Unit 4)

**Status: complete.**

1. Implement an offline evidence mapper from supported Healix symptom concepts and answers to DDXPlus evidence codes. Keep unsupported inputs explicitly unmapped; do not guess evidence values.
2. Define and document bounded fuzzy membership functions for severity language and duration phrases. Use grades only where the mapper can justify the corresponding dataset values. Keep safety-rule urgency deterministic and independent of these grades.
3. Document the Naive Bayes model as a single condition variable with conditionally independent evidence features. Return ranked synthetic-data matches, per-evidence log-likelihood contributions, calibrated confidence bands only if calibration supports them, and an explicit abstain result when evidence is insufficient or out of distribution.
4. Recompute rankings when answers or negations change. Safety rules always override and cannot be retracted by model output.
5. Evaluate split performance and a deduplicated/group-aware comparison, top-k accuracy, class-balanced metrics, calibration, evidence-count robustness, controlled noise, and latency. Explain that shared signatures exist across the supplied splits and avoid presenting random-row performance as clinical validity.
6. Test answer-driven rank changes, abstention, calibration/threshold behavior, and locked safety overrides. Keep Dempster–Shafer out unless a real product decision benefits from it and an evaluation shows value over the simpler safety-rule-wins policy.

## Item 3 — question selection as search (Unit 2)

**Status: complete.**

1. Model the intake state as known DDXPlus evidence and legal question/answer transitions. Ask only questions that Healix can explain and use in the mapper/ranking path.
2. Compare greedy information gain (hill climbing) with bounded best-first/A*-style lookahead using question cost and expected remaining uncertainty. Evaluate questions-to-confident-ranking and ranking accuracy on held-out synthetic cases; ship one default only if it improves the measured tradeoff.
3. Before adding age/sex constraint filtering, inspect DDXPlus condition metadata and evidence distributions for actual hard eligibility constraints. Add CSP filtering only when the data supports it; otherwise document the result and do not infer exclusions from correlations.
4. Test candidate transitions, question limits, deterministic tie-breaking, and safety-first early exit.

## Item 4 — learning and goal-based agent (Unit 5)

**Status: complete.**

1. Add a small decision-tree baseline using an already-approved dependency or a compact hand-written ID3 implementation. Compare it with Naive Bayes on the same patient cases and split. Report accuracy, macro metrics, robustness at reduced evidence counts, interpretability, and artifact size.
2. Keep model training/evaluation reproducible and offline; do not add a runtime training dependency or put a model in charge of urgency.
3. Make the orchestration loop explicit: percept (description, structured symptoms, answers) → state update (positive/negative/unknown facts) → action selection (ask, stop/report, escalate, or abstain). Use the existing deterministic parser and local response framing where appropriate.
4. Test each action, transition, safety override, and dataset boundary.

## Item 5 — evaluation, syllabus mapping, and docs

**Status: complete.**

1. Complete the evaluation suite: supplied-split and deduplicated/group-aware accuracy, top-k and macro metrics, robustness with k evidences, controlled evidence noise, end-to-end free-text flow, emergency recall, calibration/abstention, and latency. Keep synthetic benchmark performance separate from real-world safety claims.
2. Create `docs/SYLLABUS_ALIGNMENT.md` mapping Units 1–5 and CO1–CO5 to concrete modules/functions, tests, and evaluation outputs. List intentionally unused topics and why they do not serve Healix (for example, minimax/game playing and tabu search).
3. Add a concise “AI techniques used” README section linking to the syllabus map and explaining what runs in the live assessment path versus offline evaluation.
4. Run the complete backend suite and frontend build after the final integration; summarize limitations and measured results.

## Completion status

The project owner authorized implementation through Items 2–5 in one continuation, so the earlier stop-after-each-item checkpoints no longer apply. Items 1–5 and the final offline evaluation are complete. Limitations remain explicit: synthetic-data performance is not clinical accuracy, unknown evidence remains unknown, and dataset outputs cannot override safety rules.
