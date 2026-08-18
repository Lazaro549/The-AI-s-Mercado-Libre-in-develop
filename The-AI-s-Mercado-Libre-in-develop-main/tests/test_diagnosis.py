"""Unit tests for diagnosis module."""

import pytest
from analyzer.diagnosis import diagnose


class TestDiagnose:
    """Tests for diagnose function."""
    
    def test_healthy_metrics_no_problems(self):
        """Test that healthy metrics show no problems."""
        metrics = {
            "ctr": 0.05,
            "conversion_rate": 0.05,
            "acos": 0.15
        }
        problems = diagnose(metrics)
        
        assert len(problems) > 0
        assert problems[0]["type"] == "healthy"
    
    def test_low_ctr_detected(self):
        """Test that low CTR is detected."""
        metrics = {
            "ctr": 0.01,
            "conversion_rate": 0.05,
            "acos": 0.15
        }
        problems = diagnose(metrics)
        
        assert any(p["type"] == "low_ctr" for p in problems)
    
    def test_low_conversion_detected(self):
        """Test that low conversion rate is detected."""
        metrics = {
            "ctr": 0.05,
            "conversion_rate": 0.01,
            "acos": 0.15
        }
        problems = diagnose(metrics)
        
        assert any(p["type"] == "low_conversion" for p in problems)
    
    def test_high_acos_detected(self):
        """Test that high ACOS is detected."""
        metrics = {
            "ctr": 0.05,
            "conversion_rate": 0.05,
            "acos": 0.35
        }
        problems = diagnose(metrics)
        
        assert any(p["type"] == "high_acos" for p in problems)
    
    def test_multiple_problems_detected(self):
        """Test that multiple problems are detected."""
        metrics = {
            "ctr": 0.01,
            "conversion_rate": 0.01,
            "acos": 0.50
        }
        problems = diagnose(metrics)
        
        # Should detect all three problems
        assert any(p["type"] == "low_ctr" for p in problems)
        assert any(p["type"] == "low_conversion" for p in problems)
        assert any(p["type"] == "high_acos" for p in problems)
    
    def test_missing_metrics_raises_error(self):
        """Test that missing metrics raise KeyError."""
        metrics = {"ctr": 0.05, "conversion_rate": 0.05}
        with pytest.raises(KeyError):
            diagnose(metrics)
    
    def test_non_dict_input_raises_error(self):
        """Test that non-dict input raises TypeError."""
        with pytest.raises(TypeError):
            diagnose([0.05, 0.05, 0.15])
    
    def test_problem_messages_are_strings(self):
        """Test that problem messages are descriptive strings."""
        metrics = {
            "ctr": 0.01,
            "conversion_rate": 0.05,
            "acos": 0.15
        }
        problems = diagnose(metrics)
        
        for problem in problems:
            assert isinstance(problem["message"], str)
            assert len(problem["message"]) > 0
    
    def test_critical_acos_detected(self):
        """Test detection of critical ACOS level."""
        metrics = {
            "ctr": 0.05,
            "conversion_rate": 0.05,
            "acos": 0.45
        }
        problems = diagnose(metrics)
        
        assert any(p["type"] == "high_acos" for p in problems)
