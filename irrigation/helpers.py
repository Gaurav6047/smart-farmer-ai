"""
helpers.py — Scientific Lookup Tables for FAO-56 Physics Engine
---------------------------------------------------------------
Contains:
  • Crop Coefficients (Kc)
  • Crop Physiology (Root Depth, Depletion Fraction p)
  • Soil Hydraulics (FC, PWP)
  • Pump Curves & Area Conversions

Sources:
  - FAO Irrigation and Drainage Paper No. 56
  - Allen et al. (1998)
"""

# ==============================================================================
# 1. CROP COEFFICIENTS (Kc) & PHYSIOLOGY
# ==============================================================================
# Zr_max: Maximum rooting depth (m)
# p:      Soil water depletion fraction for no stress (FAO 56 Table 22)
# ==============================================================================

crop_params = {
    "wheat":     {"kc": {"initial": 0.3, "mid": 1.15, "late": 0.25}, "Zr_max": 1.5, "p": 0.55},
    "rice":      {"kc": {"initial": 1.05, "mid": 1.20, "late": 0.90}, "Zr_max": 0.6, "p": 0.20},
    "maize":     {"kc": {"initial": 0.3,  "mid": 1.20, "late": 0.60}, "Zr_max": 1.2, "p": 0.55},
    "sugarcane": {"kc": {"initial": 0.4,  "mid": 1.25, "late": 0.75}, "Zr_max": 1.5, "p": 0.65},
    "soybean":   {"kc": {"initial": 0.4,  "mid": 1.15, "late": 0.50}, "Zr_max": 1.0, "p": 0.50},
    "mustard":   {"kc": {"initial": 0.35, "mid": 1.05, "late": 0.35}, "Zr_max": 1.2, "p": 0.60},
    "potato":    {"kc": {"initial": 0.5,  "mid": 1.15, "late": 0.75}, "Zr_max": 0.6, "p": 0.35}
}

# Compatibility alias for legacy lookups (if any)
kc_table = {k: v["kc"] for k, v in crop_params.items()}


# ==============================================================================
# 2. SOIL HYDRAULIC PROPERTIES
# ==============================================================================
# Values in Volumetric Water Content (m³/m³)
# FC: Field Capacity
# PWP: Permanent Wilting Point
# Source: Ratliff et al. (1983) / FAO 56 General Soil Types
# ==============================================================================

soil_params = {
    # High infiltration, low retention
    "sandy": {"fc": 0.12, "pwp": 0.05, "desc": "Coarse textured sand"},
    # Balanced retention
    "loam":  {"fc": 0.27, "pwp": 0.14, "desc": "Medium textured loam"},
    # High retention, low infiltration
    "clay":  {"fc": 0.36, "pwp": 0.23, "desc": "Fine textured clay"}
}


# ==============================================================================
# 3. HYDRAULIC & ENGINEERING CONSTANTS
# ==============================================================================

# Pump Discharge (Liters/Hour)
pump_flow = {
    "1_hp":   10000, # Approx for centrifugal surface pump
    "1.5_hp": 15000,
    "2_hp":   20000,
    "3_hp":   28000,
    "5_hp":   45000
}

# Area Conversions (to Square Meters)
area_conversion = {
    "acre": 4046.86,
    "hectare": 10000.0,
    "bigha_up": 2529.0,
    "sqm": 1.0
}

# Model Metadata
METADATA = {
    "methodology": "FAO-56 Penman-Monteith dual crop coefficient",
    "deficit_model": "Daily Root Zone Water Balance",
    "version": "2.2.0-research-patched"
}