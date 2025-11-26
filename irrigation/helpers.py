"""
helpers.py — Static Parameters for the Publishable Irrigation Engine
--------------------------------------------------------------------

This module contains all static lookup tables used by the irrigation model:
  • Crop coefficient (Kc) values — FAO-56 standard
  • Soil water-holding thresholds (mm)
  • Pump flow rates (L/hr)
  • Area conversion factors (to m²)
  • Version metadata for reproducibility
"""

# ===============================
# Crop Coefficient (Kc) TABLE
# FAO-56 Standard Values
# ===============================

kc_table = {
    "wheat":     {"initial": 0.7, "mid": 1.15, "late": 0.25},
    "rice":      {"initial": 1.05, "mid": 1.20, "late": 0.90},
    "maize":     {"initial": 0.3, "mid": 1.20, "late": 0.55},
    "sugarcane": {"initial": 0.4, "mid": 1.25, "late": 0.75},
    "soybean":   {"initial": 0.4, "mid": 1.15, "late": 0.50},
    "mustard":   {"initial": 0.35, "mid": 1.05, "late": 0.35},
    "potato":    {"initial": 0.5, "mid": 1.15, "late": 0.5}
}


# ===============================
# Soil Thresholds (mm)
# Field capacity deficit before irrigation is triggered
# ===============================

soil_thresholds = {
    "sandy": 10,   # low WHC
    "loam": 15,    # medium WHC
    "clay": 22     # high WHC
}

# ===============================
# Pump Flow Rates (L/hour)
# ===============================

pump_flow = {
    "1_hp": 2000,
    "1.5_hp": 3000,
    "2_hp": 4000,
    "3_hp": 6000,
    "5_hp": 9000
}

# ===============================
# Area Conversion Factors
# Convert area units → square meters (m²)
# ===============================

area_conversion = {
    "acre": 4046.86,
    "hectare": 10000,
    "bigha_up": 2529,
    "sqm": 1
}


# ===============================
# Metadata (for publications)
# ===============================

model_version = "IrrigationEngine-2025-v1.0"
data_source = "Open-Meteo (FAO ET0 PM)"
