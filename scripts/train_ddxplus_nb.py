"""Train and evaluate a dependency-free DDXPlus evidence-code baseline.

Usage:
  python scripts/train_ddxplus_nb.py --train /path/train.zip --test /path/test.zip \
      --model data/models/ddxplus_nb.json --report docs/ddxplus_evaluation.md

The model is an educational benchmark only. It predicts synthetic dataset
labels and must never be used to diagnose or triage a real person.
"""
import argparse
import ast
import csv
import json
import math
import os
import zipfile
from collections import Counter, defaultdict


def rows_from_zip(path):
    with zipfile.ZipFile(path) as archive:
        name = next(n for n in archive.namelist() if not n.endswith("/"))
        with archive.open(name) as raw:
            import io
            stream = io.TextIOWrapper(raw, encoding="utf-8")
            yield from csv.DictReader(stream)


def features(row):
    values = set()
    for code in ast.literal_eval(row["EVIDENCES"]):
        # Retain value-specific evidence as the dataset encodes it.
        values.add(str(code))
    try:
        age = float(row.get("AGE", 0))
        values.add("AGE_0_5" if age < 6 else "AGE_6_17" if age < 18 else "AGE_18_39" if age < 40 else "AGE_40_64" if age < 65 else "AGE_65_PLUS")
    except (TypeError, ValueError):
        pass
    sex = row.get("SEX", "").strip().upper()
    if sex:
        values.add("SEX_" + sex)
    return values


def train(path):
    class_counts, token_counts, totals = Counter(), defaultdict(Counter), Counter()
    n = 0
    for row in rows_from_zip(path):
        label = row["PATHOLOGY"]
        class_counts[label] += 1
        for token in features(row):
            token_counts[label][token] += 1
            totals[label] += 1
        n += 1
    vocabulary = sorted({token for counts in token_counts.values() for token in counts})
    return {"classes": dict(class_counts), "token_counts": {k: dict(v) for k, v in token_counts.items()}, "token_totals": dict(totals), "vocabulary": vocabulary, "training_rows": n}


def rank(model, row, alpha=0.25):
    vocab_size = max(1, len(model["vocabulary"]))
    present = features(row)
    scores = {}
    n = model["training_rows"]
    for label, prior_count in model["classes"].items():
        counts = model["token_counts"][label]
        denom = model["token_totals"][label] + alpha * vocab_size
        score = math.log(prior_count / n)
        for token in present:
            score += math.log((counts.get(token, 0) + alpha) / denom)
        scores[label] = score
    return sorted(scores, key=scores.get, reverse=True)


def evaluate(model, path):
    top_hits = [0, 0, 0]
    tp, fp, fn = Counter(), Counter(), Counter()
    n = 0
    for row in rows_from_zip(path):
        actual = row["PATHOLOGY"]
        predicted = rank(model, row)
        n += 1
        for idx, k in enumerate((1, 3, 5)):
            top_hits[idx] += actual in predicted[:k]
        best = predicted[0]
        if best == actual:
            tp[actual] += 1
        else:
            fp[best] += 1
            fn[actual] += 1
    classes = model["classes"]
    macro_f1_values = []
    macro_recall_values = []
    for label in classes:
        recall = tp[label] / max(1, tp[label] + fn[label])
        precision = tp[label] / max(1, tp[label] + fp[label])
        macro_recall_values.append(recall)
        macro_f1_values.append(2 * precision * recall / max(1e-12, precision + recall))
    return {
        "test_rows": n,
        "classes": len(classes),
        "top_1_accuracy": top_hits[0] / max(1, n),
        "top_3_accuracy": top_hits[1] / max(1, n),
        "top_5_accuracy": top_hits[2] / max(1, n),
        "macro_recall": sum(macro_recall_values) / len(macro_recall_values),
        "macro_f1": sum(macro_f1_values) / len(macro_f1_values),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--train", required=True)
    parser.add_argument("--test", required=True)
    parser.add_argument("--model", default="data/models/ddxplus_nb.json")
    parser.add_argument("--report", default="docs/ddxplus_evaluation.md")
    args = parser.parse_args()
    model = train(args.train)
    metrics = evaluate(model, args.test)
    os.makedirs(os.path.dirname(args.model), exist_ok=True)
    with open(args.model, "w", encoding="utf-8") as f:
        json.dump(model, f, separators=(",", ":"))
    os.makedirs(os.path.dirname(args.report), exist_ok=True)
    with open(args.report, "w", encoding="utf-8") as f:
        f.write("# DDXPlus Naive Bayes Benchmark\n\n")
        f.write("This is a reproducible, standard-library multinomial Naive Bayes baseline over synthetic evidence-code cases. It is for coursework evaluation only, not diagnosis, treatment, or live triage. DDXPlus cases are synthetic and may not represent real-world prevalence or clinical populations.\n\n")
        f.write(f"Training records: {model['training_rows']:,}; independent test records: {metrics['test_rows']:,}; labels: {metrics['classes']}.\n\n")
        f.write("| Metric | Score |\n|---|---:|\n")
        for key, label in [("top_1_accuracy", "Top-1 accuracy"), ("top_3_accuracy", "Top-3 accuracy"), ("top_5_accuracy", "Top-5 accuracy"), ("macro_recall", "Macro recall"), ("macro_f1", "Macro F1")]:
            f.write(f"| {label} | {metrics[key]:.4f} |\n")
        f.write("\nReproduce by obtaining the English DDXPlus train and test archives and running the command documented in `scripts/train_ddxplus_nb.py`. Dataset: [DDXPlus repository](https://github.com/mila-iqia/ddxplus) (CC BY 4.0). Model: value-specific evidence codes, five age buckets, and sex feature; additive smoothing α=0.25.\n")
    print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    main()
