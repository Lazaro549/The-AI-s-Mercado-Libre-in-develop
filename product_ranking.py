# analyzer/product_ranking.py

from analyzer.metrics import summarize_metrics


def calculate_score(metrics):
    """
    Score de 0 a 100 basado en:
    - CTR
    - Conversión
    - ACOS
    """

    score = 0

    # CTR (máx 30 puntos)
    if metrics["ctr"] >= 0.05:
        score += 30
    elif metrics["ctr"] >= 0.03:
        score += 20
    elif metrics["ctr"] >= 0.02:
        score += 10

    # Conversión (máx 40 puntos)
    if metrics["conversion_rate"] >= 0.05:
        score += 40
    elif metrics["conversion_rate"] >= 0.03:
        score += 25
    elif metrics["conversion_rate"] >= 0.02:
        score += 15

    # ACOS (máx 30 puntos, menor es mejor)
    if metrics["acos"] <= 0.20:
        score += 30
    elif metrics["acos"] <= 0.30:
        score += 20
    elif metrics["acos"] <= 0.40:
        score += 10

    return score


def classify_product(score):
    """
    Clasificación de producto según score
    """

    if score >= 70:
        return "scale"
    elif score >= 40:
        return "optimize"
    else:
        return "pause"


def rank_products(products):
    """
    Recibe lista de productos y devuelve ranking completo
    """

    results = []

    for product in products:
        metrics = summarize_metrics(product)
        score = calculate_score(metrics)
        category = classify_product(score)

        results.append({
            "product_id": product.get("id", "N/A"),
            "metrics": metrics,
            "score": score,
            "category": category
        })

    # Ordenar de mejor a peor
    results = sorted(results, key=lambda x: x["score"], reverse=True)

    return results


def group_by_action(ranked_products):
    """
    Agrupa productos por acción recomendada
    """

    grouped = {
        "scale": [],
        "optimize": [],
        "pause": []
    }

    for product in ranked_products:
        grouped[product["category"]].append(product)

    return grouped
