"""
Offline evaluation runner for The-AI-s-Mercado-Libre-in-develop.

This module evaluates the existing production logic without modifying it.

Evaluated components:
- analyzer.diagnosis
- analyzer.recommendations
- analyzer.product_ranking
- analyzer.metrics
- ads.acos_optimizer

Bidding evaluation is reported as SKIPPED when the production API is not
implemented rather than inventing a replacement implementation.
"""

from __future__ import annotations

import json
import math
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from analyzer.diagnosis import diagnose
from analyzer.metrics import (
    calculate_acos,
    calculate_conversion_rate,
    calculate_ctr,
)
from analyzer.product_ranking import (
    calculate_score,
    classify_product,
    rank_products,
)
from analyzer.recommendations import generate_recommendations
from ads.acos_optimizer import evaluate_acos, suggest_acos_adjustment


ROOT_DIR = Path(__file__).resolve().parents[1]
DATASET_PATH = ROOT_DIR / "evaluation" / "datasets" / "evaluation_data.json"
REPORT_DIR = ROOT_DIR / "evaluation" / "reports"
REPORT_PATH = REPORT_DIR / "evaluation_report.json"


def load_dataset() -> dict[str, Any]:
    """Load the deterministic evaluation dataset."""
    if not DATASET_PATH.exists():
        raise FileNotFoundError(f"Dataset not found: {DATASET_PATH}")

    with DATASET_PATH.open("r", encoding="utf-8") as file:
        data = json.load(file)

    if not isinstance(data, dict):
        raise ValueError("Evaluation dataset must contain a JSON object.")

    return data


def safe_float(value: Any) -> float:
    """Convert a value to float and reject non-finite numbers."""
    result = float(value)

    if not math.isfinite(result):
        raise ValueError(f"Non-finite numeric value: {value}")

    return result


def evaluate_metrics(dataset: dict[str, Any]) -> dict[str, Any]:
    """Evaluate the production metric functions."""
    cases = dataset.get("metric_cases", [])

    passed = 0
    failed = 0
    results = []

    for case in cases:
        try:
            impressions = safe_float(case["impressions"])
            clicks = safe_float(case["clicks"])
            sales = safe_float(case["sales"])
            ad_spend = safe_float(case["ad_spend"])
            revenue = safe_float(case["revenue"])

            ctr = calculate_ctr(clicks, impressions)
            conversion_rate = calculate_conversion_rate(sales, clicks)
            acos = calculate_acos(ad_spend, revenue)

            expected = case.get("expected", {})

            checks = {
                "ctr": math.isclose(
                    ctr,
                    safe_float(expected["ctr"]),
                    rel_tol=1e-9,
                    abs_tol=1e-9,
                ),
                "conversion_rate": math.isclose(
                    conversion_rate,
                    safe_float(expected["conversion_rate"]),
                    rel_tol=1e-9,
                    abs_tol=1e-9,
                ),
                "acos": math.isclose(
                    acos,
                    safe_float(expected["acos"]),
                    rel_tol=1e-9,
                    abs_tol=1e-9,
                ),
            }

            case_passed = all(checks.values())

            if case_passed:
                passed += 1
            else:
                failed += 1

            results.append(
                {
                    "name": case.get("name", "unnamed"),
                    "passed": case_passed,
                    "checks": checks,
                    "actual": {
                        "ctr": ctr,
                        "conversion_rate": conversion_rate,
                        "acos": acos,
                    },
                    "expected": expected,
                }
            )

        except Exception as exc:
            failed += 1
            results.append(
                {
                    "name": case.get("name", "unnamed"),
                    "passed": False,
                    "error": str(exc),
                }
            )

    total = passed + failed

    return {
        "cases": total,
        "passed": passed,
        "failed": failed,
        "accuracy": passed / total if total else 0.0,
        "results": results,
    }


