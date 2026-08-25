"""
Tests for analyzer.recommendations.

These tests validate the public API:
    generate_recommendations(problems)

The tests intentionally verify behavior rather than implementation details.
"""

import pytest

from analyzer.recommendations import generate_recommendations


def test_generate_recommendations_requires_list():
    """The function should reject non-list inputs."""
    with pytest.raises(TypeError):
        generate_recommendations(None)

    with pytest.raises(TypeError):
        generate_recommendations({})

    with pytest.raises(TypeError):
        generate_recommendations("low_ctr")


def test_empty_problem_list_returns_empty_list():
    """No problems should produce no recommendations."""
    result = generate_recommendations([])

    assert isinstance(result, list)
    assert result == []


@pytest.mark.parametrize(
    "problem_type, expected_keywords",
    [
        (
            "low_ctr",
            ["título", "imagen", "precio"],
        ),
        (
            "low_conversion",
            ["precio", "descripción", "reputación"],
        ),
        (
            "high_acos",
            ["acos", "pausar", "inversión"],
        ),
        (
            "healthy",
            ["escalar", "activa", "similares"],
        ),
    ],
)
def test_generate_recommendations_for_problem_type(
    problem_type,
    expected_keywords,
):
    """Each supported problem type should generate actionable recommendations."""
    problems = [
        {
            "type": problem_type,
            "message": f"Test problem: {problem_type}",
        }
    ]

    result = generate_recommendations(problems)

    assert isinstance(result, list)
    assert len(result) == 3

    result_text = " ".join(result).lower()

    for keyword in expected_keywords:
        assert keyword.lower() in result_text


def test_multiple_problems_generate_combined_recommendations():
    """Multiple problems should produce recommendations for all problems."""
    problems = [
        {
            "type": "low_ctr",
            "message": "CTR is below target",
        },
        {
            "type": "low_conversion",
            "message": "Conversion rate is below target",
        },
        {
            "type": "high_acos",
            "message": "ACOS is above target",
        },
    ]

    result = generate_recommendations(problems)

    assert isinstance(result, list)
    assert len(result) == 9


def test_healthy_problem_generates_scaling_recommendations():
    """Healthy products should receive scaling-oriented recommendations."""
    problems = [
        {
            "type": "healthy",
            "message": "Product performance is healthy",
        }
    ]

    result = generate_recommendations(problems)

    result_text = " ".join(result).lower()

    assert "escalar presupuesto" in result_text
    assert "campaña" in result_text


def test_unknown_problem_type_is_ignored():
    """Unknown problem types should not crash the function."""
    problems = [
        {
            "type": "unknown_problem",
            "message": "Unknown problem",
        }
    ]

    result = generate_recommendations(problems)

    assert isinstance(result, list)
    assert result == []


def test_problem_without_type_is_ignored():
    """Problems without a type should be safely ignored."""
    problems = [
        {
            "message": "Missing problem type",
        }
    ]

    result = generate_recommendations(problems)

    assert isinstance(result, list)
    assert result == []


def test_recommendations_are_strings():
    """Every generated recommendation should be a string."""
    problems = [
        {"type": "low_ctr", "message": "Low CTR"},
        {"type": "low_conversion", "message": "Low conversion"},
        {"type": "high_acos", "message": "High ACOS"},
        {"type": "healthy", "message": "Healthy"},
    ]

    result = generate_recommendations(problems)

    assert all(isinstance(recommendation, str) for recommendation in result)


def test_recommendations_are_deterministic():
    """The same input should always produce the same output."""
    problems = [
        {
            "type": "high_acos",
            "message": "ACOS is too high",
        }
    ]

    first_result = generate_recommendations(problems)
    second_result = generate_recommendations(problems)

    assert first_result == second_result


def test_problem_message_does_not_change_recommendation_logic():
    """Recommendation logic should depend on problem type."""
    problems_a = [
        {
            "type": "low_ctr",
            "message": "CTR is terrible",
        }
    ]

    problems_b = [
        {
            "type": "low_ctr",
            "message": "CTR needs improvement",
        }
    ]

    assert generate_recommendations(problems_a) == generate_recommendations(
        problems_b
    )
