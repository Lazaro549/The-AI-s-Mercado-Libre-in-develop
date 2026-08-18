"""Recommendations module for actionable product optimization insights.

This module generates specific recommendations based on identified problems.
"""

import logging
from typing import List, Dict

logger = logging.getLogger(__name__)


def generate_recommendations(problems: List[Dict[str, str]]) -> List[str]:
    """Generate actionable recommendations based on identified problems.
    
    Maps problem types to specific optimization actions:
    - low_ctr: Improve visibility and appeal
    - low_conversion: Improve conversion funnel
    - high_acos: Reduce advertising costs
    - healthy: Scale successful products
    
    Args:
        problems (List[Dict[str, str]]): List of problems, each containing:
            - type (str): Problem type
            - message (str): Human-readable description
            
    Returns:
        List[str]: List of specific action recommendations.
        
    Raises:
        TypeError: If problems is not a list.
    """
    if not isinstance(problems, list):
        raise TypeError("problems must be a list")
    
    actions = []
    
    for problem in problems:
        problem_type = problem.get("type", "")
        
        if problem_type == "low_ctr":
            recommendations = [
                "Optimizar título con palabras clave principales",
                "Mejorar imagen principal (fondo blanco, producto claro)",
                "Revisar precio frente a la competencia"
            ]
            actions.extend(recommendations)
            logger.info("Low CTR recommendations added")
            
        elif problem_type == "low_conversion":
            recommendations = [
                "Ajustar precio o agregar promociones",
                "Mejorar descripción con beneficios claros",
                "Revisar reputación y tiempos de envío"
            ]
            actions.extend(recommendations)
            logger.info("Low conversion recommendations added")
            
        elif problem_type == "high_acos":
            recommendations = [
                "Reducir ACOS objetivo en campaña",
                "Pausar productos con bajo rendimiento",
                "Concentrar inversión en productos con más ventas"
            ]
            actions.extend(recommendations)
            logger.info("High ACOS recommendations added")
            
        elif problem_type == "healthy":
            recommendations = [
                "Escalar presupuesto en campañas",
                "Mantener campaña activa al menos 30 días",
                "Duplicar estrategia en productos similares"
            ]
            actions.extend(recommendations)
            logger.info("Healthy product scaling recommendations added")
        else:
            logger.warning(f"Unknown problem type: {problem_type}")
    
    logger.debug(f"Generated {len(actions)} recommendations")
    return actions
