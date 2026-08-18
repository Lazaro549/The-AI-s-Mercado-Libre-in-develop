"""Product ranking and classification module.

This module provides functions to rank products based on performance metrics
and classify them into actions: Scale, Optimize, or Pause.
"""

import logging
from typing import List, Dict
from analyzer.metrics import summarize_metrics
from config_loader import get_config

logger = logging.getLogger(__name__)


def calculate_score(metrics: Dict[str, float]) -> int:
    """Calculate a performance score for a product.
    
    Score ranges from 0 to 100 based on:
    - CTR (0-30 points): Higher CTR is better
    - Conversion Rate (0-40 points): Higher conversion is better
    - ACOS (0-30 points): Lower ACOS is better
    
    Args:
        metrics (Dict[str, float]): Dictionary containing:
            - ctr (float): Click-Through Rate
            - conversion_rate (float): Conversion rate
            - acos (float): ACOS value
            
    Returns:
        int: Performance score from 0 to 100.
        
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
    
    # Load scoring config
    config = get_config()
    scoring_config = config.get("scoring", {})
    metric_config = config.get("metrics", {})
    
    score = 0
    
    # CTR scoring (max 30 points)
    ctr_excellent = metric_config.get("ctr", {}).get("excellent", 0.05)
    ctr_good = metric_config.get("ctr", {}).get("good", 0.03)
    ctr_max_points = scoring_config.get("ctr_max_points", 30)
    
    if metrics["ctr"] >= ctr_excellent:
        score += ctr_max_points
    elif metrics["ctr"] >= ctr_good:
        score += int(ctr_max_points * 2/3)
    elif metrics["ctr"] >= metric_config.get("ctr", {}).get("low", 0.02):
        score += int(ctr_max_points * 1/3)
    
    # Conversion Rate scoring (max 40 points)
    conv_excellent = metric_config.get("conversion_rate", {}).get("excellent", 0.05)
    conv_good = metric_config.get("conversion_rate", {}).get("good", 0.03)
    conv_max_points = scoring_config.get("conversion_max_points", 40)
    
    if metrics["conversion_rate"] >= conv_excellent:
        score += conv_max_points
    elif metrics["conversion_rate"] >= conv_good:
        score += int(conv_max_points * 0.625)
    elif metrics["conversion_rate"] >= metric_config.get("conversion_rate", {}).get("low", 0.02):
        score += int(conv_max_points * 0.375)
    
    # ACOS scoring (max 30 points, lower is better)
    acos_good = metric_config.get("acos", {}).get("good", 0.20)
    acos_high = metric_config.get("acos", {}).get("high", 0.30)
    acos_max_points = scoring_config.get("acos_max_points", 30)
    
    if metrics["acos"] <= acos_good:
        score += acos_max_points
    elif metrics["acos"] <= acos_high:
        score += int(acos_max_points * 2/3)
    elif metrics["acos"] <= metric_config.get("acos", {}).get("critical", 0.40):
        score += int(acos_max_points * 1/3)
    
    logger.debug(f"Score calculated: {score} for metrics: {metrics}")
    return score


def classify_product(score: int) -> str:
    """Classify a product based on its performance score.
    
    Classification:
    - score >= 70: "scale" (high performance, increase investment)
    - 40 <= score < 70: "optimize" (needs improvement)
    - score < 40: "pause" (low performance, stop spending)
    
    Args:
        score (int): Performance score from 0 to 100.
        
    Returns:
        str: Classification ("scale", "optimize", or "pause").
        
    Raises:
        TypeError: If score is not numeric.
    """
    if not isinstance(score, (int, float)):
        raise TypeError("score must be numeric")
    
    config = get_config()
    scoring_config = config.get("scoring", {})
    
    scale_threshold = scoring_config.get("scale_threshold", 70)
    optimize_threshold = scoring_config.get("optimize_threshold", 40)
    
    if score >= scale_threshold:
        return "scale"
    elif score >= optimize_threshold:
        return "optimize"
    else:
        return "pause"


def rank_products(products: List[Dict]) -> List[Dict]:
    """Rank products by performance score.
    
    Calculates metrics and score for each product, classifies them,
    and returns sorted by score (best first).
    
    Args:
        products (List[Dict]): List of product data dictionaries, each containing:
            - id (str): Product identifier
            - impressions (int): Number of impressions
            - clicks (int): Number of clicks
            - sales (int): Number of sales
            - ad_spend (float): Advertising spend
            - revenue (float): Total revenue
            
    Returns:
        List[Dict]: Ranked products with added fields:
            - product_id (str): Product ID
            - metrics (Dict): Calculated metrics
            - score (int): Performance score
            - category (str): Classification
            
    Raises:
        TypeError: If products is not a list.
        ValueError: If products list is empty.
    """
    if not isinstance(products, list):
        raise TypeError("products must be a list")
    
    if len(products) == 0:
        logger.warning("Empty products list provided")
        return []
    
    results = []
    
    for product in products:
        try:
            metrics = summarize_metrics(product)
            score = calculate_score(metrics)
            category = classify_product(score)
            
            results.append({
                "product_id": product.get("id", "N/A"),
                "metrics": metrics,
                "score": score,
                "category": category
            })
        except (KeyError, TypeError, ValueError) as e:
            logger.error(f"Error processing product {product.get('id', 'N/A')}: {e}")
            continue
    
    # Sort by score (best first)
    results = sorted(results, key=lambda x: x["score"], reverse=True)
    logger.info(f"Ranked {len(results)} products successfully")
    
    return results


def group_by_action(ranked_products: List[Dict]) -> Dict[str, List[Dict]]:
    """Group ranked products by recommended action.
    
    Organizes products into three groups based on their classification:
    scale, optimize, or pause.
    
    Args:
        ranked_products (List[Dict]): List of ranked product dictionaries,
            each containing a "category" field.
            
    Returns:
        Dict[str, List[Dict]]: Dictionary with keys "scale", "optimize", "pause",
            each containing the corresponding products.
            
    Raises:
        TypeError: If ranked_products is not a list.
    """
    if not isinstance(ranked_products, list):
        raise TypeError("ranked_products must be a list")
    
    grouped = {
        "scale": [],
        "optimize": [],
        "pause": []
    }
    
    for product in ranked_products:
        category = product.get("category", "pause")
        if category in grouped:
            grouped[category].append(product)
        else:
            logger.warning(f"Unknown category '{category}' for product {product.get('product_id')}, defaulting to pause")
            grouped["pause"].append(product)
    
    logger.info(f"Products grouped: {len(grouped['scale'])} scale, "
                f"{len(grouped['optimize'])} optimize, {len(grouped['pause'])} pause")
    
    return grouped
