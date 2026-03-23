# ads/bidding_logic.py

def calculate_max_cpc(target_acos, revenue_per_sale, conversion_rate):
    """
    CPC máximo estimado basado en:
    - ACOS objetivo
    - ingreso por venta
    - tasa de conversión
    """
    if conversion_rate == 0:
        return 0

    return target_acos * revenue_per_sale * conversion_rate


def bidding_strategy(metrics, target_acos):
    strategy = []

    # CTR bajo → no conviene subir puja
    if metrics["ctr"] < 0.02:
        strategy.append("No aumentar puja hasta mejorar CTR")

    # Buena conversión → escalar
    if metrics["conversion_rate"] > 0.03:
        strategy.append("Aumentar puja para ganar más visibilidad")

    # ACOS alto → bajar agresividad
    if metrics["acos"] > target_acos:
        strategy.append("Reducir puja para controlar costos")

    # Buen rendimiento general
    if (
        metrics["ctr"] > 0.03 and
        metrics["conversion_rate"] > 0.03 and
        metrics["acos"] < target_acos
    ):
        strategy.append("Escalar agresivamente campaña")

    return strategy
