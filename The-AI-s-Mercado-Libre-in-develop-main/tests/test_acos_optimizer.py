"""Unit tests for ACOS optimizer module."""

import pytest
from ads.acos_optimizer import evaluate_acos, suggest_acos_adjustment


class TestEvaluateAcos:
    """Tests for evaluate_acos function."""
    
    def test_acos_below_target_is_profitable(self):
        """Test that ACOS below target is marked as profitable."""
        result = evaluate_acos(0.20, 0.30)
        
        assert result["status"] == "below_target"
        assert "rentable" in result["message"].lower()
    
    def test_acos_above_target_is_unprofitable(self):
        """Test that ACOS above target is marked as unprofitable."""
        result = evaluate_acos(0.40, 0.30)
        
        assert result["status"] == "above_target"
        assert "no rentable" in result["message"].lower()
    
    def test_acos_on_target(self):
        """Test that ACOS on target is recognized."""
        result = evaluate_acos(0.30, 0.30)
        
        assert result["status"] == "on_target"
        assert "objetivo" in result["message"].lower()
    
    def test_result_has_required_keys(self):
        """Test that result has required keys."""
        result = evaluate_acos(0.25, 0.30)
        
        assert "status" in result
        assert "message" in result
    
    def test_negative_acos_raises_error(self):
        """Test that negative ACOS raises ValueError."""
        with pytest.raises(ValueError):
            evaluate_acos(-0.25, 0.30)
    
    def test_negative_target_raises_error(self):
        """Test that negative target raises ValueError."""
        with pytest.raises(ValueError):
            evaluate_acos(0.25, -0.30)
    
    def test_non_numeric_acos_raises_error(self):
        """Test that non-numeric ACOS raises TypeError."""
        with pytest.raises(TypeError):
            evaluate_acos("0.25", 0.30)
    
    def test_zero_acos(self):
        """Test ACOS of zero (no ad spend)."""
        result = evaluate_acos(0.0, 0.30)
        
        assert result["status"] == "below_target"


class TestSuggestAcosAdjustment:
    """Tests for suggest_acos_adjustment function."""
    
    def test_above_target_suggests_cost_reduction(self):
        """Test that high ACOS suggests cost reduction."""
        actions = suggest_acos_adjustment(0.40, 0.30)
        
        assert len(actions) > 0
        assert isinstance(actions, list)
        # Should suggest reducing spending
        action_text = " ".join(actions).lower()
        assert "reducir" in action_text or "disminuir" in action_text or "pausar" in action_text
    
    def test_below_target_suggests_scaling(self):
        """Test that low ACOS suggests scaling."""
        actions = suggest_acos_adjustment(0.20, 0.30)
        
        assert len(actions) > 0
        # Should suggest increasing spending
        action_text = " ".join(actions).lower()
        assert "aumentar" in action_text or "escalar" in action_text or "incrementar" in action_text
    
    def test_on_target_suggests_maintenance(self):
        """Test that on-target ACOS suggests maintenance."""
        actions = suggest_acos_adjustment(0.30, 0.30)
        
        assert len(actions) > 0
        # Should suggest maintaining
        action_text = " ".join(actions).lower()
        assert "mantener" in action_text or "monitorear" in action_text
    
    def test_actions_are_specific_strings(self):
        """Test that actions are specific, non-empty strings."""
        actions = suggest_acos_adjustment(0.25, 0.30)
        
        for action in actions:
            assert isinstance(action, str)
            assert len(action) > 0
    
    def test_negative_acos_raises_error(self):
        """Test that negative ACOS raises ValueError."""
        with pytest.raises(ValueError):
            suggest_acos_adjustment(-0.25, 0.30)
    
    def test_negative_target_raises_error(self):
        """Test that negative target raises ValueError."""
        with pytest.raises(ValueError):
            suggest_acos_adjustment(0.25, -0.30)
    
    def test_non_numeric_acos_raises_error(self):
        """Test that non-numeric ACOS raises TypeError."""
        with pytest.raises(TypeError):
            suggest_acos_adjustment("0.25", 0.30)
    
    def test_high_acos_multiple_actions(self):
        """Test that high ACOS gets multiple recommendations."""
        actions = suggest_acos_adjustment(0.50, 0.30)
        
        assert len(actions) >= 3
    
    def test_zero_acos_with_positive_target(self):
        """Test zero ACOS (free traffic) with positive target."""
        actions = suggest_acos_adjustment(0.0, 0.30)
        
        assert len(actions) > 0
        # Should suggest scaling
        action_text = " ".join(actions).lower()
        assert "aumentar" in action_text or "escalar" in action_text
