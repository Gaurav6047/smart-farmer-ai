"""
weather.py — Weather Fetch Module
----------------------------------

Provides hourly ET₀ (FAO-56 PM) and rainfall from Open-Meteo API.

Returns:
    pandas DataFrame with columns:
      • time
      • et0   (mm/hour)
      • rain  (mm)

This weather source is reproducible and open-access without API key.
"""

import requests
import pandas as pd


def fetch_weather(lat, lon):
    """
    Fetch hourly FAO-56 ET0 & precipitation from Open-Meteo.

    Args:
        lat (float): Latitude
        lon (float): Longitude

    Returns:
        pandas.DataFrame: Hourly weather data (time, et0, rain)

    Raises:
        RuntimeError: If weather API fails
    """

    url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}&longitude={lon}"
        "&hourly=et0_fao_evapotranspiration,precipitation"
        "&timezone=auto"
    )

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
    except Exception as e:
        raise RuntimeError(f"Failed to fetch weather data: {e}")

    if "hourly" not in data:
        raise RuntimeError("Weather API returned invalid format.")

    hourly = data["hourly"]

    df = pd.DataFrame({
        "time": hourly["time"],
        "et0": hourly["et0_fao_evapotranspiration"],  # mm/hour
        "rain": hourly["precipitation"]               # mm
    })

    return df
