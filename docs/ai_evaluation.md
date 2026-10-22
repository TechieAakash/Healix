# Healix AI Refactor Evaluation

All DDXPlus metrics below are evaluations on synthetic patient records. They do not measure clinical accuracy or real-world safety.

## Existing multinomial benchmark on the official split

Train rows: 1,025,602; test rows: 134,529; pathologies: 49.

| Metric | Value |
|---|---:|
| Top-1 | 0.9971 |
| Top-3 | 1.0000 |
| Top-5 | 1.0000 |
| Macro recall | 0.9961 |
| Macro F1 | 0.9966 |

## Split overlap and mapped-evidence evaluation

4,901 test rows (3.64%) share an exact age/sex/evidence signature with training. There is no patient ID, so this is a signature audit, not a patient-level leak claim. On unique test signatures absent from training, the full-feature baseline top-1 is 0.9970 across 129,439 signatures.

The live mapper deliberately supports only explicitly curated evidence and often abstains; it does not claim the official full-feature benchmark score.

| Evidence count | Cases | Top-1 | Top-3 |
|---:|---:|---:|---:|
| 1 | 408 | 0.2353 | 0.6495 |
| 2 | 645 | 0.3597 | 0.9194 |
| 3 | 1229 | 0.5972 | 0.9203 |
| 4 | 1494 | 0.6747 | 0.9284 |
| 5 | 1851 | 0.8244 | 0.9708 |
| all | 12170 | 0.8209 | 0.9616 |

Calibration temperature and abstention thresholds are in `data/models/ddxplus_calibration.json`; validation calibration uses curated evidence only and excludes exact validation signatures shared with training in the reported protocol. The raw DDXPlus case files have no patient IDs; all reported probabilities are pattern-match scores on synthetic data.

On this mapped test sample, the calibrated policy accepted 10,764/11,117 cases with at least 3 mapped evidence codes; accepted top-1 was 0.8918. It abstained on the remainder.

Validation cases with at least 3 mapped evidence codes: coverage 93.12%, top-1 0.8763, ECE 0.0186, top-label Brier 0.0522. The selected confidence floor accepted 10,443/11,568 validation cases at a 0.30 minimum top score, with accepted top-1 0.8981.

### Model and fuzzy-input definition

The ranker is a Naive Bayes network with one condition node and one conditionally independent Bernoulli child per mapped evidence code: `P(condition | evidence) ∝ P(condition) × product P(evidence_i | condition)`. It adds only observed positive evidence; absent or unknown facts are not negative likelihoods. Each result includes the log-likelihood contribution from every mapped feature. Temperature scaling is fit on validation data; the report's ECE and top-label Brier score summarize calibration.

Pain severity words map to DDXPlus E_56 values with normalized triangular memberships centered at mild=3, moderate=5, significant=6, severe=8, and extreme=10 (radius 2 for centers below 10, radius 1 at 10). Numeric scores are clamped to [0,10] and linearly interpolated between adjacent integer values. Duration phrases map to fuzzy `recent`, `ongoing`, or `prolonged` context grades only; DDXPlus has no general duration evidence, so duration never changes model likelihood or urgency.

### Controlled evidence deletion

| Evidence deleted | Cases retained | Top-1 |
|---:|---:|---:|
| 0% | 12170 | 0.8209 |
| 10% | 12170 | 0.7916 |
| 25% | 12170 | 0.7410 |
| 50% | 12170 | 0.6380 |

## Question search comparison

| Method | Cases | Mean questions | Top-1 after up to 5 questions | Confident coverage |
|---|---:|---:|---:|---:|
| greedy | 282 | 2.13 | 0.4539 | 30.85% |
| best_first_two_step | 282 | 2.29 | 0.4752 | 29.08% |

The simulator assumes an unlisted synthetic binary evidence is a No answer for search branches only. The live ranker omits unknown evidence and does not treat absent data as negative. Best-first is the live default: it produced higher top-1 in this sampled comparison (47.52% vs 45.39%), at the cost of 0.16 more questions on average and lower confident coverage (29.08% vs 30.85%).

## Decision-tree baseline

A hand-written ID3 tree trained on a deterministic stratified sample of 9,800 training rows and evaluated on the same 4,836 stratified test cases as the Naive Bayes comparison reached top-1 0.6900, top-3 0.8594, and top-5 0.9245; Naive Bayes top-1 on those exact cases was 0.9963. The tree has 131 nodes, a depth cap of 7, and serialized size 23,061 bytes. It remains an offline comparison baseline.

| Supplied feature count | ID3 top-1 | Naive Bayes top-1 |
|---:|---:|---:|
| 1 | 0.0310 | 0.2876 |
| 3 | 0.0604 | 0.7585 |
| 5 | 0.1001 | 0.9208 |

## Live-flow checks and limits

Curated free-text mapping checks: 5/5. Deterministic emergency recall on the explicit emergency evaluation cases: 100.00%. Mean local mapper/ranker latency over 120 samples: 0.215 ms.

**Age/sex constraint filtering:** Not applied: release_conditions.json contains symptom/antecedent lists and severity, with no hard age/sex eligibility constraints. Age/sex correlations are not treated as exclusions.

The duration phrases are represented only as fuzzy intake context. The dataset has no general symptom-duration feature, and duration is excluded from the Naive Bayes ranking and deterministic urgency score.
