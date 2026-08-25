"""
Deterministic bidding optimization utilities.

The public API is intentionally compatible with the existing test suite.
"""

from __future__ import annotations

from numbers import Real


DEFAULT_MIN_BID = 0.10
DEFAULT_MAX_BID = 10.00


def _validate_number(value: Real, name: str) -> float:
    """Validate a numeric non-negative value."""
    if isinstance(value, bool) or not isinstance(value, Real):
        raise TypeError(f"{name} must be numeric")

    value = float(value)

    if value < 0:
        raise ValueError(f"{name} cannot be negative")

    return value


def get_min_bid(
    budget: float = 0.0,
    *args,
    **kwargs,
) -> float:
    """
    Return the minimum allowed bid.

    Extra keyword arguments are accepted for compatibility with callers
    that provide a complete bidding parameter set.
    """
    budget = _validate_number(budget, "budget")

    # Keep a stable floor while allowing very small budgets to use
    # the minimum bid without producing zero bids.
    if budget == 0:
        return DEFAULT_MIN_BID

    return DEFAULT_MIN_BID


def get_max_bid(
    budget: float = 0.0,
    *args,
    **kwargs,
) -> float:
    """
    Return the maximum allowed bid.

    The value scales conservatively with budget while remaining bounded.
    """
    budget = _validate_number(budget, "budget")

    if budget == 0:
        return DEFAULT_MIN_BID

    return max(
        DEFAULT_MIN_BID,
        min(DEFAULT_MAX_BID, budget),
    )


def _clamp(
    value: float,
    minimum: float,
    maximum: float,
) -> float:
    """Clamp a value between minimum and maximum."""
    return max(minimum, min(maximum, value))


def calculate_bid(
    budget: float = 0.0,
    current_bid: float = 0.0,
    acos: float = 0.0,
    target_acos: float = 0.0,
    conversion_rate: float = 0.0,
    clicks: float = 0.0,
    sales: float = 0.0,
    revenue: float = 0.0,
    impressions: float = 0.0,
    ad_spend: float = 0.0,
    **kwargs,
) -> float:
    """
    Calculate a recommended advertising bid.

    Parameters are intentionally permissive because the existing test suite
    supplies different subsets of the complete bidding context.

    Decision rules:

    - Invalid negative values raise ValueError.
    - Missing/zero performance data produces a conservative bid.
    - ACOS substantially above target lowers the bid.
    - ACOS below target increases the bid.
    - ACOS near target maintains the bid.
    - Conversion rate influences the strength of the adjustment.
    - The result is always bounded by get_min_bid() and get_max_bid().
    """

    values = {
        "budget": budget,
        "current_bid": current_bid,
        "acos": acos,
        "target_acos": target_acos,
        "conversion_rate": conversion_rate,
        "clicks": clicks,
        "sales": sales,
        "revenue": revenue,
        "impressions": impressions,
        "ad_spend": ad_spend,
    }

    for name, value in values.items():
        values[name] = _validate_number(value, name)

    budget = values["budget"]
    current_bid = values["current_bid"]
    acos = values["acos"]
    target_acos = values["target_acos"]
    conversion_rate = values["conversion_rate"]
    clicks = values["clicks"]
    sales = values["sales"]

    minimum = get_min_bid(budget=budget)
    maximum = get_max_bid(budget=budget)

    if maximum < minimum:
        maximum = minimum

    # If no current bid is provided, start from the minimum.
    if current_bid <= 0:
        current_bid = minimum

    current_bid = _clamp(
        current_bid,
        minimum,
        maximum,
    )

    # Derive conversion rate when the caller provides clicks and sales
    # but leaves conversion_rate at zero.
    if conversion_rate == 0 and clicks > 0:
        conversion_rate = sales / clicks

    # Without a valid target, remain conservative.
    if target_acos <= 0:
        return round(current_bid, 2)

    # ACOS substantially above target.
    if acos > target_acos * 1.25:
        multiplier = 0.75

    # ACOS moderately above target.
    elif acos > target_acos * 1.05:
        multiplier = 0.90

    # ACOS approximately on target.
    elif acos >= target_acos * 0.95:
        multiplier = 1.00

    # ACOS moderately below target.
    elif acos >= target_acos * 0.75:
        multiplier = 1.05

    # Strong ACOS performance.
    else:
        multiplier = 1.15

    # No conversions should never result in an aggressive bid increase.
    if conversion_rate <= 0:
        multiplier = min(multiplier, 0.90)

    # Very low conversion rate should also be conservative.
    elif conversion_rate < 0.01:
        multiplier = min(multiplier, 0.95)

    recommended_bid = current_bid * multiplier

    return round(
        _clamp(
            recommended_bid,
            minimum,
            maximum,
        ),
        2,
    )
