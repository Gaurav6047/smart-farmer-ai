# ====================================================================
# normalizer.py — SmartFert Normalizer
# ====================================================================

VALID_SEASONS = ["Kharif", "Rabi", "Zaid", "Perennial", "Any"]
VALID_CONDITIONS = ["Irrigated", "Rainfed", "Standard", "Hybrid", "Coastal", "Transplanted", "Direct-seeded", "Perennial", "Any"]

def normalize_state(state):
    return str(state).strip() if state else ""

def normalize_crop(crop):
    return str(crop).strip() if crop else ""

def normalize_season(season):
    if not season: return "Any"
    s = str(season).strip()
    if s in VALID_SEASONS: return s
    
    mapper = {"kharif": "Kharif", "rabi": "Rabi", "zaid": "Zaid", "perennial": "Perennial"}
    return mapper.get(s.lower(), "Any")

def normalize_condition(cond):
    if not cond: return "Standard"
    c = str(cond).strip()
    if c in VALID_CONDITIONS: return c
    
    # Simple map logic
    for v in VALID_CONDITIONS:
        if c.lower() == v.lower():
            return v
    return "Standard"

SOIL_NORMALIZATION = {
    "red": "red", "red soil": "red", "red sandy loam": "red",
    "black": "black", "black soil": "black", "vertisol": "black",
    "alluvial": "alluvial", "loam": "alluvial",
    "laterite": "lateritic", "lateritic": "lateritic",
    "sandy": "sandy", "coastal": "sandy",
}

def normalize_soil(soil_type):
    if not soil_type: return "unknown"
    s = str(soil_type).strip().lower()
    
    if s in SOIL_NORMALIZATION: return SOIL_NORMALIZATION[s]
    
    if "red" in s: return "red"
    if "black" in s or "vertisol" in s: return "black"
    if "alluvial" in s: return "alluvial"
    if "laterit" in s: return "lateritic"
    if "sand" in s: return "sandy"
    
    return s

def normalize_float(val):
    try:
        return float(val) if val is not None and str(val).strip() != "" else 0.0
    except:
        return 0.0