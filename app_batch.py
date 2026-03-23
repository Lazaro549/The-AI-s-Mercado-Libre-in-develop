# app_batch.py

from analyzer.product_ranking import rank_products, group_by_action
from analyzer.diagnosis import diagnose
from analyzer.recommendations import generate_recommendations


def analyze_catalog(products):
    print("\n========== ANÁLISIS MASIVO DE PRODUCTOS ==========\n")

    # 1. Ranking
    ranked = rank_products(products)

    print("🔝 TOP PRODUCTOS (ordenados por rendimiento):\n")
    for p in ranked:
        print(f"ID: {p['product_id']}")
        print(f"Score: {p['score']} | Categoría: {p['category']}")
        print(f"Métricas: {p['metrics']}")
        print("-" * 50)

    # 2. Agrupación por acción
    grouped = group_by_action(ranked)

    print("\n📊 RESUMEN DE ACCIONES:\n")
    print(f"🟢 Escalar: {len(grouped['scale'])}")
    print(f"🟡 Optimizar: {len(grouped['optimize'])}")
    print(f"🔴 Pausar: {len(grouped['pause'])}")

    # 3. Detalle por grupo (solo problemas y acciones)
    for category, items in grouped.items():
        print(f"\n===== {category.upper()} =====\n")

        for product in items:
            print(f"Producto: {product['product_id']}")
            problems = diagnose(product["metrics"])
            actions = generate_recommendations(problems)

            print("Problemas:")
            for p in problems:
                print("-", p["message"])

            print("Acciones:")
            for a in actions:
                print("-", a)

            print("-" * 50)


if __name__ == "__main__":
    # 🔧 Simulación de catálogo (reemplazar con datos reales)
    products = [
        {
            "id": "A1",
            "impressions": 15000,
            "clicks": 800,
            "sales": 60,
            "ad_spend": 2000,
            "revenue": 12000
        },
        {
            "id": "B2",
            "impressions": 12000,
            "clicks": 200,
            "sales": 5,
            "ad_spend": 1500,
            "revenue": 4000
        },
        {
            "id": "C3",
            "impressions": 9000,
            "clicks": 90,
            "sales": 1,
            "ad_spend": 800,
            "revenue": 1500
        }
    ]

    analyze_catalog(products)
