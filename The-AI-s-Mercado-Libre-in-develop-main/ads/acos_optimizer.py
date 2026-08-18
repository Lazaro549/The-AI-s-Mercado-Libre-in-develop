"""ACOS optimization module for profitability management.

This module provides functions to evaluate and optimize ACOS (Advertising Cost of Sales)
to ensure campaigns maintain profitability targets.
"""

import logging
from typing import Dict, List

logger = logging.getLogger(__name__)


def evaluate_acos(current_acos: float, target_acos: float) -> Dict[str, str]:
    """Evaluate current ACOS against target profitability.
    
    Compares actual ACOS with the target threshold to determine if the campaign
    is profitable or needs adjustment.
    
    Args:
        current_acos (float): Current ACOS value (e.g., 0.25 for 25%).
        target_acos (float): Target ACOS threshold (e.g., 0.30 for 30%).
        
    Returns:
        Dict[str, str]: Evaluation result with:
            - status (str): "above_target", "below_target", or "on_target"
            - message (str): Human-readable evaluation
            
    Raises:
        ValueError: If current_acos or target_acos are negative.
        TypeError: If arguments are not numeric.
    """
    if not isinstance(current_acos, (int, float)) or not isinstance(target_acos, (int, float)):
        raise TypeError("current_acos and target_acos must be numeric")
    
    if current_acos < 0 or target_acos < 0:
        raise ValueError("current_acos and target_acos cannot be negative")
    
    if current_acos > target_acos:
        status = "above_target"
        message = "ACOS por encima del objetivo (no rentable)"
        logger.warning(f"ACOS above target: {current_acos:.2%} > {target_acos:.2%}")
    elif current_acos < target_acos:
        status = "below_target"
        message = "ACOS por debajo del objetivo (rentable)"
        logger.info(f"ACOS below target: {current_acos:.2%} < {target_acos:.2%}")
    else:
        status = "on_target"
        message = "ACOS en objetivo"
        logger.info(f"ACOS on target: {current_acos:.2%}")
    
    return {
        "status": status,
        "message": message
    }


def suggest_acos_adjustment(current_acos: float, target_acos: float) -> List[str]:
    """Suggest specific actions to adjust ACOS to meet profitability targets.
    
    Recommends different strategies depending on whether ACOS is above or below target:
    - If above: Reduce spending and focus on best performers
    - If below: Increase spending on high-performing campaigns
    - If on target: Maintain and monitor
    
    Args:
        current_acos (float): Current ACOS value (e.g., 0.25 for 25%).
        target_acos (float): Target ACOS threshold (e.g., 0.30 for 30%).
        
    Returns:
        List[str]: List of specific actions to optimize ACOS.
        
    Raises:
        ValueError: If current_acos or target_acos are negative.
        TypeError: If arguments are not numeric.
    """
    if not isinstance(current_acos, (int, float)) or not isinstance(target_acos, (int, float)):
        raise TypeError("current_acos and target_acos must be numeric")
    
    if current_acos < 0 or target_acos < 0:
        raise ValueError("current_acos and target_acos cannot be negative")
    
    actions = []
    
    if current_acos > target_acos:
        actions = [
            "Reducir ACOS objetivo",
            "Disminuir presupuesto en campañas",
            "Pausar productos con bajo rendimiento"
        ]
        logger.info("Cost reduction actions recommended")
    elif current_acos < target_acos:
        actions = [
            "Aumentar presupuesto",
            "Escalar productos con buen rendimiento",
            "Incrementar visibilidad en campañas"
        ]
        logger.info("Scaling actions recommended")
    else:
        actions = [
            "Mantener configuración actual",
            "Monitorear métricas semanalmente"
        ]
        logger.info("Maintenance actions recommended")
    
    return actions
