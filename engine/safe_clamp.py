# ============================================================
# safe_clamp.py — SmartFert Engine
# Ensures input values are within realistic agronomic ranges
# to prevent math errors (e.g., negative yield).
# ============================================================

def clamp_soil_inputs(soil_dict):
    """
    Clamps soil parameters to safe ranges.
    """
    d = soil_dict.copy()

    # pH Range: 3.0 to 11.0 (Extreme limits)
    if d.get("pH") is not None:
        try:
            val = float(d["pH"])
            d["pH"] = max(3.0, min(11.0, val))
        except:
            d["pH"] = 7.0 # Default neutral

    # Organic Carbon Range: 0% to 5%
    if d.get("OC") is not None:
        try:
            val = float(d["OC"])
            d["OC"] = max(0.0, min(5.0, val))
        except:
            d["OC"] = 0.5

    # Electrical Conductivity: 0 to 20 dS/m
    if d.get("EC") is not None:
        try:
            val = float(d["EC"])
            d["EC"] = max(0.0, min(20.0, val))
        except:
            d["EC"] = 0.0

    # Macronutrients (0 to 2000 kg/ha)
    for k in ["SN", "SP", "SK"]:
        if d.get(k) is not None:
            try:
                val = float(d[k])
                d[k] = max(0.0, min(2000.0, val))
            except:
                d[k] = 0.0
            
    return d