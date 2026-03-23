# analyzer/recommendations.py

def generate_recommendations(problems):
    actions = []

    for problem in problems:

        if problem["type"] == "low_ctr":
            actions.append("Optimizar título con palabras clave principales")
            actions.append("Mejorar imagen principal (fondo blanco, producto claro)")
            actions.append("Revisar precio frente a la competencia")

        elif problem["type"] == "low_conversion":
            actions.append("Ajustar precio o agregar promociones")
            actions.append("Mejorar descripción con beneficios claros")
            actions.append("Revisar reputación y tiempos de envío")

        elif problem["type"] == "high_acos":
            actions.append("Reducir ACOS objetivo en campaña")
            actions.append("Pausar productos con bajo rendimiento")
            actions.append("Concentrar inversión en productos con más ventas")

        elif problem["type"] == "healthy":
            actions.append("Escalar presupuesto en campañas")
            actions.append("Mantener campaña activa al menos 30 días")
            actions.append("Duplicar estrategia en productos similares")

    return actions
