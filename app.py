# app.py

from analyzer.metrics import summarize_metrics
from analyzer.diagnosis import diagnose
from analyzer.recommendations import generate_recommendations

from ads.acos_optimizer import evaluate_acos, suggest_acos_adjustment
from ads.bidding_logic import bidding_strategy, calculate_max_cpc


def analyze_product(data, target_acos):
    # 1. Calcular métricas
    metrics = summarize_metrics(data)

    # 2. Diagnóstico
    problems = diagnose(metrics)

    # 3. Recomendaciones de publicación
    recommendations = generate_recommendations(problems)

    # 4. Evaluación de ACOS
    acos_status = evaluate_acos(metrics["acos"], target_acos)
    acos_actions = suggest_acos_adjustment(metrics["acos"], target_acos)

    # 5. Estrategia de pujas
    cpc = calculate_max_cpc(
        target_acos,
        data["revenue"] / max(data["sales"], 1),
        metrics["conversion_rate"]
    )

    bidding_actions = bidding_strategy(metrics, target_acos)

    # 6. Resultado final
    return {
        "metrics": metrics,
        "diagnosis": problems,
        "recommendations": recommendations,
        "acos": {
            "status": acos_status,
            "actions": acos_actions
        },
        "ads": {
            "max_cpc": cpc,
            "bidding_strategy": bidding_actions
        }
    }


def print_report(result):
    print("\n--- REPORTE DE PRODUCTO ---\n")

    print("📊 Métricas:")
    for k, v in result["metrics"].items():
        print(f"- {k}: {round(v, 4)}")

    print("\n🔍 Diagnóstico:")
    for d in result["diagnosis"]:
        print(f"- {d['message']}")

    print("\n⚙️ Recomendaciones:")
    for r in result["recommendations"]:
        print(f"- {r}")

    print("\n💰 ACOS:")
    print(f"- Estado: {result['acos']['status']['message']}")
    for a in result["acos"]["actions"]:
        print(f"- {a}")

    print("\n⚔️ Estrategia Ads:")
    print(f"- CPC máximo sugerido: {round(result['ads']['max_cpc'], 2)}")
    for s in result["ads"]["bidding_strategy"]:
        print(f"- {s}")


if __name__ == "__main__":
    # 🔴 Simulación (debes reemplazar con datos reales)
    product_data = {
        "impressions": 15000,
        "clicks": 120,
        "sales": 3,
        "ad_spend": 900,
        "revenue": 3000
    }

    target_acos = 0.25

    result = analyze_product(product_data, target_acos)
    print_report(result)
