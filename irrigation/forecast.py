"""
forecast.py — Atmospheric Demand Forecasting (ET0)
--------------------------------------------------
PHYSICS UPDATE:
  - REMOVED direct ETc prediction (Scientifically invalid).
  - IMPLEMENTED ET0 (Reference Evapotranspiration) forecasting.
  - ML Model now predicts atmospheric demand solely based on weather.
  - [PATCH 5] Added RMSE + MAE Validation for Research Compliance.
  - [PATCH 6] Added Caching for Performance Optimization.
"""

import requests
import pandas as pd
import numpy as np
import streamlit as st
from datetime import datetime, timedelta
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error

# ============================================================
# 1) HISTORICAL WEATHER FETCH (Training Data)
# ============================================================

# Cache data fetch to avoid API spamming on re-runs
@st.cache_data(ttl=3600) 
def fetch_training_data(lat, lon, days=60):
    """Fetches historical ET0 for model training (Open-Meteo Archive)."""
    
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
        raw = requests.get(url, timeout=20).json()
        if "error" in raw:
            raise RuntimeError(f"API Error: {raw.get('reason')}")
    except Exception as e:
        print(f"[Forecast] History fetch failed: {e}")
        return None

    df = pd.DataFrame(raw["hourly"])
    df["time"] = pd.to_datetime(df["time"])
    df["date"] = df["time"].dt.date
    
    # Validation: Remove partial days or NaNs
    df = df.dropna()
    return df

# ============================================================
# 2) FEATURE ENGINEERING (Daily Aggregation)
# ============================================================

def prepare_features(hourly_df):
    """Aggregates hourly physics data into daily training features."""
    
    daily = hourly_df.groupby("date", as_index=False).agg({
        "temperature_2m": "mean",
        "relative_humidity_2m": "mean",
        "windspeed_10m": "mean",
        "shortwave_radiation": "sum",
        "et0_fao_evapotranspiration": "sum", # TARGET VARIABLE
        "precipitation": "sum"
    })

    daily["doy"] = pd.to_datetime(daily["date"]).dt.dayofyear
    
    # Physics Sanity Check: ET0 cannot be negative
    daily = daily[daily["et0_fao_evapotranspiration"] >= 0]
    
    return daily.sort_values("date")

# ============================================================
# 3) ML MODEL (ET0 PREDICTOR)
# ============================================================

# Cache the trained model! Retraining on every click is redundant.
@st.cache_resource
def train_et0_model(daily_df):
    """
    Trains XGBoost on atmospheric variables to predict ET0.
    [PATCH 5] Computes and returns RMSE and MAE validation metrics.
    """
    
    features = ["temperature_2m", "relative_humidity_2m", "windspeed_10m", 
                "shortwave_radiation", "doy", "precipitation"]
    target = "et0_fao_evapotranspiration"

    X = daily_df[features]
    y = daily_df[target]

    # --- Scientific Validation Split (Last 20% for temporal validation) ---
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, shuffle=False)

    model = XGBRegressor(
        n_estimators=200,
        learning_rate=0.08,
        max_depth=5,
        objective="reg:squarederror",
        n_jobs=-1,
        random_state=42
    )
    
    # 1. Train on training set to compute metrics
    model.fit(X_train, y_train)
    preds = model.predict(X_test)
    
    rmse = np.sqrt(mean_squared_error(y_test, preds))
    mae = mean_absolute_error(y_test, preds)
    
    metrics = {
        "rmse_et0": float(rmse),
        "mae_et0": float(mae)
    }

    # 2. Retrain on FULL dataset for production forecasting
    model.fit(X, y)
    
    return model, features, metrics

# ============================================================
# 4) FORECAST GENERATION
# ============================================================

def predict_et0_next_3_days(lat, lon):
    """
    Orchestrates the forecast pipeline:
    1. Fetch History -> 2. Train Model -> 3. Fetch Forecast Weather -> 4. Predict ET0
    
    Returns:
        tuple: (forecast_dataframe, metrics_dictionary)
    """
    
    # A. Get Training Data
    hist_df = fetch_training_data(lat, lon)
    if hist_df is None or len(hist_df) < 14:
        print("[Forecast] Insufficient history for training.")
        return None, None
        
    training_data = prepare_features(hist_df)
    
    # B. Train Model & Get Validation Metrics
    # (Cached via decorators on the function itself)
    model, feature_names, metrics = train_et0_model(training_data)
    
    # C. Get Future Atmospheric Conditions
    url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}&longitude={lon}"
        "&hourly=temperature_2m,relative_humidity_2m,windspeed_10m,"
        "shortwave_radiation,precipitation"
        "&timezone=auto&forecast_days=4"
    )
    
    try:
        resp = requests.get(url, timeout=10).json()
        future_hourly = pd.DataFrame(resp["hourly"])
        future_hourly["time"] = pd.to_datetime(future_hourly["time"])
        future_hourly["date"] = future_hourly["time"].dt.date
    except Exception as e:
        print(f"[Forecast] Future weather fetch failed: {e}")
        return None, metrics

    # D. Aggregate Future Data
    future_daily = future_hourly.groupby("date", as_index=False).agg({
        "temperature_2m": "mean",
        "relative_humidity_2m": "mean",
        "windspeed_10m": "mean",
        "shortwave_radiation": "sum",
        "precipitation": "sum"
    })
    
    future_daily["doy"] = pd.to_datetime(future_daily["date"]).dt.dayofyear
    future_daily = future_daily.head(3) # Strict 3-day window

    # E. Predict ET0
    X_future = future_daily[feature_names]
    et0_pred = model.predict(X_future)
    
    # Apply Physics Constraints (ET0 >= 0)
    future_daily["et0_pred"] = np.maximum(et0_pred, 0.0)
    
    return future_daily[["date", "et0_pred", "precipitation"]], metrics