def evaluate_diagnosis(dataset: dict[str, Any]) -> dict[str, Any]:
    """Evaluate the production diagnosis function."""
    cases = dataset.get("diagnosis_cases", [])

    passed = 0
    failed = 0
    results = []

    for case in cases:
        try:
            metrics = case["metrics"]
            expected_types = set(case.get("expected_problem_types", []))

            actual_problems = diagnose(metrics)

            if not isinstance(actual_problems, list):
                raise TypeError("diagnose() must return a list.")

            actual_types = {
                problem.get("type")
                for problem in actual_problems
                if isinstance(problem, dict)
            }

            case_passed = actual_types == expected_types

            if case_passed:
                passed += 1
            else:
                failed += 1

            results.append(
                {
                    "name": case.get("name", "unnamed"),
                    "passed": case_passed,
                    "expected_problem_types": sorted(expected_types),
                    "actual_problem_types": sorted(actual_types),
                }
            )

        except Exception as exc:
            failed += 1
            results.append(
                {
                    "name": case.get("name", "unnamed"),
                    "passed": False,
                    "error": str(exc),
                }
            )

    total = passed + failed

    return {
        "cases": total,
        "passed": passed,
        "failed": failed,
        "accuracy": passed / total if total else 0.0,
        "results": results,
    }


def evaluate_recommendations(dataset: dict[str, Any]) -> dict[str, Any]:
    """Evaluate the actual generate_recommendations() API."""
    cases = dataset.get("recommendation_cases", [])

    passed = 0
    failed = 0
    results = []

    for case in cases:
        try:
            problems = case["problems"]
            expected_keywords = [
                keyword.lower()
                for keyword in case.get("expected_keywords", [])
            ]

            recommendations = generate_recommendations(problems)

            if not isinstance(recommendations, list):
                raise TypeError(
                    "generate_recommendations() must return a list."
                )

            recommendation_text = " ".join(
                str(item) for item in recommendations
            ).lower()

            checks = {
                keyword: keyword in recommendation_text
                for keyword in expected_keywords
            }

            case_passed = all(checks.values())

            if case_passed:
                passed += 1
            else:
                failed += 1

            results.append(
                {
                    "name": case.get("name", "unnamed"),
                    "passed": case_passed,
                    "checks": checks,
                    "recommendations": recommendations,
                }
            )

        except Exception as exc:
            failed += 1
            results.append(
                {
                    "name": case.get("name", "unnamed"),
                    "passed": False,
                    "error": str(exc),
                }
            )

    total = passed + failed

    return {
        "cases": total,
        "passed": passed,
        "failed": failed,
        "accuracy": passed / total if total else 0.0,
        "results": results,
    }


def evaluate_ranking(dataset: dict[str, Any]) -> dict[str, Any]:
    """Evaluate the existing product ranking implementation."""
    ranking_cases = dataset.get("ranking_cases", [])

    passed = 0
    failed = 0
    results = []

    for case in ranking_cases:
        try:
            products = case["products"]
            expected_top_ids = case.get("expected_top_ids", [])

            ranked = rank_products(products)

            actual_top_ids = [
                product.get("id")
                for product in ranked[: len(expected_top_ids)]
            ]

            case_passed = actual_top_ids == expected_top_ids

            if case_passed:
                passed += 1
            else:
                failed += 1

            results.append(
                {
                    "name": case.get("name", "unnamed"),
                    "passed": case_passed,
                    "expected_top_ids": expected_top_ids,
                    "actual_top_ids": actual_top_ids,
                }
            )

        except Exception as exc:
            failed += 1
            results.append(
                {
                    "name": case.get("name", "unnamed"),
                    "passed": False,
                    "error": str(exc),
                }
            )

    total = passed + failed

    return {
        "cases": total,
        "passed": passed,
        "failed": failed,
        "accuracy": passed / total if total else 0.0,
        "results": results,
    }


def evaluate_acos_optimizer(dataset: dict[str, Any]) -> dict[str, Any]:
    """Evaluate the actual ACOS optimizer implementation."""
    cases = dataset.get("acos_cases", [])

    passed = 0
    failed = 0
    results = []

    for case in cases:
        try:
            acos = safe_float(case["acos"])
            target = safe_float(case["target"])

            evaluation = evaluate_acos(acos, target)
            suggestions = suggest_acos_adjustment(acos, target)

            if not isinstance(evaluation, dict):
                raise TypeError("evaluate_acos() must return a dict.")

            if not isinstance(suggestions, list):
                raise TypeError(
                    "suggest_acos_adjustment() must return a list."
                )

            expected_profitable = case.get("expected_profitable")

            if expected_profitable is None:
                case_passed = True
            else:
                case_passed = (
                    evaluation.get("profitable") == expected_profitable
                )

            if case_passed:
                passed += 1
            else:
                failed += 1

            results.append(
                {
                    "name": case.get("name", "unnamed"),
                    "passed": case_passed,
                    "evaluation": evaluation,
                    "suggestions": suggestions,
                }
            )

        except Exception as exc:
            failed += 1
            results.append(
                {
                    "name": case.get("name", "unnamed"),
                    "passed": False,
                    "error": str(exc),
                }
            )

    total = passed + failed

    return {
        "cases": total,
        "passed": passed,
        "failed": failed,
        "accuracy": passed / total if total else 0.0,
        "results": results,
    }


