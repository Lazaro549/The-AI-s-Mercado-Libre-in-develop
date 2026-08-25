"""Metrics for evaluating recommendation and decision outputs."""

from __future__ import annotations

from collections import Counter
from typing import Iterable


def calculate_confusion_matrix(
    y_true: Iterable[str],
    y_pred: Iterable[str],
) -> dict[str, dict[str, int]]:
    """Build a confusion matrix from expected and predicted labels.

    Args:
        y_true: Expected recommendation labels.
        y_pred: Recommendations produced by the system.

    Returns:
        Nested dictionary where rows represent expected labels and
        columns represent predicted labels.
    """
    true_labels = list(y_true)
    predicted_labels = list(y_pred)

    if len(true_labels) != len(predicted_labels):
        raise ValueError("y_true and y_pred must have the same length.")

    labels = sorted(set(true_labels) | set(predicted_labels))

    matrix = {
        actual: {predicted: 0 for predicted in labels}
        for actual in labels
    }

    for actual, predicted in zip(true_labels, predicted_labels):
        matrix[actual][predicted] += 1

    return matrix


def calculate_classification_metrics(
    y_true: Iterable[str],
    y_pred: Iterable[str],
) -> dict[str, float]:
    """Calculate accuracy, precision, recall, and F1.

    Metrics use macro averaging so every recommendation class contributes
    equally, regardless of class frequency.

    Args:
        y_true: Expected recommendation labels.
        y_pred: Recommendations produced by the system.

    Returns:
        Dictionary containing accuracy, precision, recall, and F1 score.
    """
    true_labels = list(y_true)
    predicted_labels = list(y_pred)

    if len(true_labels) != len(predicted_labels):
        raise ValueError("y_true and y_pred must have the same length.")

    if not true_labels:
        return {
            "accuracy": 0.0,
            "precision": 0.0,
            "recall": 0.0,
            "f1": 0.0,
        }

    labels = sorted(set(true_labels) | set(predicted_labels))

    correct = sum(
        actual == predicted
        for actual, predicted in zip(true_labels, predicted_labels)
    )
    accuracy = correct / len(true_labels)

    true_counts = Counter(true_labels)
    predicted_counts = Counter(predicted_labels)

    precision_scores: list[float] = []
    recall_scores: list[float] = []
    f1_scores: list[float] = []

    for label in labels:
        true_positive = sum(
            actual == label and predicted == label
            for actual, predicted in zip(true_labels, predicted_labels)
        )

        false_positive = predicted_counts[label] - true_positive
        false_negative = true_counts[label] - true_positive

        precision = (
            true_positive / (true_positive + false_positive)
            if true_positive + false_positive > 0
            else 0.0
        )

        recall = (
            true_positive / (true_positive + false_negative)
            if true_positive + false_negative > 0
            else 0.0
        )

        f1 = (
            2 * precision * recall / (precision + recall)
            if precision + recall > 0
            else 0.0
        )

        precision_scores.append(precision)
        recall_scores.append(recall)
        f1_scores.append(f1)

    return {
        "accuracy": accuracy,
        "precision": sum(precision_scores) / len(precision_scores),
        "recall": sum(recall_scores) / len(recall_scores),
        "f1": sum(f1_scores) / len(f1_scores),
    }
