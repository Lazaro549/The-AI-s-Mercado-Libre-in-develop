# app.py

from analyzer.metrics import summarize_metrics
from analyzer.diagnosis import diagnose
from analyzer.recommendations import generate_recommendations

from ads.acos_optimizer import evaluate_acos, suggest_acos_adjustment
from ads.bidding_logic import bidding_strategy, calculate_max_cpc


def analyze_product(data, target_acos):
    print("\n--- ANÁLISIS DE PUBLICACIÓN ---\n")

    # 1. Métricas
    metrics = summarize_metrics(data)
    print("Métricas:")
    print(metrics)

    # 2. Diagnóstico
    problems = diagnose(metrics)
    print("\nProblemas detectados:")
    for p in problems:
        print("-", p["message"])

    # 3. Recomendaciones
    actions = generate_recommendations(problems)
    print("\nAcciones recomendadas:")
    for a in actions:
        print("-", a)

    # 4. Evaluación de ACOS
    acos_status = evaluate_acos(metrics["acos"], target_acos)
    acos_actions = suggest_acos_adjustment(metrics["acos"], target_acos)

    print("\nEstado de ACOS:")
    print("-", acos_status["message"])

    print("\nAcciones sobre ACOS:")
    for a in acos_actions:
        print("-", a)

    # 5. Estrategia de pujas
    cpc = calculate_max_cpc(
        target_acos,
        data["revenue"] / data["sales"] if data["sales"] > 0 else 0,
        metrics["conversion_rate"]
    )

    strategy = bidding_strategy(metrics, target_acos)

    print("\nEstrategia de pujas:")
    print("- CPC máximo sugerido:", round(cpc, 2))

    for s in strategy:
        print("-", s)

    print("\n--- FIN DEL ANÁLISIS ---\n")


if __name__ == "__main__":
    # 🔧 Datos de prueba (esto luego lo conectas a datos reales)
    product_data = {
        "impressions": 12000,
        "clicks": 150,
        "sales": 3,
        "ad_spend": 900,
        "revenue": 3000
    }

    target_acos = 0.25

    analyze_product(product_data, target_acos)
