"""Ranking metrics for evaluating product prioritization."""

from __future__ import annotations

import math
from typing import Sequence


def precision_at_k(
    ranked_items: Sequence[str],
    relevant_items: set[str],
    k: int,
) -> float:
    """Calculate Precision@K.

    Args:
        ranked_items: Items ordered by the system.
        relevant_items: Set of relevant items.
        k: Number of top-ranked items to evaluate.

    Returns:
        Fraction of the top-k items that are relevant.
    """
    if k <= 0:
        raise ValueError("k must be greater than zero.")

    if not ranked_items:
        return 0.0

    top_k = ranked_items[:k]

    if not top_k:
        return 0.0

    relevant_count = sum(item in relevant_items for item in top_k)

    return relevant_count / len(top_k)


def recall_at_k(
    ranked_items: Sequence[str],
    relevant_items: set[str],
    k: int,
) -> float:
    """Calculate Recall@K.

    Args:
        ranked_items: Items ordered by the system.
        relevant_items: Set of relevant items.
        k: Number of top-ranked items to evaluate.

    Returns:
        Fraction of all relevant items found in the top-k results.
    """
    if k <= 0:
        raise ValueError("k must be greater than zero.")

    if not relevant_items:
        return 0.0

    top_k = ranked_items[:k]
    found = sum(item in relevant_items for item in top_k)

    return found / len(relevant_items)


def ndcg_at_k(
    ranked_items: Sequence[str],
    relevance_scores: dict[str, float],
    k: int,
) -> float:
    """Calculate normalized discounted cumulative gain at K.

    Relevance scores can be binary or graded.

    Args:
        ranked_items: Items ordered by the system.
        relevance_scores: Mapping from item ID to relevance score.
        k: Number of top-ranked items to evaluate.

    Returns:
        NDCG@K in the range [0, 1].
    """
    if k <= 0:
        raise ValueError("k must be greater than zero.")

    if not relevance_scores:
        return 0.0

    top_k = ranked_items[:k]

    dcg = 0.0

    for rank, item in enumerate(top_k, start=1):
        relevance = max(0.0, relevance_scores.get(item, 0.0))
        dcg += relevance / math.log2(rank + 1)

    ideal_items = sorted(
        relevance_scores.values(),
        reverse=True,
    )[:k]

    ideal_dcg = sum(
        max(0.0, relevance) / math.log2(rank + 1)
        for rank, relevance in enumerate(ideal_items, start=1)
    )

    if ideal_dcg == 0.0:
        return 0.0

    return dcg / ideal_dcg
