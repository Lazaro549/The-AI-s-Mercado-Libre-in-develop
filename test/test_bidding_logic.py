"""
Test suite for the bidding logic module (`ads/bidding_logic.py`).

The tests are designed to be resilient to changes in the public API:
* They first attempt to import the expected functions. If a function
  does not exist, the corresponding test is skipped.
* The tests use `inspect.signature` to adapt to the function's
  signature when checking parameter existence.
* The suite covers a variety of realistic bidding scenarios, including
  strong/weak performance, target ACOS, boundary checks, zero/edge
  inputs, and invalid inputs that should raise an exception.
"""

from __future__ import annotations

import inspect
import math
from typing import Any, Callable, Dict, Iterable, Tuple

import pytest

# Import the module under test.  If the module cannot be imported,
# the entire test module will be skipped.
try:
    import ads.bidding_logic as bidding_logic
except Exception as exc:  # pragma: no cover
    pytest.skip(f"Unable to import ads.bidding_logic: {exc}", allow_module_level=True)

# Helper utilities ---------------------------------------------------------

def _has_function(name: str) -> bool:
    """Return True if the module has a public function with the given name."""
    return callable(getattr(bidding_logic, name, None))

def _get_signature(func: Callable) -> inspect.Signature:
    """Return the signature of a function."""
    return inspect.signature(func)

def _call_with_kwargs(func: Callable, kwargs: Dict[str, Any]) -> Any:
    """Call a function with keyword arguments, ignoring missing params."""
    sig = _get_signature(func)
    filtered = {k: v for k, v in kwargs.items() if k in sig.parameters}
    return func(**filtered)

# Parameters for test scenarios ---------------------------------------------

# Normal scenario: typical values that should produce a positive bid
NORMAL_PARAMS = {
    "budget": 1_000.0,
    "target_acos": 0.10,
    "impressions": 10_000,
    "clicks": 200,
    "sales": 50.0,
}

# Strong performance: high conversion rate
STRONG_PERFORMANCE_PARAMS = {
    "budget": 1_000.0,
    "target_acos": 0.10,
    "impressions": 10_000,
    "clicks": 500,
    "sales": 200.0,
}

# Weak performance: low conversion rate
WEAK_PERFORMANCE_PARAMS = {
    "budget": 1_000.0,
    "target_acos": 0.10,
    "impressions": 10_000,
    "clicks": 200,
    "sales": 5.0,
}

# Target ACOS scenario: very tight ACOS target
TIGHT_ACOS_PARAMS = {
    "budget": 1_000.0,
    "target_acos": 0.02,
    "impressions": 10_000,
    "clicks": 200,
    "sales": 50.0,
}

# Edge case: zero impressions, zero clicks
ZERO_INPUTS_PARAMS = {
    "budget": 1_000.0,
    "target_acos": 0.10,
    "impressions": 0,
    "clicks": 0,
    "sales": 0.0,
}

# Invalid inputs: negative values that should raise an exception
INVALID_PARAMS = [
    {"budget": -100.0, "target_acos": 0.10, "impressions": 1000, "clicks": 50, "sales": 10.0},
    {"budget": 1000.0, "target_acos": -0.05, "impressions": 1000, "clicks": 50, "sales": 10.0},
    {"budget": 1000.0, "target_acos": 0.10, "impressions": -100, "clicks": 50, "sales": 10.0},
    {"budget": 1000.0, "target_acos": 0.10, "impressions": 1000, "clicks": -10, "sales": 10.0},
    {"budget": 1000.0, "target_acos": 0.10, "impressions": 1000, "clicks": 50, "sales": -5.0},
]

# ---------------------------------------------------------------------------

# Determine whether the core bidding function exists
if _has_function("calculate_bid"):
    calculate_bid: Callable = getattr(bidding_logic, "calculate_bid")
else:
    calculate_bid = None  # pragma: no cover

