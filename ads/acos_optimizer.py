# ads/acos_optimizer.py

def evaluate_acos(current_acos, target_acos):
    if current_acos > target_acos:
        return {
            "status": "above_target",
            "message": "ACOS por encima del objetivo (no rentable)"
        }
    elif current_acos < target_acos:
        return {
            "status": "below_target",
            "message": "ACOS por debajo del objetivo (rentable)"
        }
    else:
        return {
            "status": "on_target",
            "message": "ACOS en objetivo"
        }


def suggest_acos_adjustment(current_acos, target_acos):
    if current_acos > target_acos:
        return [
            "Reducir ACOS objetivo",
            "Disminuir presupuesto en campañas",
            "Pausar productos con bajo rendimiento"
        ]
    elif current_acos < target_acos:
        return [
            "Aumentar presupuesto",
            "Escalar productos con buen rendimiento",
            "Incrementar visibilidad en campañas"
        ]
    else:
        return [
            "Mantener configuración actual",
            "Monitorear métricas semanalmente"
        ]
