"""
forecast.py — 3-Day FAO-ETc Forecast Model (Fully Corrected)
------------------------------------------------------------

Predicts next 3 days ETc using:
    • 45-day historical weather (Open-Meteo Archive)
    • Daily aggregated features
    • XGBoostRegressor (deterministic)
    • FAO-56 Kc (crop-stage specific)
"""

import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from xgboost import XGBRegressor
from irrigation.helpers import kc_table


# ============================================================
# 1) Fetch Historical Weather (past 45 days)
# ============================================================

def fetch_historical_weather(lat, lon, days=45):
    end_date = datetime.utcnow().date()
    start_date = end_date - timedelta(days=days)

    url = (
        f"https://archive-api.open-meteo.com/v1/archive?"
        f"latitude={lat}&longitude={lon}"
        f"&start_date={start_date}&end_date={end_date}"
        "&hourly=temperature_2m,relative_humidity_2m,windspeed_10m,"
        "shortwave_radiation,et0_fao_evapotranspiration,precipitation"
        "&timezone=auto"
    )

    try:
        raw = requests.get(url, timeout=10).json()
    except:
        raise RuntimeError("Historical weather API failed.")

    if "hourly" not in raw:
        raise RuntimeError("Historical weather missing 'hourly'.")

    df = pd.DataFrame(raw["hourly"])
    df["time"] = pd.to_datetime(df["time"], errors="coerce")
    df.dropna(subset=["time"], inplace=True)
    df["date"] = df["time"].dt.date

    return df


# ============================================================
# 2) Prepare Daily Data (FAO-ETc Target)
# ============================================================

def prepare_training_data(df, kc_value):
    daily = df.groupby("date", as_index=False).agg({
        "temperature_2m": "mean",
        "relative_humidity_2m": "mean",
        "windspeed_10m": "mean",
        "shortwave_radiation": "sum",
        "et0_fao_evapotranspiration": "sum",
        "precipitation": "sum",
    })

    daily["doy"] = pd.to_datetime(daily["date"]).dt.dayofyear
    daily["ETc"] = daily["et0_fao_evapotranspiration"] * kc_value

    daily = daily.dropna()

    if len(daily) < 10:
        raise RuntimeError("Insufficient historical weather data.")

    return daily


# ============================================================
# 3) Train ML Model (Deterministic XGBoost)
# ============================================================

def train_ETc_model(daily):
    features = [
        "temperature_2m",
        "relative_humidity_2m",
        "windspeed_10m",
        "shortwave_radiation",
        "precipitation",
        "doy",
    ]

    X = daily[features]
    y = daily["ETc"]

    model = XGBRegressor(
        n_estimators=250,
        learning_rate=0.05,
        max_depth=6,
        subsample=0.85,
        colsample_bytree=0.85,
        objective="reg:squarederror",
        random_state=42,
        n_jobs=1
    )

    model.fit(X, y)
    return model, features


# ============================================================
# 4) Fetch Next 3 Days (Forecast Weather)
# ============================================================

def fetch_future_weather(lat, lon):
    url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}&longitude={lon}"
        "&hourly=temperature_2m,relative_humidity_2m,windspeed_10m,"
        "shortwave_radiation,precipitation"
        "&timezone=auto"
    )

    try:
        raw = requests.get(url, timeout=10).json()
    except:
        raise RuntimeError("Future weather API failed.")

    if "hourly" not in raw:
        raise RuntimeError("Future weather missing 'hourly'.")

    df = pd.DataFrame(raw["hourly"])
    df["time"] = pd.to_datetime(df["time"], errors="coerce")
    df.dropna(subset=["time"], inplace=True)
    df["date"] = df["time"].dt.date

    return df


# ============================================================
# 5) Predict Next 3 Days ETc
# ============================================================

def predict_next_3_days(lat, lon, crop, stage):

    # Validate crop/stage
    if crop not in kc_table:
        raise ValueError(f"Unknown crop '{crop}'")
    if stage not in kc_table[crop]:
        raise ValueError(f"Invalid stage '{stage}'")

    kc_value = kc_table[crop][stage]

    # Historical → training
    df_hist = fetch_historical_weather(lat, lon)
    daily = prepare_training_data(df_hist, kc_value)
    model, features = train_ETc_model(daily)

    # Future weather
    df_future = fetch_future_weather(lat, lon)

    # Daily aggregation
    pred = df_future.groupby("date", as_index=False).agg({
        "temperature_2m": "mean",
        "relative_humidity_2m": "mean",
        "windspeed_10m": "mean",
        "shortwave_radiation": "sum",
        "precipitation": "sum",
    })

    pred["doy"] = pd.to_datetime(pred["date"]).dt.dayofyear

    # Only next 3 days
    pred = pred.head(3)

    # Predict ETc — FIXED CLIP
    y_hat = model.predict(pred[features])
    y_hat = np.clip(y_hat, 0, None)   # THIS FIXES YOUR ERROR

    pred["ETc_pred"] = y_hat.astype(float)

    return pred
