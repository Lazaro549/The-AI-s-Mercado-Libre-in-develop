"""Diagnosis module for identifying performance issues.

This module analyzes product metrics and identifies problems that need attention.
"""

import logging
from typing import Dict, List
from config_loader import get_config

logger = logging.getLogger(__name__)


def diagnose(metrics: Dict[str, float]) -> List[Dict[str, str]]:
    """Diagnose performance issues based on product metrics.
    
    Analyzes CTR, Conversion Rate, and ACOS to identify problems:
    - Low CTR: Many impressions but few clicks
    - Low Conversion: Many clicks but few sales
    - High ACOS: Low profitability
    
    Args:
        metrics (Dict[str, float]): Dictionary containing:
            - ctr (float): Click-Through Rate
            - conversion_rate (float): Conversion rate
            - acos (float): ACOS value
            
    Returns:
        List[Dict[str, str]]: List of problems found, each with:
            - type (str): Problem type
            - message (str): Human-readable problem description
            
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
    
    # Load thresholds from config
    config = get_config()
    metric_config = config.get("metrics", {})
    
    ctr_low_threshold = metric_config.get("ctr", {}).get("low", 0.02)
    conversion_low_threshold = metric_config.get("conversion_rate", {}).get("low", 0.02)
    acos_high_threshold = metric_config.get("acos", {}).get("high", 0.30)
    
    problems = []
    
    # Check CTR
    if metrics["ctr"] < ctr_low_threshold:
        problems.append({
            "type": "low_ctr",
            "message": f"Bajo CTR ({metrics['ctr']:.2%}): muchas impresiones pero pocos clics"
        })
        logger.warning(f"Low CTR detected: {metrics['ctr']:.4f}")
    
    # Check Conversion Rate
    if metrics["conversion_rate"] < conversion_low_threshold:
        problems.append({
            "type": "low_conversion",
            "message": f"Baja conversión ({metrics['conversion_rate']:.2%}): muchos clics pero pocas ventas"
        })
        logger.warning(f"Low conversion rate detected: {metrics['conversion_rate']:.4f}")
    
    # Check ACOS
    if metrics["acos"] > acos_high_threshold:
        problems.append({
            "type": "high_acos",
            "message": f"ACOS alto ({metrics['acos']:.2%}): inversión publicitaria poco rentable"
        })
        logger.warning(f"High ACOS detected: {metrics['acos']:.4f}")
    
    # If no problems found
    if not problems:
        problems.append({
            "type": "healthy",
            "message": "Publicación con buen rendimiento"
        })
        logger.info("Product metrics are healthy")
    
    return problems
