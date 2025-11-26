# ============================================================
# advisory_engine.py — Generates text advisories (Bilingual + Safe Fallback)
# ============================================================

def safe_num(x):
    try:
        return float(x)
    except:
        return None


# ------------------------------------------------------------
# MAIN FUNCTION (tr is OPTIONAL now)
# ------------------------------------------------------------
def generate_advisories(soil, micronutrients, source_used, master, tr=None):
    """
    soil        : dict of soil values
    micronutrients : dict of detected deficiencies
    source_used : "NPK" or "STCR"
    master      : master dataset
    tr          : OPTIONAL translation function
                  If missing → English fallback
    """

    # -------------------------------
    # SAFE TRANSLATION FALLBACK
    # -------------------------------
    if tr is None:
        # fallback: identity translation (English)
        tr = lambda x: x

    adv = []

    # ---------------------------------------------------
    # 1. Mode Info
    # ---------------------------------------------------
    if source_used == "STCR":
        adv.append(tr("adv_stcr_mode"))
    else:
        adv.append(tr("adv_npk_mode"))

    rules = master["soil_thresholds"]["soil_fertility_thresholds"]
    macro = rules["macronutrients"]
    critical = master["soil_thresholds"]["critical_levels"]

    # ---------------------------------------------------
    # 2. Organic Carbon
    # ---------------------------------------------------
    OC = safe_num(soil.get("OC"))
    oc_rule = rules["organic_carbon"]["thresholds"]

    if OC is not None:
        if OC < oc_rule["low"]["max"]:
            adv.append(tr("adv_low_oc"))
        elif OC > 0.75:
            adv.append(tr("adv_good_oc"))

    # ---------------------------------------------------
    # 3. Nitrogen
    # ---------------------------------------------------
    SN = safe_num(soil.get("SN"))
    if SN is not None and SN < macro["nitrogen"]["thresholds"]["low"]["max"]:
        adv.append(tr("adv_low_n"))

    # ---------------------------------------------------
    # 4. Phosphorus + pH Interaction
    # ---------------------------------------------------
    SP = safe_num(soil.get("SP"))
    pH = safe_num(soil.get("pH"))

    if SP is not None and SP < 10:
        if pH is not None and pH < 6.5:
            adv.append(tr("adv_low_p_acidic"))
        else:
            adv.append(tr("adv_low_p"))

    # ---------------------------------------------------
    # 5. Micronutrient Advisories
    # ---------------------------------------------------
    if micronutrients:
        for micro in micronutrients.keys():
            msg = tr("adv_micro_detected").replace("{micro}", micro)
            adv.append(msg)

    # ---------------------------------------------------
    # 6. pH related
    # ---------------------------------------------------
    if pH is not None:
        if pH < critical["pH_low"]:
            adv.append(tr("adv_low_ph"))
        elif pH > critical["pH_high"]:
            adv.append(tr("adv_high_ph"))

    # ---------------------------------------------------
    # 7. EC / Salinity
    # ---------------------------------------------------
    EC = safe_num(soil.get("EC"))
    if EC is not None and EC > critical["EC_high"]:
        adv.append(tr("adv_high_ec"))

    return adv
