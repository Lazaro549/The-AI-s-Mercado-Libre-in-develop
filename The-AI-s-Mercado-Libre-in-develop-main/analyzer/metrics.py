"""Metrics calculation module for the AI Mercado Libre Optimizer.

This module provides functions to calculate key performance indicators (KPIs)
used to analyze product performance in advertising campaigns.
"""

import logging
from typing import Dict, Union

logger = logging.getLogger(__name__)


def calculate_ctr(clicks: int, impressions: int) -> float:
    """Calculate Click-Through Rate (CTR).
    
    CTR = Clicks / Impressions
    Indicates the percentage of users who clicked on the ad.
    
    Args:
        clicks (int): Number of clicks received.
        impressions (int): Number of impressions shown.
        
    Returns:
        float: CTR as a decimal (0.0 to 1.0). Returns 0.0 if impressions is 0.
        
    Raises:
        ValueError: If clicks or impressions are negative.
        TypeError: If arguments are not numeric.
    """
    if not isinstance(clicks, (int, float)) or not isinstance(impressions, (int, float)):
        raise TypeError("clicks and impressions must be numeric")
    
    if clicks < 0 or impressions < 0:
        raise ValueError("clicks and impressions cannot be negative")
    
    if impressions == 0:
        logger.warning("impressions is 0, returning CTR of 0")
        return 0.0
    
    ctr = clicks / impressions
    logger.debug(f"CTR calculated: {ctr:.4f} (clicks={clicks}, impressions={impressions})")
    return ctr


def calculate_conversion_rate(sales: int, clicks: int) -> float:
    """Calculate Conversion Rate.
    
    Conversion Rate = Sales / Clicks
    Indicates the percentage of clicks that resulted in a sale.
    
    Args:
        sales (int): Number of sales made.
        clicks (int): Number of clicks received.
        
    Returns:
        float: Conversion rate as a decimal (0.0 to 1.0). Returns 0.0 if clicks is 0.
        
    Raises:
        ValueError: If sales or clicks are negative.
        TypeError: If arguments are not numeric.
    """
    if not isinstance(sales, (int, float)) or not isinstance(clicks, (int, float)):
        raise TypeError("sales and clicks must be numeric")
    
    if sales < 0 or clicks < 0:
        raise ValueError("sales and clicks cannot be negative")
    
    if clicks == 0:
        logger.warning("clicks is 0, returning conversion rate of 0")
        return 0.0
    
    conversion_rate = sales / clicks
    logger.debug(f"Conversion rate calculated: {conversion_rate:.4f} (sales={sales}, clicks={clicks})")
    return conversion_rate


def calculate_acos(ad_spend: Union[int, float], revenue: Union[int, float]) -> float:
    """Calculate ACOS (Advertising Cost of Sales).
    
    ACOS = Ad Spend / Revenue
    Indicates the percentage of revenue that was spent on advertising.
    Lower ACOS is better for profitability.
    
    Args:
        ad_spend (Union[int, float]): Total advertising spend.
        revenue (Union[int, float]): Total revenue from sales.
        
    Returns:
        float: ACOS as a decimal (0.0 to infinity). Returns 0.0 if revenue is 0.
        
    Raises:
        ValueError: If ad_spend or revenue are negative.
        TypeError: If arguments are not numeric.
    """
    if not isinstance(ad_spend, (int, float)) or not isinstance(revenue, (int, float)):
        raise TypeError("ad_spend and revenue must be numeric")
    
    if ad_spend < 0 or revenue < 0:
        raise ValueError("ad_spend and revenue cannot be negative")
    
    if revenue == 0:
        logger.warning("revenue is 0, returning ACOS of 0")
        return 0.0
    
    acos = ad_spend / revenue
    logger.debug(f"ACOS calculated: {acos:.4f} (ad_spend={ad_spend}, revenue={revenue})")
    return acos


def summarize_metrics(data: Dict[str, Union[int, float]]) -> Dict[str, float]:
    """Calculate all key metrics for a product.
    
    Computes CTR, Conversion Rate, and ACOS from raw performance data.
    
    Args:
        data (Dict[str, Union[int, float]]): Dictionary containing:
            - clicks (int): Number of clicks
            - impressions (int): Number of impressions
            - sales (int): Number of sales
            - ad_spend (Union[int, float]): Total ad spend
            - revenue (Union[int, float]): Total revenue
            
    Returns:
        Dict[str, float]: Dictionary with keys: ctr, conversion_rate, acos
        
    Raises:
        KeyError: If required keys are missing from data dictionary.
        TypeError: If any value is not numeric.
        ValueError: If any value is negative.
    """
    required_keys = ["clicks", "impressions", "sales", "ad_spend", "revenue"]
    missing_keys = [k for k in required_keys if k not in data]
    
    if missing_keys:
        raise KeyError(f"Missing required keys: {missing_keys}")
    
    try:
        metrics = {
            "ctr": calculate_ctr(data["clicks"], data["impressions"]),
            "conversion_rate": calculate_conversion_rate(data["sales"], data["clicks"]),
            "acos": calculate_acos(data["ad_spend"], data["revenue"])
        }
        logger.info(f"Metrics summarized: {metrics}")
        return metrics
    except (TypeError, ValueError) as e:
        logger.error(f"Error calculating metrics: {e}")
        raise
