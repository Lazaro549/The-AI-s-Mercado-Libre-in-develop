def predict_price(title, description, attributes):
    """Simple heuristic price prediction placeholder.
    Replace with a real ML model integration later.
    """
    base = 10.0
    length = len(title or "") + len(description or "")
    attr_bonus = sum(len(str(v)) for v in (attributes or {}).values())
    price = base + (length * 0.1) + (attr_bonus * 0.05)
    return round(price, 2)
