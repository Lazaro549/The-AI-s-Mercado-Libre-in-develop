"""
Pytest test suite for the :mod:`analyzer.recommendations` module.

The tests are intentionally generic: they do not depend on the internal
implementation details or specific constant values.  They instead verify
that the public recommendation function behaves consistently across
different performance scenarios and correctly handles edge cases such as
insufficient data or zero metrics.

The test suite dynamically discovers the recommendation function in the
module, allowing it to adapt to different function names without
requiring modifications to the production code.
"""

import inspect
from typing import Any

import pandas as pd
import pytest

import analyzer.recommendations as rec_mod


def _find_recommendation_function() -> Any:
    """
    Locate the recommendation function in :mod:`analyzer.recommendations`.

    The function is expected to accept a :class:`pandas.DataFrame` (or a
    compatible input) and return a recommendation as a string or dictionary.
    """
    candidate_names = [
        "recommend",
        "get_recommendation",
        "evaluate_performance",
        "recommendation",
        "recommendation_for_product",
    ]
    for name in candidate_names:
        if hasattr(rec_mod, name):
            return getattr(rec_mod, name)
    raise RuntimeError(
        "Could not locate the recommendation function in "
        "analyzer.recommendations.  Expected one of: "
        f"{', '.join(candidate_names)}"
    )


# Global reference to the recommendation function
RECOMMEND_FUNC = _find_recommendation_function()


@pytest.fixture
def sample_df() -> pd.DataFrame:
    """
    Return a minimal dataframe used for testing.

    The dataframe contains the most common metrics that the
    recommendation logic relies on.  The exact column names are not
    critical; the tests simply need to provide a dataframe that
    mimics realistic input.
    """
    return pd.DataFrame(
        [
            {
                "sales_volume": 100,
                "conversion_rate": 0.05,
                "average_price": 150.0,
                "inventory_level": 50,
            }
        ]
    )


def _call_recommender(df: pd.DataFrame) -> Any:
    """
    Helper that calls the recommendation function with the provided ``df``.
    """
    try:
        return RECOMMEND_FUNC(df)
    except TypeError as exc:
        # If the function expects additional arguments, try supplying
        # dummy values for the remaining parameters.
        sig = inspect.signature(RECOMMEND_FUNC)
        params = list(sig.parameters.values())
        if len(params) > 1:
            # Build a tuple of dummy arguments (None) for the remaining
            # parameters.  The first argument is always the dataframe.
            dummy_args = [df] + [None] * (len(params) - 1)
            return RECOMMEND_FUNC(*dummy_args)
        raise exc


@pytest.mark.parametrize(
    "metrics,expected_keywords",
    [
        # Strong performance: high sales and conversion, sufficient inventory
        (
            {
                "sales_volume": 1000,
                "conversion_rate": 0.1,
                "average_price": 200.0,
                "inventory_level": 200,
            },
            {"increase", "maintain", "strong", "optimal"},
        ),
        # Weak performance: low sales and conversion, inventory low
        (
            {
                "sales_volume": 10,
                "conversion_rate": 0.01,
                "average_price": 200.0,
                "inventory_level": 5,
            },
            {"decrease", "promo", "weak", "low"},
        ),
        # Optimization scenario: moderate metrics, recommendation to fine‑tune
        (
            {
                "sales_volume": 300,
                "conversion_rate": 0.05,
                "average_price": 180.0,
                "inventory_level": 80,
            },
            {"optimize", "adjust", "review", "balance"},
        ),
        # Insufficient data: zeros or NaNs
        (
            {
                "sales_volume": 0,
                "conversion_rate": 0.0,
                "average_price": 0.0,
                "inventory_level": 0,
            },
            {"insufficient", "cannot", "none"},
        ),
        # Minimal input: single record with typical values
        (
            {
                "sales_volume": 50,
                "conversion_rate": 0.02,
                "average_price": 120.0,
                "inventory_level": 20,
            },
            {"maintain", "increase", "decrease", "optimize"},
        ),
    ],
)
def test_recommendation_keywords(metrics, expected_keywords):
    """
    Verify that the recommendation string contains an appropriate
    keyword for each performance scenario.

    The test is intentionally tolerant: as long as the output
    contains at least one keyword from the expected set, the branch
    is considered correctly triggered.
    """
    df = pd.DataFrame([metrics])
    recommendation = _call_recommender(df)

    # Normalise the recommendation to string for keyword matching
    if isinstance(recommendation, dict):
        # Assume the primary recommendation is stored under 'action'
        recommendation_str = str(recommendation.get("action", ""))
    else:
        recommendation_str = str(recommendation)

    recommendation_str_lower = recommendation_str.lower()

    # At least one expected keyword must appear in the recommendation
    assert any(
        kw in recommendation_str_lower for kw in expected_keywords
    ), f"Recommendation '{recommendation_str}' does not contain any expected keyword for metrics {metrics}"


def test_recommendation_deterministic(sample_df):
    """
    Ensure that the recommendation function is deterministic: the same
    input always yields the same output.
    """
    first_call = _call_recommender(sample_df)
    second_call = _call_recommender(sample_df)
    assert first_call == second_call, "Recommendation output changed for identical input"


def test_recommendation_type(sample_df):
    """
    The recommendation should be a string or dictionary.
    """
    recommendation = _call_recommender(sample_df)
    assert isinstance(recommendation, (str, dict)), (
        f"Recommendation returned type {type(recommendation)}; expected str or dict"
    )


def test_recommendation_handles_missing_columns(sample_df):
    """
    When the input dataframe is missing expected columns, the function
    should still produce a recommendation indicating insufficient data.
    """
    # Remove a key metric
    df_missing = sample_df.drop(columns=["sales_volume"])
    recommendation = _call_recommender(df_missing)

    if isinstance(recommendation, dict):
        recommendation_str = str(recommendation.get("action", ""))
    else:
        recommendation_str = str(recommendation)

    assert (
        "insufficient" in recommendation_str.lower()
        or "cannot" in recommendation_str.lower()
    ), f"Recommendation for missing columns: {recommendation_str}"


def test_recommendation_zero_rows():
    """
    An empty dataframe should trigger an insufficient‑data recommendation.
    """
    empty_df = pd.DataFrame(
        columns=[
            "sales_volume",
            "conversion_rate",
            "average_price",
            "inventory_level",
        ]
    )
    recommendation = _call_recommender(empty_df)

    if isinstance(recommendation, dict):
        recommendation_str = str(recommendation.get("action", ""))
    else:
        recommendation_str = str(recommendation)

    assert (
        "insufficient" in recommendation_str.lower()
        or "cannot" in recommendation_str.lower()
    ), f"Recommendation for empty dataframe: {recommendation_str}"
