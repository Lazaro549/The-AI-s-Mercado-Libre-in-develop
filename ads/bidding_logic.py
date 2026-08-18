"""Bidding strategy module for advertising campaign optimization.

This module provides functions to calculate optimal CPC bids and generate
bidding strategies based on product performance metrics.
"""

import logging
from typing import Dict, List, Union

logger = logging.getLogger(__name__)


def calculate_max_cpc(target_acos: float, revenue_per_sale: Union[int, float], 
                      conversion_rate: float) -> float:
    """Calculate maximum CPC (Cost Per Click) based on profitability targets.
    
    Formula: Max CPC = Target ACOS × Revenue Per Sale × Conversion Rate
    
    This helps determine the maximum you should bid per click while maintaining
    your target profitability.
    
    Args:
        target_acos (float): Target ACOS (e.g., 0.25 for 25%).
        revenue_per_sale (Union[int, float]): Average revenue generated per sale.
        conversion_rate (float): Conversion rate (e.g., 0.03 for 3%).
        
    Returns:
        float: Maximum CPC to maintain profitability. Returns 0.0 if conversion_rate is 0.
        
    Raises:
        ValueError: If target_acos, revenue_per_sale, or conversion_rate are negative.
        TypeError: If arguments are not numeric.
    """
    if not isinstance(target_acos, (int, float)) or not isinstance(revenue_per_sale, (int, float)) \
            or not isinstance(conversion_rate, (int, float)):
        raise TypeError("target_acos, revenue_per_sale, and conversion_rate must be numeric")
    
    if target_acos < 0 or revenue_per_sale < 0 or conversion_rate < 0:
        raise ValueError("target_acos, revenue_per_sale, and conversion_rate cannot be negative")
    
    if conversion_rate == 0:
        logger.warning("conversion_rate is 0, returning max CPC of 0")
        return 0.0
    
    max_cpc = target_acos * revenue_per_sale * conversion_rate
    logger.debug(f"Max CPC calculated: {max_cpc:.2f} "
                 f"(target_acos={target_acos}, revenue={revenue_per_sale}, conv_rate={conversion_rate})")
    return max_cpc


def bidding_strategy(metrics: Dict[str, float], target_acos: float) -> List[str]:
    """Generate a bidding strategy based on product performance metrics.
    
    Recommends bidding actions:
    - Don't increase if CTR is low (visibility problem)
    - Increase if conversion is high (good sales potential)
    - Decrease if ACOS exceeds target (profitability issue)
    - Aggressive scaling if all metrics are good
    
    Args:
        metrics (Dict[str, float]): Dictionary containing:
            - ctr (float): Click-Through Rate
            - conversion_rate (float): Conversion rate
            - acos (float): Current ACOS
        target_acos (float): Target ACOS threshold.
        
    Returns:
        List[str]: List of bidding strategy recommendations.
        
    Raises:
        KeyError: If required metric keys are missing.
        TypeError: If metrics values are not numeric.
    """
    if not isinstance(metrics, dict):
        raise TypeError("metrics must be a dictionary")
    
    required_keys = ["ctr", "conversion_rate", "acos"]
    missing_keys = [k for k in required_keys if k not in metrics]
    if missing_keys:
        raise KeyError(f"Missing required metrics: {missing_keys}")
    
    if not isinstance(target_acos, (int, float)):
        raise TypeError("target_acos must be numeric")
    
    strategy = []
    
    # Low CTR → don't increase bid
    if metrics["ctr"] < 0.02:
        strategy.append("No aumentar puja hasta mejorar CTR")
        logger.info("Strategy: Don't increase bid due to low CTR")
    
    # Good conversion → scale
    if metrics["conversion_rate"] > 0.03:
        strategy.append("Aumentar puja para ganar más visibilidad")
        logger.info("Strategy: Increase bid due to good conversion")
    
    # High ACOS → reduce aggressiveness
    if metrics["acos"] > target_acos:
        strategy.append("Reducir puja para controlar costos")
        logger.info("Strategy: Reduce bid due to high ACOS")
    
    # All metrics good → aggressive scaling
    if (metrics["ctr"] > 0.03 and
        metrics["conversion_rate"] > 0.03 and
        metrics["acos"] < target_acos):
        strategy.append("Escalar agresivamente campaña")
        logger.info("Strategy: Aggressive scaling recommended")
    
    # If no specific strategy
    if not strategy:
        strategy.append("Mantener puja actual y monitorear métricas")
        logger.info("Strategy: Maintain current bid")
    
    return strategy
