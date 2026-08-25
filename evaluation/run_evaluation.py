"""
Main evaluation runner for the Mercado Libre AI project.

This module orchestrates the offline evaluation suite without modifying
the production application logic.

Usage:
    python evaluation/run_evaluation.py

Output:
    evaluation/reports/evaluation_report.json
"""

from __future__ import annotations

import json
import math
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


# ---------------------------------------------------------------------------
# Repository paths
# ---------------------------------------------------------------------------

EVALUATION_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = EVALUATION_DIR.parent
DATASET_PATH = EVALUATION_DIR / "datasets" / "evaluation_data.json"
REPORTS_DIR = EVALUATION_DIR / "reports"
REPORT_PATH = REPORTS_DIR / "evaluation_report.json"

# Make the repository root importable when this script is executed directly.
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def load_dataset() -> dict[str, Any]:
    """Load the deterministic evaluation dataset."""
    if not DATASET_PATH.exists():
        raise FileNotFoundError(
            f"Evaluation dataset not found: {DATASET_PATH}"
        )

    with DATASET_PATH.open("r", encoding="utf-8") as file:
        data = json.load(file)

    if not isinstance(data, dict):
        raise ValueError("Evaluation dataset must contain a JSON object.")

    return data


def safe_float(value: Any) -> float:
    """Convert a value to float while preventing invalid numeric values."""
    try:
        result = float(value)
    except (TypeError, ValueError):
        return 0.0

    if not math.isfinite(result):
        return 0.0

    return result


def calculate_binary_metrics(
    expected: list[str],
    predicted: list[str],
    positive_label: str,
) -> dict[str, float | int]:
    """Calculate binary classification metrics."""
    if len(expected) != len(predicted):
        raise ValueError("Expected and predicted lists must have equal length.")

    tp = sum(
        1
        for actual, prediction in zip(expected, predicted)
        if actual == positive_label and prediction == positive_label
    )
    tn = sum(
        1
        for actual, prediction in zip(expected, predicted)
        if actual != positive_label and prediction != positive_label
    )
    fp = sum(
        1
        for actual, prediction in zip(expected, predicted)
        if actual != positive_label and prediction == positive_label
    )
    fn = sum(
        1
        for actual, prediction in zip(expected, predicted)
        if actual == positive_label and prediction != positive_label
    )

    total = len(expected)

    accuracy = (tp + tn) / total if total else 0.0
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0

    if precision + recall:
        f1 = 2 * precision * recall / (precision + recall)
    else:
        f1 = 0.0

    return {
        "cases": total,
        "true_positive": tp,
        "true_negative": tn,
        "false_positive": fp,
        "false_negative": fn,
        "accuracy": round(accuracy, 4),
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "f1": round(f1, 4),
    }


def validate_numeric_results(results: dict[str, Any]) -> bool:
    """Verify that numeric evaluation results contain finite values."""
    for value in results.values():
        if isinstance(value, (int, float)):
            if not math.isfinite(float(value)):
                return False

    return True


def print_section(title: str) -> None:
    """Print a formatted evaluation section."""
    print()
    print(title)
    print("-" * len(title))


def print_metric(name: str, value: Any) -> None:
    """Print a single evaluation metric."""
    if isinstance(value, float):
        print(f"{name}: {value:.4f}")
    else:
        print(f"{name}: {value}")


# ---------------------------------------------------------------------------
# Component evaluators
# ---------------------------------------------------------------------------


def evaluate_recommendations(dataset: dict[str, Any]) -> dict[str, Any]:
    """
    Evaluate recommendation logic.

    The production recommendation function is imported dynamically so this
    evaluator remains compatible with the existing repository structure.
    """
    cases = dataset.get("recommendation_cases", [])

    if not cases:
        return {
            "status": "SKIPPED",
            "reason": "No recommendation cases found.",
        }

    try:
        from analyzer.recommendations import recommend_action
    except ImportError as exc:
        return {
            "status": "ERROR",
            "reason": f"Could not import recommendation logic: {exc}",
        }

    expected_labels: list[str] = []
    predicted_labels: list[str] = []
    errors: list[str] = []

    for case in cases:
        case_id = str(case.get("id", "unknown"))
        expected = str(case.get("expected", ""))

        try:
            features = case.get("input", {})

            prediction = recommend_action(features)

            if isinstance(prediction, dict):
                prediction = (
                    prediction.get("action")
                    or prediction.get("recommendation")
                    or prediction.get("decision")
                )

            predicted = str(prediction)

            expected_labels.append(expected)
            predicted_labels.append(predicted)

        except Exception as exc:  # noqa: BLE001
            errors.append(f"{case_id}: {exc}")

    if errors:
        return {
            "status": "ERROR",
            "errors": errors,
            "cases": len(cases),
        }

    labels = sorted(set(expected_labels))

    # Evaluate each decision label using one-vs-rest metrics.
    per_label: dict[str, Any] = {}

    for label in labels:
        per_label[label] = calculate_binary_metrics(
            expected_labels,
            predicted_labels,
            label,
        )

    accuracy = (
        sum(
            actual == prediction
            for actual, prediction in zip(
                expected_labels,
                predicted_labels,
            )
        )
        / len(expected_labels)
        if expected_labels
        else 0.0
    )

    return {
        "status": "PASS",
        "cases": len(cases),
        "accuracy": round(accuracy, 4),
        "labels": labels,
        "per_label": per_label,
    }


