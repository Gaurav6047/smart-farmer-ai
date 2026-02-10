import pandas as pd
import numpy as np
from datetime import datetime

from irrigation.weather import fetch_weather
from irrigation.forecast import predict_et0_next_3_days
from irrigation.helpers import (
    crop_params, 
    soil_params, 
    pump_flow, 
    area_conversion,
    METADATA
)

def calculate_effective_rain_usda(rain_mm):
    """
    Research Grade: USDA Soil Conservation Service Method.
    P_eff = P_tot * (125 - 0.2 * P_tot) / 125  for P_tot < 250mm
    P_eff = 125 + 0.1 * P_tot                  for P_tot > 250mm
    """
    if rain_mm <= 0:
        return 0.0
    elif rain_mm < 250:
        return rain_mm * (125 - 0.2 * rain_mm) / 125.0
    else:
        return 125.0 + 0.1 * rain_mm

def get_irrigation_plan(
    lat, 
    lon, 
    crop, 
    stage, 
    soil, 
    area_value, 
    area_unit, 
    pump_hp, 
    pump_efficiency, 
    application_efficiency,
    initial_deficit_mm=None  # [NEW] Optional Input
):
    """
    FAO-56 COMPLIANT IRRIGATION ENGINE (Research Grade)
    ---------------------------------------------------
    Performs daily soil water balance accounting (Dual Kc methodology simplified).
    Updated to handle Initial Soil Water Deficit initialization.
    """

    # ======================================================
    # 1. SCIENTIFIC INPUT VALIDATION
    # ======================================================
    if crop not in crop_params:
        raise ValueError(f"Crop '{crop}' parameters missing in physics DB.")
    
    if soil not in soil_params:
        raise ValueError(f"Soil '{soil}' hydraulic properties missing.")
        
    if not (0 < pump_efficiency <= 1.0):
        raise ValueError("Pump efficiency must be between 0 and 1.")

    if not (0 < application_efficiency <= 1.0):
        raise ValueError("Application efficiency must be between 0 and 1.")

    # ======================================================
    # 2. PARAMETER INITIALIZATION
    # ======================================================
    # Crop Params
    kc_value = crop_params[crop]["kc"][stage]
    max_root_depth = crop_params[crop]["Zr_max"]
    p_fraction = crop_params[crop]["p"]
    
    # Root Depth Growth Model (Sigmoidal approximation for stages)
    stage_factors = {
        "initial": 0.3,
        "mid": 0.8, 
        "late": 1.0
    }
    current_stage_factor = stage_factors.get(stage, 0.7)
    zr_current = max_root_depth * current_stage_factor

    # Soil Params (Volumetric)
    fc_vol = soil_params[soil]["fc"]   # m3/m3
    pwp_vol = soil_params[soil]["pwp"] # m3/m3
    
    # RAW Calculation (Readily Available Water)
    # TAW = 1000 * (FC - PWP) * Zr
    taw_mm = 1000.0 * (fc_vol - pwp_vol) * zr_current 
    raw_mm = taw_mm * p_fraction                      

    # ======================================================
    # 3. WEATHER DATA INGESTION
    # ======================================================
    df = fetch_weather(lat, lon)
    if df is None or df.empty:
        raise RuntimeError("Weather data acquisition failed.")

    df["date"] = pd.to_datetime(df["time"]).dt.date
    
    # Aggregation: Hourly -> Daily
    daily = df.groupby("date", as_index=False).agg({
        "et0": "sum",
        "rain": "sum"
    })
    
    # Sanity Check for Physics (FAO limit ~15-20mm/day depending on region)
    if daily["et0"].mean() > 25:
        raise ValueError("ET0 input detected as excessively high (>25mm/day). Check source units.")

    # ======================================================
    # 4. SOIL WATER BALANCE SIMULATION
    # ======================================================
    
    daily["ETc"] = daily["et0"] * kc_value
    
    # USDA SCS Method for Effective Rainfall
    daily["eff_rain"] = daily["rain"].apply(calculate_effective_rain_usda)

    # [UPGRADE] INITIAL DEFICIT SYSTEM ---------------------
    # Logic: Determines starting soil moisture based on input or history.
    
    start_deficit_val = 0.0

    if initial_deficit_mm is not None:
        # A. User Explicit Input
        try:
            start_deficit_val = float(initial_deficit_mm)
        except (ValueError, TypeError):
            start_deficit_val = 0.0 # Fallback safety
    else:
        # B. Automatic Estimation (Last 3 Days)
        # Assumes the crop has been consuming water recently.
        if not daily.empty:
            recent_window = daily.head(3) # Proxy using available window
            # Estimate = Sum(ETc) - Sum(Effective Rain)
            est_loss = recent_window["ETc"].sum()
            est_gain = recent_window["eff_rain"].sum()
            start_deficit_val = est_loss - est_gain

    # C. Scientific Clipping (Boundary Conditions)
    # 1. Deficit cannot be negative (would imply saturation > Field Capacity)
    # 2. Deficit cannot exceed TAW (Total Available Water)
    start_deficit_val = max(0.0, start_deficit_val)
    start_deficit_val = min(start_deficit_val, taw_mm)

    current_deficit = start_deficit_val
    # ------------------------------------------------------
    
    daily["deficit_start"] = 0.0
    daily["deficit_end"] = 0.0
    daily["irrigation_needed"] = False
    
    # [Image of soil water balance diagram]

    for i in daily.index:
        et_out = daily.at[i, "ETc"]
        rain_in = daily.at[i, "eff_rain"]
        
        daily.at[i, "deficit_start"] = current_deficit
        
        # Water Balance Equation: Dr,i = Dr,i-1 - (P - RO) - I - CR + ETc + DP
        # Simplified: New = Old + Out - In
        new_deficit = current_deficit + et_out - rain_in
        
        # Boundary Condition: Deficit cannot be negative (Drainage/Runoff occurs)
        if new_deficit < 0:
            new_deficit = 0.0
            
        daily.at[i, "deficit_end"] = new_deficit
        current_deficit = new_deficit
        
        # Stress Trigger
        if current_deficit >= raw_mm:
            daily.at[i, "irrigation_needed"] = True

    # ======================================================
    # 5. FORECASTING & IRRIGATION SCHEDULING
    # ======================================================
    
    forecast_log = []
    predicted_trigger_date = None
    forecast_metrics = None
    
    try:
        f_df, metrics = predict_et0_next_3_days(lat, lon)
        forecast_metrics = metrics
        
        if f_df is not None:
            future_deficit = current_deficit
            
            for _, row in f_df.iterrows():
                et0_pred = row["et0_pred"]
                etc_pred = max(0.0, et0_pred * kc_value)

                # USDA Method for Forecast Rain
                rain_pred = calculate_effective_rain_usda(row["precipitation"])
                
                future_deficit = future_deficit + etc_pred - rain_pred
                if future_deficit < 0: future_deficit = 0
                
                is_stress = future_deficit >= raw_mm
                
                forecast_log.append({
                    "date": str(row["date"]),
                    "et0_pred": round(et0_pred, 2),
                    "etc_pred": round(etc_pred, 2),
                    "rain_pred": round(row["precipitation"], 2),
                    "deficit_pred": round(future_deficit, 2),
                    "stress_flag": is_stress
                })
                
                if is_stress and predicted_trigger_date is None:
                    predicted_trigger_date = str(row["date"])
                    
    except Exception as e:
        print(f"[Engine] Forecast sub-system error: {e}")

    # ======================================================
    # 6. HYDRAULIC OUTPUT CALCULATION (Current Day)
    # ======================================================
    
    last_day = daily.iloc[-1]
    final_deficit_mm = last_day["deficit_end"]
    
    # Area Calculation
    area_m2 = area_value * area_conversion[area_unit]
    
    net_depth_mm = 0.0
    gross_depth_mm = 0.0
    water_volume_m3 = 0.0
    water_liters_pumped = 0.0
    pump_hours = 0.0

    # Irrigation Logic
    if final_deficit_mm >= raw_mm:
        
        # Management Strategy: Refill to Field Capacity
        # Net depth required to bring soil back to FC
        net_depth_mm = final_deficit_mm 
        
        # Gross Depth (Efficiency Accounting)
        gross_depth_mm = net_depth_mm / application_efficiency
        
        # Volume = Depth(m) * Area(m2)
        water_volume_m3 = (gross_depth_mm / 1000.0) * area_m2
        water_liters_pumped = water_volume_m3 * 1000.0
        
        # Pump Time
        effective_flow = pump_flow[pump_hp] * pump_efficiency
        if effective_flow > 0:
            pump_hours = water_liters_pumped / effective_flow
        
    else:
        net_depth_mm = 0.0
        gross_depth_mm = 0.0
        water_liters_pumped = 0.0
        pump_hours = 0.0

    # ======================================================
    # 7. FINAL METADATA PACKAGING
    # ======================================================
    
    physics_metadata = {
        "model_version": METADATA["version"],
        "parameters": {
            "crop": crop,
            "kc_current": kc_value,
            "root_depth_m": zr_current,
            "depletion_fraction_p": p_fraction,
            "soil_type": soil,
            "fc_vol": fc_vol,
            "pwp_vol": pwp_vol,
            "raw_mm": round(raw_mm, 2),
            "taw_mm": round(taw_mm, 2),
            "area_m2": area_m2  # CRITICAL: Passed for UI calculations
        },
        "efficiency": {
            "application_eff": application_efficiency,
            "pump_eff": pump_efficiency
        },
        "state": {
            "initial_deficit_mm": round(start_deficit_val, 2), # [NEW] Logged for transparency
            "current_deficit_mm": round(final_deficit_mm, 2),
            "irrigation_trigger_mm": round(raw_mm, 2),
            "is_stressed": bool(final_deficit_mm >= raw_mm)
        },
        "recommendation": {
            "net_irrigation_mm": round(net_depth_mm, 2),
            "gross_irrigation_mm": round(gross_depth_mm, 2),
            "water_volume_L": round(water_liters_pumped, 0),
            "pump_hours": round(pump_hours, 2)
        },
        "forecast_metrics": forecast_metrics,
        "forecast_log": forecast_log,
        "predicted_trigger_date": predicted_trigger_date
    }

    return daily, physics_metadata