import streamlit as st
import sys
import os
import pandas as pd
import plotly.express as px
from datetime import datetime

# -------------------------------------------------------
# PATH SETUP
# -------------------------------------------------------
ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(ROOT_DIR)

# -------------------------------------------------------
# IMPORTS
# -------------------------------------------------------
from irrigation.engine import get_irrigation_plan
from irrigation.forecast import predict_next_3_days
from irrigation.helpers import pump_flow
from utils.language import get_text
from utils.theme import load_theme
from utils.sidebar import render_sidebar

# -------------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------------
st.set_page_config(
    page_title="Smart Irrigation Engine",
    page_icon="",
    layout="wide"
)

load_theme()
render_sidebar()

# -------------------------------------------------------
# LANGUAGE HANDLING
# -------------------------------------------------------
lang = st.session_state.get("lang", "English")
T = get_text(lang)
tr = lambda k: T.get(k, k)

# -------------------------------------------------------
# HEADER
# -------------------------------------------------------
st.markdown(f"""
<div class="header-box">
    <h2 style='margin:0;color:white;'>{tr("smart_irrigation")}</h2>
    <p style='margin:0;color:white; opacity:0.9;'>{tr("irrigation_subtitle")}</p>
</div>
""", unsafe_allow_html=True)

# -------------------------------------------------------
# INPUT FORM
# -------------------------------------------------------
with st.form("irrigation_form"):
    col1, col2 = st.columns(2)

    with col1:
        st.subheader(tr("irrigation_location"))
        lat = st.number_input(tr("latitude"), value=28.61, format="%.4f")
        lon = st.number_input(tr("longitude"), value=77.20, format="%.4f")
        crop = st.selectbox(tr("crop"), ["wheat", "rice", "maize", "sugarcane", "soybean", "mustard", "potato"])
        stage = st.selectbox(tr("stage"), ["initial", "mid", "late"])

    with col2:
        st.subheader(tr("irrigation_soil_area"))
        soil = st.selectbox(tr("soil_type"), ["sandy", "loam", "clay"])
        a1, a2 = st.columns([2, 1])
        area_value = a1.number_input(tr("area_value"), value=1.0)
        area_unit = a2.selectbox(tr("area_unit"), ["acre", "hectare", "bigha_up", "sqm"])
        pump_hp = st.selectbox(tr("pump_hp"), ["1_hp", "1.5_hp", "2_hp", "3_hp", "5_hp"])

    submit = st.form_submit_button(tr("run_model"))

# -------------------------------------------------------
# MODEL EXECUTION
# -------------------------------------------------------
if submit:

    if not (-90 <= lat <= 90 and -180 <= lon <= 180):
        st.error("Invalid latitude or longitude.")
        st.stop()
    if area_value <= 0:
        st.error("Area must be greater than 0.")
        st.stop()

    with st.spinner(tr("processing")):
        daily, meta = get_irrigation_plan(lat, lon, crop, stage, soil, area_value, area_unit, pump_hp)
        forecast_df = predict_next_3_days(lat, lon, crop, stage)

    today = daily.iloc[0]
    pump_time = today["pump_hours"] if today["irrigation_needed"] else 0.0
    status_text = tr("status_start_pump") if today["irrigation_needed"] else tr("status_no_water")

    # -------------------------------
    # HEADER CARD
    # -------------------------------
    st.markdown(f"""
    <div class="glass-card" style="padding:20px; margin-top:10px; border-radius:16px;">
        <h3 style="margin:0; color:#1A9E55;"> {tr("irrigation_plan")} — {today['date']}</h3>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric(tr("et0_today"), f"{today['et0_daily']:.2f} mm")
    c2.metric(tr("soil_deficit_mm"), f"{today['cumulative_deficit']:.2f} mm")
    c3.metric(tr("pump_runtime"), f"{pump_time} {tr('units_hours')}")
    c4.metric(tr("action"), status_text)

    st.markdown("---")

    # -------------------------------
    # DECISION BLOCK
    # -------------------------------
    if today["irrigation_needed"]:
        st.error(f"**{tr('status_start_pump')}:** {pump_hp.replace('_', ' ')} — {pump_time} Hours")
        st.caption(f"{tr('status_needed_thresh')} ({today['cumulative_deficit']:.2f} mm > {meta['threshold_mm']} mm)")
    else:
        st.success(tr("status_sufficient"))

    # -------------------------------
    # EXPLANATION
    # -------------------------------
    st.subheader(tr("explanation"))
    if today["irrigation_needed"]:
        st.markdown(f"""
        • {tr("ex_etc_loss")} **{today['ETc']:.2f} mm**  
        • {tr("ex_deficit_reached")} **{today['cumulative_deficit']:.2f} mm**  
        • {tr("ex_threshold")} **{meta['threshold_mm']} mm**
        """)
    else:
        st.markdown(f"""
        • {tr("ex_soil_ok")}  
        • {tr("ex_below_thresh")} (**{today['cumulative_deficit']:.2f} mm** < **{meta['threshold_mm']} mm**)
        """)

    # -------------------------------
    # DAILY TABLE
    # -------------------------------
    st.subheader(tr("daily_table"))
    st.dataframe(daily, use_container_width=True)

    # -------------------------------
    # GRAPHS
    # -------------------------------
    st.subheader(tr("graph_title"))
    g1, g2 = st.columns(2)

    with g1:
        fig1 = px.line(daily, x="date", y="ETc", markers=True, title=tr("graph_etc"))
        st.plotly_chart(fig1, use_container_width=True)

    with g2:
        fig2 = px.line(daily, x="date", y="cumulative_deficit", markers=True, title=tr("graph_deficit"))
        st.plotly_chart(fig2, use_container_width=True)

    # -------------------------------
    # FORECAST SECTION
    # -------------------------------
    st.subheader(tr("forecast_title"))
    if forecast_df is not None and not forecast_df.empty:
        st.dataframe(forecast_df, use_container_width=True)

        fig3 = px.bar(
            forecast_df, x="date", y="ETc_pred",
            title=tr("graph_forecast"), text_auto=True
        )
        st.plotly_chart(fig3, use_container_width=True)

        if meta["predicted_irrigation_day"]:
            st.info(f"{tr('next_irrigation')}: {meta['predicted_irrigation_day']}")

            # Optional future pump time estimate
            next_day = forecast_df[forecast_df["date"] == meta["predicted_irrigation_day"]]
            if not next_day.empty:
                net_et = float(next_day["ETc_pred"].iloc[0] - next_day["precipitation"].iloc[0])
                net_et = max(0, net_et)
                water_liters = net_et * meta["area_m2"]
                runtime = round(water_liters / pump_flow[meta["pump_hp"]], 2)
                st.caption(f"{tr('forecast_runtime')}: {runtime} {tr('units_hours')}")
        else:
            st.info(tr("no_trigger_next"))
    else:
        st.warning(tr("forecast_unavailable"))

    # -------------------------------
    # METADATA
    # -------------------------------
    st.subheader(tr("metadata_title"))
    st.json(meta)
