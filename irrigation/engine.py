import pandas as pd
from datetime import datetime


from irrigation.weather import fetch_weather
from irrigation.forecast import predict_next_3_days
from irrigation.helpers import kc_table, soil_thresholds, pump_flow, area_conversion


def get_irrigation_plan(lat, lon, crop, stage, soil, area_value, area_unit, pump_hp):
    """
    Publishable-Grade Irrigation Decision Engine (with 3-Day Forecast)
    ------------------------------------------------------------------
    Implements:
      • FAO-56 Penman–Monteith ET₀ (Open-Meteo)
      • FAO-56 Crop Coefficient ETc Model
      • Rain-adjusted ETc (net_ETc)
      • FAO Cumulative Soil Water Deficit Model (CWD)
      • Water Requirement Estimation (mm → liters)
      • Pump Hour Calculation
      • 3-Day Forecasted ETc Model (XGBoost)
      • Predictive Irrigation Trigger Logic
      • Explanation strings + metadata (publication-ready)
    """

    # ============================
    # INPUT VALIDATION
    # ============================
    if crop not in kc_table:
        raise ValueError(f"Unknown crop '{crop}'. Available: {list(kc_table.keys())}")

    if stage not in kc_table[crop]:
        raise ValueError(f"Invalid stage '{stage}'. Must be one of: {list(kc_table[crop].keys())}")

    if soil not in soil_thresholds:
        raise ValueError(f"Unknown soil '{soil}'. Must be one of: {list(soil_thresholds.keys())}")

    if pump_hp not in pump_flow:
        raise ValueError(f"Invalid pump_hp '{pump_hp}'. Available: {list(pump_flow.keys())}")

    if area_unit not in area_conversion:
        raise ValueError(f"Unknown area unit '{area_unit}'.")


    # ============================
    # FETCH WEATHER
    # ============================
    df = fetch_weather(lat, lon)
    if df is None or len(df) == 0:
        raise ValueError("Weather API returned empty data.")

    df["date"] = pd.to_datetime(df["time"]).dt.date


    # ============================
    # DAILY AGGREGATION
    # ============================
    daily = df.groupby("date", as_index=False).agg({
        "et0": "sum",
        "rain": "sum"
    })
    daily.rename(columns={"et0": "et0_daily", "rain": "rain_daily"}, inplace=True)


    # ============================
    # ETc CALCULATION
    # ============================
    kc_value = kc_table[crop][stage]
    daily["ETc"] = daily["et0_daily"] * kc_value


    # ============================
    # net_ETc
    # ============================
    daily["net_ETc"] = (daily["ETc"] - daily["rain_daily"]).clip(lower=0)


    # ============================
    # AREA
    # ============================
    area_m2 = area_value * area_conversion[area_unit]


    # ============================
    # WATER LITERS
    # ============================
    daily["water_liters"] = daily["net_ETc"] * area_m2


    # ============================
    # PUMP HOURS
    # ============================
    flow_rate = pump_flow[pump_hp]
    daily["pump_hours"] = (daily["water_liters"] / flow_rate).round(2)


    # ============================
    # CUMULATIVE DEFICIT MODEL
    # ============================
    threshold = soil_thresholds[soil]
    daily["cumulative_deficit"] = 0.0
    daily["irrigation_needed"] = False

    deficit = 0.0
    explanations = []

    for i in range(len(daily)):
        deficit += daily.loc[i, "net_ETc"]
        daily.loc[i, "cumulative_deficit"] = deficit

        if deficit > threshold:
            daily.loc[i, "irrigation_needed"] = True
            deficit = 0.0  # reset bucket

        # explanation string
        expl = (
            f"ET0={daily.loc[i,'et0_daily']:.2f} mm, "
            f"Kc={kc_value}, "
            f"ETc={daily.loc[i,'ETc']:.2f} mm, "
            f"Rain={daily.loc[i,'rain_daily']:.2f} mm, "
            f"Deficit={daily.loc[i,'cumulative_deficit']:.2f} mm, "
            f"Threshold={threshold} mm"
        )
        explanations.append(expl)

    daily["explanation"] = explanations


    # ======================================================
    # 3-DAY ETc FORECAST + FUTURE IRRIGATION PREDICTION
    # ======================================================
    try:
        forecast_df = predict_next_3_days(lat, lon, crop, stage)
    except Exception as e:
        forecast_df = None


    predicted_trigger_day = None

    if forecast_df is not None:
        # predicted net_ETc = ETc_pred (rain assumed minimal)
        forecast_df["net_ETc_pred"] = (forecast_df["ETc_pred"] - forecast_df["precipitation"]).clip(lower=0)

        # start with latest observed deficit
        future_def = float(daily["cumulative_deficit"].iloc[-1])

        trigger_found = False
        future_results = []

        for i in range(len(forecast_df)):
            future_def += forecast_df.loc[i, "net_ETc_pred"]

            row = {
                "date": str(forecast_df.loc[i, "date"]),
                "ETc_pred": float(forecast_df.loc[i, "ETc_pred"]),
                "cumulative_deficit_pred": float(future_def)
            }
            future_results.append(row)

            if (not trigger_found) and future_def > threshold:
                predicted_trigger_day = forecast_df.loc[i, "date"]
                trigger_found = True

        forecast_output = future_results
    else:
        forecast_output = None


    # ============================
    # METADATA
    # ============================
    metadata = {
        "lat": lat,
        "lon": lon,
        "crop": crop,
        "stage": stage,
        "soil": soil,
        "area_value": area_value,
        "area_unit": area_unit,
        "area_m2": area_m2,
        "pump_hp": pump_hp,
        "threshold_mm": threshold,
        "data_source": "Open-Meteo API (FAO ET0 PM)",
        "method": "FAO-56 Penman–Monteith + Kc Model + CWD + ML Forecast",
        "generated_on": str(datetime.utcnow()),
        "forecast": forecast_output,
        "predicted_irrigation_day": str(predicted_trigger_day) if predicted_trigger_day else None
    }

    return daily, metadata
