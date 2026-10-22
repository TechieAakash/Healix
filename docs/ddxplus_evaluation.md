# DDXPlus Naive Bayes Benchmark

This is a reproducible, standard-library multinomial Naive Bayes baseline over synthetic evidence-code cases. It is for coursework evaluation only, not diagnosis, treatment, or live triage. DDXPlus cases are synthetic and may not represent real-world prevalence or clinical populations.

Training records: 1,025,602; independent test records: 134,529; labels: 49.

| Metric | Score |
|---|---:|
| Top-1 accuracy | 0.9971 |
| Top-3 accuracy | 1.0000 |
| Top-5 accuracy | 1.0000 |
| Macro recall | 0.9961 |
| Macro F1 | 0.9966 |

Reproduce by obtaining the English DDXPlus train and test archives and running the command documented in `scripts/train_ddxplus_nb.py`. Dataset: [DDXPlus repository](https://github.com/mila-iqia/ddxplus) (CC BY 4.0). Model: value-specific evidence codes, five age buckets, and sex feature; additive smoothing α=0.25.