def evaluate_bidding() -> dict[str, Any]:
    """
    Report bidding evaluation as skipped when the production API does not
    expose an implemented bidding function.

    We deliberately do not invent a calculate_bid implementation.
    """
    return {
        "status": "SKIPPED",
        "reason": (
            "No implemented calculate_bid/get_min_bid/get_max_bid "
            "production API was found in ads.bidding_logic."
        ),
        "cases": 0,
        "passed": 0,
        "failed": 0,
    }


def calculate_overall_score(
    evaluations: dict[str, dict[str, Any]],
) -> float:
    """Calculate the mean score of executed evaluation components."""
    scores = []

    for evaluation in evaluations.values():
        if evaluation.get("status") == "SKIPPED":
            continue

        if "accuracy" in evaluation:
            scores.append(float(evaluation["accuracy"]))

    if not scores:
        return 0.0

    return sum(scores) / len(scores)


def build_report(dataset: dict[str, Any]) -> dict[str, Any]:
    """Run all available evaluations and construct the report."""
    evaluations = {
        "metrics": evaluate_metrics(dataset),
        "diagnosis": evaluate_diagnosis(dataset),
        "recommendations": evaluate_recommendations(dataset),
        "ranking": evaluate_ranking(dataset),
        "acos_optimizer": evaluate_acos_optimizer(dataset),
        "bidding": evaluate_bidding(),
    }

    overall_score = calculate_overall_score(evaluations)

    executed_failures = sum(
        evaluation.get("failed", 0)
        for evaluation in evaluations.values()
        if evaluation.get("status") != "SKIPPED"
    )

    status = "PASS" if executed_failures == 0 else "REVIEW"

    return {
        "project": "The-AI-s-Mercado-Libre-in-develop",
        "evaluation_type": "offline_deterministic_evaluation",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "status": status,
        "overall_score": round(overall_score, 4),
        "evaluations": evaluations,
        "limitations": [
            "Synthetic deterministic data is used.",
            "The evaluation measures deterministic decision and optimization logic.",
            "No Mercado Libre API credentials or network access are required.",
            "Bidding is skipped because the current production module does not "
            "expose an implemented bidding API.",
        ],
    }


def write_report(report: dict[str, Any]) -> None:
    """Write the evaluation report as formatted JSON."""
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    with REPORT_PATH.open("w", encoding="utf-8") as file:
        json.dump(
            report,
            file,
            indent=2,
            ensure_ascii=False,
        )


def print_summary(report: dict[str, Any]) -> None:
    """Print a concise human-readable evaluation summary."""
    print("=" * 58)
    print("Mercado Libre AI Evaluation")
    print("=" * 58)

    for name, evaluation in report["evaluations"].items():
        print(f"\n{name.replace('_', ' ').title()}")
        print("-" * 30)

        if evaluation.get("status") == "SKIPPED":
            print("Status: SKIPPED")
            print(f"Reason: {evaluation['reason']}")
            continue

        print(f"Cases:  {evaluation.get('cases', 0)}")
        print(f"Passed: {evaluation.get('passed', 0)}")
        print(f"Failed: {evaluation.get('failed', 0)}")

        if "accuracy" in evaluation:
            print(f"Score:  {evaluation['accuracy']:.2%}")

    print("\n" + "=" * 58)
    print("Overall Evaluation")
    print("=" * 58)
    print(f"Score:  {report['overall_score']:.2%}")
    print(f"Status: {report['status']}")
    print(f"Report: {REPORT_PATH}")


def main() -> int:
    """Run the complete offline evaluation."""
    try:
        dataset = load_dataset()
        report = build_report(dataset)
        write_report(report)
        print_summary(report)

        return 0 if report["status"] == "PASS" else 1

    except Exception as exc:
        print(f"Evaluation failed: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