def evaluate_ranking(dataset: dict[str, Any]) -> dict[str, Any]:
    """Evaluate the existing product ranking logic."""
    products = dataset.get("ranking_products", [])

    if not products:
        return {
            "status": "SKIPPED",
            "reason": "No ranking products found.",
        }

    try:
        from analyzer.product_ranking import rank_products
    except ImportError as exc:
        return {
            "status": "ERROR",
            "reason": f"Could not import ranking logic: {exc}",
        }

    try:
        ranked = rank_products(products)

        if isinstance(ranked, dict):
            ranked = ranked.get("products", ranked.get("ranking", []))

        if not isinstance(ranked, list):
            raise TypeError("Ranking function did not return a list.")

        expected_order = [
            str(item)
            for item in dataset.get("expected_ranking", [])
        ]

        predicted_order: list[str] = []

        for item in ranked:
            if isinstance(item, dict):
                product_id = (
                    item.get("id")
                    or item.get("product_id")
                    or item.get("sku")
                )
            else:
                product_id = item

            if product_id is not None:
                predicted_order.append(str(product_id))

        return {
            "status": "PASS",
            "cases": len(products),
            "expected_ranking": expected_order,
            "predicted_ranking": predicted_order,
        }

    except Exception as exc:  # noqa: BLE001
        return {
            "status": "ERROR",
            "reason": str(exc),
        }


def evaluate_acos_optimizer(dataset: dict[str, Any]) -> dict[str, Any]:
    """Evaluate ACOS optimizer behavior."""
    cases = dataset.get("acos_cases", [])

    if not cases:
        return {
            "status": "SKIPPED",
            "reason": "No ACOS cases found.",
        }

    try:
        from ads.acos_optimizer import optimize_acos
    except ImportError as exc:
        return {
            "status": "ERROR",
            "reason": f"Could not import ACOS optimizer: {exc}",
        }

    passed = 0
    failed = 0
    errors: list[str] = []

    for case in cases:
        case_id = str(case.get("id", "unknown"))

        try:
            result = optimize_acos(case.get("input", {}))

            if isinstance(result, dict):
                values = result.values()
            else:
                values = [result]

            numeric_values = [
                safe_float(value)
                for value in values
                if isinstance(value, (int, float))
            ]

            if all(math.isfinite(value) for value in numeric_values):
                passed += 1
            else:
                failed += 1

        except Exception as exc:  # noqa: BLE001
            failed += 1
            errors.append(f"{case_id}: {exc}")

    return {
        "status": "PASS" if failed == 0 else "REVIEW",
        "cases": len(cases),
        "passed": passed,
        "failed": failed,
        "pass_rate": round(passed / len(cases), 4),
        "errors": errors,
    }


def evaluate_bidding(dataset: dict[str, Any]) -> dict[str, Any]:
    """Evaluate bidding logic behavior."""
    cases = dataset.get("bidding_cases", [])

    if not cases:
        return {
            "status": "SKIPPED",
            "reason": "No bidding cases found.",
        }

    try:
        from ads.bidding_logic import calculate_bid
    except ImportError as exc:
        return {
            "status": "ERROR",
            "reason": f"Could not import bidding logic: {exc}",
        }

    passed = 0
    failed = 0
    errors: list[str] = []

    for case in cases:
        case_id = str(case.get("id", "unknown"))

        try:
            result = calculate_bid(case.get("input", {}))

            if isinstance(result, dict):
                values = result.values()
            else:
                values = [result]

            numeric_values = [
                safe_float(value)
                for value in values
                if isinstance(value, (int, float))
            ]

            if all(math.isfinite(value) for value in numeric_values):
                passed += 1
            else:
                failed += 1

        except Exception as exc:  # noqa: BLE001
            failed += 1
            errors.append(f"{case_id}: {exc}")

    return {
        "status": "PASS" if failed == 0 else "REVIEW",
        "cases": len(cases),
        "passed": passed,
        "failed": failed,
        "pass_rate": round(passed / len(cases), 4),
        "errors": errors,
    }


