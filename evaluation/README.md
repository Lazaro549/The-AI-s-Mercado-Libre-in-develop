# Evaluation

This directory contains a reproducible, offline evaluation suite for the Mercado Libre advertising analysis and optimization engine.

The evaluation focuses on the quality and consistency of the repository's existing decision logic rather than benchmarking a trained machine learning model.

---

## Objectives

The evaluation measures the behavior of the existing system across four main areas:

1. Recommendation quality
2. Product ranking quality
3. ACOS optimization behavior
4. Bidding recommendation behavior

It also evaluates robustness against common edge cases.

The evaluation is deterministic and does not require Mercado Libre API credentials, network access, or production advertising data.

---

## Evaluation Structure

```text
evaluation/
├── README.md
├── run_evaluation.py
├── datasets/
│   └── evaluation_data.json
├── metrics/
│   ├── __init__.py
│   ├── recommendation_metrics.py
│   └── ranking_metrics.py
└── reports/
    ├── .gitkeep
    └── evaluation_report.json