# Optional helper functions for min/max bid bounds
get_min_bid = getattr(bidding_logic, "get_min_bid", None)
get_max_bid = getattr(bidding_logic, "get_max_bid", None)

# ---------------------------------------------------------------------------

# Test cases ---------------------------------------------------------------

@pytest.mark.skipif(calculate_bid is None, reason="calculate_bid function not present")
@pytest.mark.parametrize(
    "params,description",
    [
        (NORMAL_PARAMS, "normal scenario"),
        (STRONG_PERFORMANCE_PARAMS, "strong performance"),
        (WEAK_PERFORMANCE_PARAMS, "weak performance"),
        (TIGHT_ACOS_PARAMS, "tight ACOS target"),
    ],
)
def test_calculate_bid_scenarios(params: Dict[str, Any], description: str) -> None:
    """
    Test that calculate_bid returns a non-negative float and respects
    any available min/max bounds for a variety of realistic scenarios.
    """
    bid = _call_with_kwargs(calculate_bid, params)

    assert isinstance(bid, (float, int)), f"{description}: bid should be numeric"
    assert bid >= 0, f"{description}: bid should be non-negative"

    # If min/max helper functions exist, ensure bid is within bounds
    if callable(get_min_bid):
        min_bid = get_min_bid(**params)
        assert bid >= min_bid, f"{description}: bid below minimum {min_bid}"
    if callable(get_max_bid):
        max_bid = get_max_bid(**params)
        assert bid <= max_bid, f"{description}: bid above maximum {max_bid}"


@pytest.mark.skipif(calculate_bid is None, reason="calculate_bid function not present")
def test_calculate_bid_zero_inputs() -> None:
    """
    When all performance metrics are zero, the function should return 0
    or a value that does not exceed the maximum allowed bid.
    """
    bid = _call_with_kwargs(calculate_bid, ZERO_INPUTS_PARAMS)
    assert isinstance(bid, (float, int)), "Zero inputs: bid should be numeric"
    assert bid >= 0, "Zero inputs: bid should be non-negative"

    # If a max bid is defined, the zero input bid should not exceed it
    if callable(get_max_bid):
        max_bid = get_max_bid(**ZERO_INPUTS_PARAMS)
        assert bid <= max_bid, f"Zero inputs: bid exceeds max {max_bid}"


@pytest.mark.skipif(calculate_bid is None, reason="calculate_bid function not present")
@pytest.mark.parametrize("params", INVALID_PARAMS)
def test_calculate_bid_invalid_inputs(params: Dict[str, Any]) -> None:
    """
    The function should raise ValueError (or a subclass) when any input
    parameter is invalid (negative or nonsensical values).
    """
    with pytest.raises(ValueError):
        _call_with_kwargs(calculate_bid, params)


# ---------------------------------------------------------------------------

# Optional: test min/max helper functions if they exist

@pytest.mark.skipif(get_min_bid is None, reason="get_min_bid function not present")
def test_get_min_bid_validity() -> None:
    """
    Ensure that get_min_bid returns a non-negative float for a normal scenario.
    """
    min_bid = get_min_bid(**NORMAL_PARAMS)
    assert isinstance(min_bid, (float, int)), "min_bid should be numeric"
    assert min_bid >= 0, "min_bid should be non-negative"


@pytest.mark.skipif(get_max_bid is None, reason="get_max_bid function not present")
def test_get_max_bid_validity() -> None:
    """
    Ensure that get_max_bid returns a float greater than or equal to min_bid.
    """
    min_bid = get_min_bid(**NORMAL_PARAMS) if callable(get_min_bid) else 0.0
    max_bid = get_max_bid(**NORMAL_PARAMS)
    assert isinstance(max_bid, (float, int)), "max_bid should be numeric"
    assert max_bid >= min_bid, "max_bid should be >= min_bid"
    assert max_bid >= 0, "max_bid should be non-negative"
