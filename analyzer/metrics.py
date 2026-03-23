# analyzer/metrics.py

def calculate_ctr(clicks, impressions):
    if impressions == 0:
        return 0
    return clicks / impressions


def calculate_conversion_rate(sales, clicks):
    if clicks == 0:
        return 0
    return sales / clicks


def calculate_acos(ad_spend, revenue):
    if revenue == 0:
        return 0
    return ad_spend / revenue


def summarize_metrics(data):
    return {
        "ctr": calculate_ctr(data["clicks"], data["impressions"]),
        "conversion_rate": calculate_conversion_rate(data["sales"], data["clicks"]),
        "acos": calculate_acos(data["ad_spend"], data["revenue"])
    }
