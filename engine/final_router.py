# ============================================================
# final_router.py — SmartFert Main Controller
# Orchestrates all engines to produce final recommendation.
# ============================================================

from engine.data_loader import load_master_dataset
from engine.normalizer import (
    normalize_state, normalize_crop, normalize_season, 
    normalize_soil, normalize_condition, normalize_float
)
from engine.safe_clamp import clamp_soil_inputs
from engine.npk_engine import get_npk_recommendation
from engine.stcr_engine import compute_stcr
from engine.correction_engine import apply_all_corrections, calculate_organic_content
from engine.advisory_engine import generate_advisories
from engine.fertilizer_convert import convert_to_fertilizers
from engine.bag_rounder import apply_rounding


def validate_entry(state, crop, master):
    if state not in master["data"]:
        return False, f"State '{state}' not found."
    if crop not in master["data"][state]:
        return False, f"Crop '{crop}' not found in {state}."
    return True, None


# ======================================================================
# ✔ FIX APPLIED: tr=None added + passed to generate_advisories()
# ======================================================================
def generate_fertilizer_recommendation(
    state, crop, season,
    soil, organic_type, organic_qty_kg,
    target_yield=None, mode="AUTO", master=None,
    tr=None       # <-- FIX: allow optional translation function
):
    # 0. Load Data if not provided
    if not master:
        master = load_master_dataset()
    
    # 1. Normalize & Validate User Inputs
    state = normalize_state(state)
    crop = normalize_crop(crop)
    season = normalize_season(season)
    
    ok, err = validate_entry(state, crop, master)
    if not ok:
        return {"error": err}

    entry = master["data"][state][crop]
    stcr_avail = entry.get("stcr_available", False)
    npk_avail = entry.get("npk_available", False)

    # 2. Normalize Soil & Clamp
    soil_norm = {
        "SN": normalize_float(soil.get("SN")),
        "SP": normalize_float(soil.get("SP")),
        "SK": normalize_float(soil.get("SK")),
        "pH": normalize_float(soil.get("pH")),
        "OC": normalize_float(soil.get("OC")),
        "EC": normalize_float(soil.get("EC")),
        "Zn": normalize_float(soil.get("Zn")),
        "Fe": normalize_float(soil.get("Fe")),
        "S": normalize_float(soil.get("S")),
        "B": normalize_float(soil.get("B")),
        "Soil_Type": normalize_soil(soil.get("Soil_Type")),
        "Condition": normalize_condition(soil.get("Condition")),
    }
    soil_norm = clamp_soil_inputs(soil_norm)

    # 3. Calculate Organic Nutrients (ON, OP, OK)
    org_vals = calculate_organic_content(organic_type, organic_qty_kg, master)
    soil_norm["ON"] = org_vals["N"]
    soil_norm["OP"] = org_vals["P2O5"]
    soil_norm["OK"] = org_vals["K2O"]

    # 4. Engine Execution Logic
    raw, final, warnings, source = {}, {}, [], "NPK"
    micros = {}
    
    # --- STCR MODE ---
    if mode in ["STCR", "AUTO"] and stcr_avail and target_yield:
        try:
            baseline = get_npk_recommendation(
                entry.get("npk", []),
                season,
                soil_norm["Soil_Type"]
            )
            
            stcr_res = compute_stcr(entry["stcr"][0], soil_norm, target_yield, baseline)
            
            final = stcr_res["final"]
            raw = stcr_res["raw"]
            warnings = stcr_res["warnings"]
            source = "STCR"
            
            corr_res = apply_all_corrections(
                raw, final,
                organic_type, organic_qty_kg,
                soil_norm,
                "STCR",
                master
            )
            micros = corr_res["micronutrient_recommendation"]
            
        except Exception as e:
            if mode == "STCR":
                return {"error": f"STCR Calculation Failed: {str(e)}"}
            source = "NPK"

    # --- NPK MODE ---
    if source == "NPK":
        if not npk_avail:
            return {"error": "No Data Available for this crop/state configuration."}
        
        raw = get_npk_recommendation(
            entry["npk"],
            season,
            soil_norm["Soil_Type"],
            soil_norm["Condition"]
        )
        
        corr_res = apply_all_corrections(
            raw, raw,
            organic_type, organic_qty_kg,
            soil_norm,
            "NPK",
            master
        )
        
        final = corr_res["npk_corrected"]
        micros = corr_res["micronutrient_recommendation"]
        warnings.extend(corr_res["advisories"])

    # ==================================================================
    # 5. Advisories (FIXED — passes tr correctly)
    # ==================================================================
    advisories = generate_advisories(
        soil=soil_norm,
        micronutrients=micros,
        source_used=source,
        master=master,
        tr=tr      # <-- CRITICAL FIX
    )
    advisories.extend(warnings)
    
    # 6. Convert to Fertilizers
    ferts = convert_to_fertilizers(final)
    
    # 7. Apply Bag Rounding
    ferts_rounded = apply_rounding(ferts, mode="Field")

    return {
        "status": "success",
        "meta": {
            "state": state,
            "crop": crop,
            "source_engine": source
        },
        "nutrients_required_kg_ha": final,
        "fertilizers_recommended_kg_ha": ferts_rounded,
        "organic_credit_kg": org_vals,
        "micronutrients": micros,
        "advisories": advisories
    }
