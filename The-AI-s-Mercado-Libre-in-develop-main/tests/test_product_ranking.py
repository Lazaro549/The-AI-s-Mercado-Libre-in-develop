"""Unit tests for product ranking module."""

import pytest
from analyzer.product_ranking import calculate_score, classify_product, rank_products, group_by_action


class TestCalculateScore:
    """Tests for calculate_score function."""
    
    def test_perfect_metrics_max_score(self):
        """Test that perfect metrics give max score."""
        metrics = {
            "ctr": 0.05,
            "conversion_rate": 0.05,
            "acos": 0.15
        }
        score = calculate_score(metrics)
        assert score >= 90  # Should be high
    
    def test_poor_metrics_low_score(self):
        """Test that poor metrics give low score."""
        metrics = {
            "ctr": 0.01,
            "conversion_rate": 0.01,
            "acos": 0.50
        }
        score = calculate_score(metrics)
        assert score < 30  # Should be low
    
    def test_average_metrics_medium_score(self):
        """Test that average metrics give medium score."""
        metrics = {
            "ctr": 0.03,
            "conversion_rate": 0.03,
            "acos": 0.25
        }
        score = calculate_score(metrics)
        assert 40 <= score <= 70  # Should be medium
    
    def test_missing_metrics_raises_error(self):
        """Test that missing metrics raise KeyError."""
        metrics = {"ctr": 0.05, "conversion_rate": 0.05}
        with pytest.raises(KeyError):
            calculate_score(metrics)
    
    def test_non_dict_input_raises_error(self):
        """Test that non-dict input raises TypeError."""
        with pytest.raises(TypeError):
            calculate_score([0.05, 0.05, 0.2])
    
    def test_score_range(self):
        """Test that score is between 0 and 100."""
        metrics = {
            "ctr": 0.03,
            "conversion_rate": 0.03,
            "acos": 0.25
        }
        score = calculate_score(metrics)
        assert 0 <= score <= 100


class TestClassifyProduct:
    """Tests for classify_product function."""
    
    def test_high_score_returns_scale(self):
        """Test that score >= 70 returns 'scale'."""
        assert classify_product(75) == "scale"
        assert classify_product(100) == "scale"
        assert classify_product(70) == "scale"
    
    def test_medium_score_returns_optimize(self):
        """Test that 40 <= score < 70 returns 'optimize'."""
        assert classify_product(50) == "optimize"
        assert classify_product(40) == "optimize"
        assert classify_product(69) == "optimize"
    
    def test_low_score_returns_pause(self):
        """Test that score < 40 returns 'pause'."""
        assert classify_product(39) == "pause"
        assert classify_product(0) == "pause"
        assert classify_product(20) == "pause"
    
    def test_non_numeric_score_raises_error(self):
        """Test that non-numeric score raises TypeError."""
        with pytest.raises(TypeError):
            classify_product("70")


class TestRankProducts:
    """Tests for rank_products function."""
    
    def test_rank_products_basic(self):
        """Test basic product ranking."""
        products = [
            {
                "id": "P1",
                "impressions": 1000,
                "clicks": 50,
                "sales": 5,
                "ad_spend": 100,
                "revenue": 500
            },
            {
                "id": "P2",
                "impressions": 2000,
                "clicks": 40,
                "sales": 2,
                "ad_spend": 150,
                "revenue": 300
            }
        ]
        
        ranked = rank_products(products)
        
        assert len(ranked) == 2
        assert "product_id" in ranked[0]
        assert "metrics" in ranked[0]
        assert "score" in ranked[0]
        assert "category" in ranked[0]
        # First should have higher score
        assert ranked[0]["score"] >= ranked[1]["score"]
    
    def test_rank_products_empty_list(self):
        """Test ranking empty product list."""
        ranked = rank_products([])
        assert ranked == []
    
    def test_rank_products_not_list_raises_error(self):
        """Test that non-list input raises TypeError."""
        with pytest.raises(TypeError):
            rank_products({"id": "P1"})
    
    def test_rank_products_handles_invalid_product(self):
        """Test that invalid products are skipped."""
        products = [
            {
                "id": "P1",
                "impressions": 1000,
                "clicks": 50,
                "sales": 5,
                "ad_spend": 100,
                "revenue": 500
            },
            {
                "id": "P2"
                # Missing required fields
            }
        ]
        
        ranked = rank_products(products)
        # Should only have the valid product
        assert len(ranked) == 1
        assert ranked[0]["product_id"] == "P1"


class TestGroupByAction:
    """Tests for group_by_action function."""
    
    def test_group_by_action_basic(self):
        """Test basic grouping by action."""
        ranked = [
            {"product_id": "P1", "score": 80, "category": "scale"},
            {"product_id": "P2", "score": 50, "category": "optimize"},
            {"product_id": "P3", "score": 20, "category": "pause"}
        ]
        
        grouped = group_by_action(ranked)
        
        assert "scale" in grouped
        assert "optimize" in grouped
        assert "pause" in grouped
        assert len(grouped["scale"]) == 1
        assert len(grouped["optimize"]) == 1
        assert len(grouped["pause"]) == 1
    
    def test_group_by_action_all_scale(self):
        """Test grouping when all products should scale."""
        ranked = [
            {"product_id": "P1", "score": 80, "category": "scale"},
            {"product_id": "P2", "score": 75, "category": "scale"}
        ]
        
        grouped = group_by_action(ranked)
        
        assert len(grouped["scale"]) == 2
        assert len(grouped["optimize"]) == 0
        assert len(grouped["pause"]) == 0
    
    def test_group_by_action_empty_list(self):
        """Test grouping empty list."""
        grouped = group_by_action([])
        
        assert len(grouped["scale"]) == 0
        assert len(grouped["optimize"]) == 0
        assert len(grouped["pause"]) == 0
    
    def test_group_by_action_not_list_raises_error(self):
        """Test that non-list input raises TypeError."""
        with pytest.raises(TypeError):
            group_by_action({"category": "scale"})
    
    def test_group_by_action_unknown_category(self):
        """Test handling of unknown category."""
        ranked = [
            {"product_id": "P1", "score": 50, "category": "unknown"}
        ]
        
        grouped = group_by_action(ranked)
        
        # Unknown category defaults to pause
        assert len(grouped["pause"]) == 1
