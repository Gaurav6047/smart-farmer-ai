# ============================================================
# npk_engine.py — NPK Database Lookup Logic
# Implements priority-based fallback for finding data
# ============================================================
from engine.normalizer import normalize_soil, normalize_condition, normalize_season, normalize_float

def get_npk_recommendation(npk_list, season, soil_type=None, condition=None):
    """
    Scans the 'npk' list from the dataset to find the best match.
    Priority 1: Season + Soil + Condition
    Priority 2: Season + Soil
    Priority 3: Season Only
    Priority 4: Season = "Any"
    """
    if not npk_list: return {"N": 0, "P2O5": 0, "K2O": 0}

    # Normalize inputs
    season = normalize_season(season)
    soil_type = normalize_soil(soil_type)
    condition = normalize_condition(condition)

    def extract(row):
        return {
            "N": normalize_float(row.get("N_kg_ha")),
            "P2O5": normalize_float(row.get("P2O5_kg_ha")),
            "K2O": normalize_float(row.get("K2O_kg_ha"))
        }

    # Priority 1: Exact Match (Season + Soil + Cond)
    for row in npk_list:
        if (normalize_season(row.get("Season")) == season and 
            normalize_soil(row.get("Soil_Type")) == soil_type and
            normalize_condition(row.get("Condition")) == condition):
            return extract(row)

    # Priority 2: Season + Soil
    for row in npk_list:
        if (normalize_season(row.get("Season")) == season and 
            normalize_soil(row.get("Soil_Type")) == soil_type):
            return extract(row)

    # Priority 3: Season Only (Condition assumed standard, Soil ignored)
    for row in npk_list:
        if normalize_season(row.get("Season")) == season:
            return extract(row)

    # Priority 4: Fallback "Any" season
    for row in npk_list:
        if normalize_season(row.get("Season")) == "Any":
            return extract(row)

    # No match found
    return {"N": 0, "P2O5": 0, "K2O": 0}