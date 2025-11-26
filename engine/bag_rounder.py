# ============================================================
# bag_rounder.py — SmartFert Rounding Logic
# ============================================================

def round_nearest(x, base):
    """Rounds x to the nearest multiple of base."""
    if x is None or x <= 0: return 0
    return base * round(x / base)

def apply_rounding(ferts, mode="Exact"):
    """
    Modes:
    - Exact: 2 decimal places (Scientific)
    - Field: Nearest 5kg (Easy for farmer)
    - Bag: Nearest 25kg (Half bag logic)
    """
    if not ferts: return {}
    m = mode.lower()

    if m == "exact":
        return {k: round(v, 2) for k, v in ferts.items()}
    
    elif m.startswith("field"):
        return {k: round_nearest(v, 5) for k, v in ferts.items()}
    
    elif m.startswith("bag"):
        # Urea/DAP/MOP usually 45-50kg bags. 
        # Rounding to 25kg (half bag) is safest approximation.
        return {k: round_nearest(v, 25) for k, v in ferts.items()}
    
    # Default fallback
    return {k: round(v, 2) for k, v in ferts.items()}