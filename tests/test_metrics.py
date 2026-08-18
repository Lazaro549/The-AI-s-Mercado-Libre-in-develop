"""Unit tests for metrics module."""

import pytest
from analyzer.metrics import calculate_ctr, calculate_conversion_rate, calculate_acos, summarize_metrics


class TestCalculateCTR:
    """Tests for calculate_ctr function."""
    
    def test_normal_ctr_calculation(self):
        """Test normal CTR calculation."""
        ctr = calculate_ctr(100, 5000)
        assert ctr == pytest.approx(0.02)
    
    def test_zero_clicks(self):
        """Test CTR with zero clicks."""
        ctr = calculate_ctr(0, 5000)
        assert ctr == 0.0
    
    def test_zero_impressions(self):
        """Test CTR with zero impressions returns 0."""
        ctr = calculate_ctr(100, 0)
        assert ctr == 0.0
    
    def test_ctr_100_percent(self):
        """Test CTR when all impressions click."""
        ctr = calculate_ctr(100, 100)
        assert ctr == 1.0
    
    def test_negative_clicks_raises_error(self):
        """Test that negative clicks raise ValueError."""
        with pytest.raises(ValueError):
            calculate_ctr(-10, 5000)
    
    def test_negative_impressions_raises_error(self):
        """Test that negative impressions raise ValueError."""
        with pytest.raises(ValueError):
            calculate_ctr(100, -5000)
    
    def test_non_numeric_clicks_raises_error(self):
        """Test that non-numeric clicks raise TypeError."""
        with pytest.raises(TypeError):
            calculate_ctr("100", 5000)
    
    def test_float_values(self):
        """Test CTR calculation with float values."""
        ctr = calculate_ctr(50.5, 2000.5)
        assert isinstance(ctr, float)


class TestCalculateConversionRate:
    """Tests for calculate_conversion_rate function."""
    
    def test_normal_conversion_calculation(self):
        """Test normal conversion rate calculation."""
        conv = calculate_conversion_rate(10, 500)
        assert conv == pytest.approx(0.02)
    
    def test_zero_sales(self):
        """Test conversion with zero sales."""
        conv = calculate_conversion_rate(0, 500)
        assert conv == 0.0
    
    def test_zero_clicks(self):
        """Test conversion with zero clicks returns 0."""
        conv = calculate_conversion_rate(10, 0)
        assert conv == 0.0
    
    def test_all_clicks_convert(self):
        """Test when all clicks convert."""
        conv = calculate_conversion_rate(100, 100)
        assert conv == 1.0
    
    def test_negative_sales_raises_error(self):
        """Test that negative sales raise ValueError."""
        with pytest.raises(ValueError):
            calculate_conversion_rate(-10, 500)
    
    def test_negative_clicks_raises_error(self):
        """Test that negative clicks raise ValueError."""
        with pytest.raises(ValueError):
            calculate_conversion_rate(10, -500)


class TestCalculateACOS:
    """Tests for calculate_acos function."""
    
    def test_normal_acos_calculation(self):
        """Test normal ACOS calculation."""
        acos = calculate_acos(500, 2500)
        assert acos == pytest.approx(0.2)
    
    def test_zero_ad_spend(self):
        """Test ACOS with zero ad spend."""
        acos = calculate_acos(0, 2500)
        assert acos == 0.0
    
    def test_zero_revenue(self):
        """Test ACOS with zero revenue returns 0."""
        acos = calculate_acos(500, 0)
        assert acos == 0.0
    
    def test_acos_above_one(self):
        """Test ACOS above 1 (losing money)."""
        acos = calculate_acos(3000, 2000)
        assert acos == pytest.approx(1.5)
    
    def test_negative_ad_spend_raises_error(self):
        """Test that negative ad spend raise ValueError."""
        with pytest.raises(ValueError):
            calculate_acos(-500, 2500)
    
    def test_negative_revenue_raises_error(self):
        """Test that negative revenue raise ValueError."""
        with pytest.raises(ValueError):
            calculate_acos(500, -2500)


class TestSummarizeMetrics:
    """Tests for summarize_metrics function."""
    
    def test_normal_metrics_summary(self):
        """Test normal metrics summary calculation."""
        data = {
            "clicks": 100,
            "impressions": 5000,
            "sales": 10,
            "ad_spend": 500,
            "revenue": 2500
        }
        metrics = summarize_metrics(data)
        
        assert "ctr" in metrics
        assert "conversion_rate" in metrics
        assert "acos" in metrics
        assert metrics["ctr"] == pytest.approx(0.02)
        assert metrics["conversion_rate"] == pytest.approx(0.1)
        assert metrics["acos"] == pytest.approx(0.2)
    
    def test_missing_required_keys(self):
        """Test that missing keys raise KeyError."""
        data = {"clicks": 100, "impressions": 5000}
        with pytest.raises(KeyError):
            summarize_metrics(data)
    
    def test_negative_values_raise_error(self):
        """Test that negative values raise ValueError."""
        data = {
            "clicks": -100,
            "impressions": 5000,
            "sales": 10,
            "ad_spend": 500,
            "revenue": 2500
        }
        with pytest.raises(ValueError):
            summarize_metrics(data)
    
    def test_all_zeros(self):
        """Test metrics summary with all zeros."""
        data = {
            "clicks": 0,
            "impressions": 0,
            "sales": 0,
            "ad_spend": 0,
            "revenue": 0
        }
        metrics = summarize_metrics(data)
        assert metrics["ctr"] == 0.0
        assert metrics["conversion_rate"] == 0.0
        assert metrics["acos"] == 0.0
