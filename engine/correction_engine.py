# ============================================================
# correction_engine.py — SmartFert Tuning
# FIX: Added logic to prevent double subtraction of organic
# nutrient if the STCR equation already handles it.
# ============================================================

def safe_num(x):
    try: return float(x)
    except: return None

def classify(value, thresholds):
    """Returns 'low', 'medium', or 'high' based on soil test."""
    v = safe_num(value)
    if v is None: return "medium"
    
    if v < thresholds["low"]["max"]: return "low"
    if v < thresholds["medium"]["max"]: return "medium"
    return "high"

def calculate_organic_content(o_type, o_qty, master):
    """Calculates kg of N, P, K added by organic manure."""
    organic_rules = master["organic_rules"]
    manure = organic_rules["organic_inputs"]["manure"]
    cakes = organic_rules["organic_inputs"]["oilseed_cakes"]
    all_sources = manure + cakes

    # Normalize name comparison
    entry = next((m for m in all_sources if m["name"].lower().strip() == str(o_type).lower().strip()), None)
    
    if not entry or not o_qty:
        return {"N": 0, "P2O5": 0, "K2O": 0}
    
    return {
        "N": (entry["N_percent"] / 100) * o_qty,
        "P2O5": (entry["P2O5_percent"] / 100) * o_qty,
        "K2O": (entry["K2O_percent"] / 100) * o_qty
    }

def compute_micronutrients(soil, micro_rules):
    """Detects deficiencies based on soil tests."""
    out = {}
    for key, block in micro_rules.items():
        if key == "logic": continue
        
        crit = block.get("critical_limit")
        if crit is None: continue

        param = block["parameter"]
        soil_key = None
        if "Zinc" in param: soil_key = "Zn"
        elif "Iron" in param: soil_key = "Fe"
        elif "Manganese" in param: soil_key = "Mn"
        elif "Copper" in param: soil_key = "Cu"
        elif "Boron" in param: soil_key = "B"
        elif "Sulphur" in param: soil_key = "S"
        
        val = safe_num(soil.get(soil_key))
        if val is not None and val < crit:
            # Recommendations
            if soil_key == "Zn": out["Zinc"] = {"ZnSO4_kg": 25}
            elif soil_key == "Fe": out["Iron"] = {"FeSO4_kg": 20}
            elif soil_key == "S": out["Sulphur"] = {"Gypsum_kg": 40}
            elif soil_key == "B": out["Boron"] = {"Borax_kg": 5}
            else: out[key] = {"Supplement_kg": 10}
            
    return out 

def apply_all_corrections(
    npk_raw, npk_initial, organic_type, organic_qty_kg, 
    soil, source_used, master, ignore_organic_subtraction=False
):
    """
    Args:
        ignore_organic_subtraction (bool): If True, organic nutrients won't be subtracted 
                                           (used when STCR equation already accounts for them).
    """
    corrected = npk_initial.copy()
    
    # --------------------------------------------------------
    # STEP 1: SOIL FERTILITY MULTIPLIERS
    # --------------------------------------------------------
    # Apply Soil Multipliers mainly for NPK mode or if STCR doesn't use soil params (rare)
    if source_used == "NPK":
        macro = master["soil_thresholds"]["soil_fertility_thresholds"]["macronutrients"]
        MULT = {"low": 1.25, "medium": 1.0, "high": 0.75}

        cN = classify(soil.get("SN"), macro["nitrogen"]["thresholds"])
        corrected["N"] *= MULT[cN]

        pH = safe_num(soil.get("pH"))
        p_key = "phosphorus_acidic" if pH and pH < 6.5 else "phosphorus_alkaline"
        cP = classify(soil.get("SP"), macro[p_key]["thresholds"])
        corrected["P2O5"] *= MULT[cP]

        cK = classify(soil.get("SK"), macro["potassium"]["thresholds"])
        corrected["K2O"] *= MULT[cK]

    # --------------------------------------------------------
    # STEP 2: SUBTRACT ORGANIC INPUTS (Conditional)
    # --------------------------------------------------------
    org_vals = calculate_organic_content(organic_type, organic_qty_kg, master)
    
    if not ignore_organic_subtraction:
        corrected["N"] = max(corrected["N"] - org_vals["N"], 0)
        corrected["P2O5"] = max(corrected["P2O5"] - org_vals["P2O5"], 0)
        corrected["K2O"] = max(corrected["K2O"] - org_vals["K2O"], 0)
    
    # Rounding
    for k in corrected:
        corrected[k] = round(corrected[k], 2)

    # --------------------------------------------------------
    # STEP 3: MICRONUTRIENTS
    # --------------------------------------------------------
    micro_rules = master["soil_thresholds"]["soil_fertility_thresholds"]["micronutrients"]
    micros = compute_micronutrients(soil, micro_rules)

    return {
        "npk_corrected": corrected,
        "organic_used": org_vals,
        "micronutrient_recommendation": micros,
        "advisories": []
    }