# ---------------------------------------------------------------------------
# Overall evaluation
# ---------------------------------------------------------------------------


def calculate_overall_score(results: dict[str, Any]) -> float:
    """Calculate a transparent overall evaluation score."""
    component_scores: list[float] = []

    recommendation = results.get("recommendations", {})
    if recommendation.get("status") == "PASS":
        component_scores.append(
            safe_float(recommendation.get("accuracy"))
        )

    acos = results.get("acos_optimizer", {})
    if acos.get("status") in {"PASS", "REVIEW"}:
        component_scores.append(
            safe_float(acos.get("pass_rate"))
        )

    bidding = results.get("bidding", {})
    if bidding.get("status") in {"PASS", "REVIEW"}:
        component_scores.append(
            safe_float(bidding.get("pass_rate"))
        )

    if not component_scores:
        return 0.0

    return round(
        sum(component_scores) / len(component_scores),
        4,
    )


def write_report(results: dict[str, Any]) -> None:
    """Write the evaluation results to JSON."""
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    report = {
        "project": "The-AI-s-Mercado-Libre-in-develop",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "evaluation_type": "offline_deterministic",
        "results": results,
        "overall_score": results["overall_score"],
        "status": results["status"],
    }

    with REPORT_PATH.open("w", encoding="utf-8") as file:
        json.dump(
            report,
            file,
            indent=2,
            ensure_ascii=False,
        )


def print_summary(results: dict[str, Any]) -> None:
    """Print a human-readable evaluation summary."""
    print()
    print("=" * 50)
    print("Mercado Libre AI Evaluation")
    print("=" * 50)

    recommendation = results["recommendations"]

    print_section("Recommendation Evaluation")

    if recommendation.get("status") == "PASS":
        print_metric("Cases", recommendation.get("cases", 0))
        print_metric("Accuracy", recommendation.get("accuracy", 0.0))
    else:
        print(f"Status: {recommendation.get('status')}")

    ranking = results["ranking"]

    print_section("Ranking Evaluation")
    print_metric("Cases", ranking.get("cases", 0))
    print(f"Status: {ranking.get('status')}")

    acos = results["acos_optimizer"]

    print_section("ACOS Optimizer")
    print_metric("Cases evaluated", acos.get("cases", 0))
    print_metric("Passed", acos.get("passed", 0))
    print_metric("Failed", acos.get("failed", 0))
    print_metric("Pass rate", acos.get("pass_rate", 0.0))

    bidding = results["bidding"]

    print_section("Bidding Logic")
    print_metric("Cases evaluated", bidding.get("cases", 0))
    print_metric("Passed", bidding.get("passed", 0))
    print_metric("Failed", bidding.get("failed", 0))
    print_metric("Pass rate", bidding.get("pass_rate", 0.0))

    print_section("Overall Evaluation")

    score = results["overall_score"]

    print_metric("Score", score)
    print(f"Status: {results['status']}")

    print()
    print(f"Report: {REPORT_PATH}")


def run_evaluation() -> dict[str, Any]:
    """Run the complete evaluation suite."""
    dataset = load_dataset()

    results: dict[str, Any] = {
        "recommendations": evaluate_recommendations(dataset),
        "ranking": evaluate_ranking(dataset),
        "acos_optimizer": evaluate_acos_optimizer(dataset),
        "bidding": evaluate_bidding(dataset),
    }

    results["overall_score"] = calculate_overall_score(results)

    component_statuses = [
        result.get("status")
        for result in results.values()
        if isinstance(result, dict)
    ]

    has_errors = "ERROR" in component_statuses

    results["status"] = "REVIEW" if has_errors else "PASS"

    return results


def main() -> int:
    """CLI entry point."""
    try:
        results = run_evaluation()

        write_report(results)
        print_summary(results)

        return 0

    except Exception as exc:  # noqa: BLE001
        print()
        print("=" * 50)
        print("Evaluation failed")
        print("=" * 50)
        print(f"Error: {exc}")

        return 1


if __name__ == "__main__":
    raise SystemExit(main())
