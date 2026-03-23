# analyzer/diagnosis.py

def diagnose(metrics):
    problems = []

    # CTR bajo
    if metrics["ctr"] < 0.02:
        problems.append({
            "type": "low_ctr",
            "message": "Bajo CTR: muchas impresiones pero pocos clics"
        })

    # Conversión baja
    if metrics["conversion_rate"] < 0.02:
        problems.append({
            "type": "low_conversion",
            "message": "Baja conversión: muchos clics pero pocas ventas"
        })

    # ACOS alto
    if metrics["acos"] > 0.30:
        problems.append({
            "type": "high_acos",
            "message": "ACOS alto: inversión publicitaria poco rentable"
        })

    if not problems:
        problems.append({
            "type": "healthy",
            "message": "Publicación con buen rendimiento"
        })

    return problems
