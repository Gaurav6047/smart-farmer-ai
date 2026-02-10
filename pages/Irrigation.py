import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import os
import sys

# -------------------------------------------------------
# PATH SETUP
# -------------------------------------------------------
ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
sys.path.append(ROOT_DIR)

# =====================================================================
# 0. CONFIG & INLINE UTILS
# =====================================================================
st.set_page_config(
    page_title="Smart Irrigation Engine",
    page_icon="💧",
    layout="wide"
)

# ✅ RENAMED to avoid conflict with utils.theme
def load_local_css():
    st.markdown("""
    <style>
        /* Header Box Styling */
        .header-box {
            padding: 2rem;
            border-radius: 15px;
            background: linear-gradient(90deg, #0288d1 0%, #01579b 100%);
            color: white !important;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            margin-bottom: 2rem;
        }
        .header-box h2, .header-box p {
            color: white !important;
        }

        /* Glass Card Styling */
        .glass-card {
            background-color: #f0f4f8;
            border: 1px solid #e1e4e8;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }

        /* Metric Card Visibility Fix */
        .stMetric {
            background-color: #ffffff !important;
            padding: 10px;
            border-radius: 8px;
            border: 1px solid #eee;
            text-align: center;
            color: #000000 !important;
        }
        
        [data-testid="stMetricLabel"] {
            color: #444444 !important; /* Dark Grey for Label */
        }
        [data-testid="stMetricValue"] {
            color: #000000 !important; /* Pure Black for Value */
        }
        [data-testid="stMetricDelta"] {
            font-weight: bold;
        }
    </style>
    """, unsafe_allow_html=True)

# =====================================================================
# 1. IMPORTS & SETUP
# =====================================================================
try:
    from irrigation.engine import get_irrigation_plan
    from irrigation.helpers import pump_flow, area_conversion
    from utils.sidebar import render_sidebar
    from utils.theme import load_theme
    #  Import get_text from utils.language (Centralized Management)
    from utils.language import get_text
except ImportError:
    st.error("🚨 Critical Error: 'irrigation', 'utils' or 'language' package not found. Ensure files are present.")
    st.stop()

#  Load BOTH Themes (Global + Local)
load_theme()       # Loads Sidebar defaults
load_local_css()   # Loads Header & Card styles

# =====================================================================
# 2. SIDEBAR & LANGUAGE CONTROL
# =====================================================================
#  FIX: Don't expect return value, read from Session State
render_sidebar()

# Get language from session state (set by sidebar.py), default to English
language = st.session_state.get("lang", "English")

#  Prepare Language Key for language.py
lang_key = "Hindi" if "Hindi" in language else "English"

# Load Utils with Selected Language
T = get_text(lang_key)
tr = lambda k: T.get(k, k)

# =====================================================================
# 3. DISPLAY MAPPERS (For Bilingual UI Options)
# =====================================================================
# These map the Engine Keys (English) -> Display Text (Bilingual/Hindi)

def format_crop(val):
    map_hi = {
        "wheat": "गेहूँ (Wheat)", "rice": "चावल (Rice)", "maize": "मक्का (Maize)",
        "sugarcane": "गन्ना (Sugarcane)", "soybean": "सोयाबीन (Soybean)",
        "mustard": "सरसों (Mustard)", "potato": "आलू (Potato)"
    }
    return map_hi.get(val, val) if "Hindi" in language else val.title()

def format_stage(val):
    map_hi = {"initial": "प्रारंभिक (Initial)", "mid": "मध्य (Mid)", "late": "अंतिम (Late)"}
    return map_hi.get(val, val) if "Hindi" in language else val.title()

def format_soil(val):
    map_hi = {"sandy": "रेतीली (Sandy)", "loam": "दुमट (Loam)", "clay": "चिकनी (Clay)"}
    return map_hi.get(val, val) if "Hindi" in language else val.title()

# =====================================================================
# 4. HEADER
# =====================================================================
st.markdown(f"""
<div class="header-box">
    <h2 style='margin:0;color:white;'>{tr("smart_irrigation")}</h2>
    <p style='margin:0;color:white; opacity:0.9;'>{tr("irrigation_subtitle")}</p>
</div>
""", unsafe_allow_html=True)

# =====================================================================
# 5. INPUT FORM
# =====================================================================
with st.form("irrigation_form"):

    col1, col2 = st.columns(2)

    with col1:
        st.subheader(tr("irrigation_location"))
        lat = st.number_input(tr("latitude"), value=28.61, format="%.4f")
        lon = st.number_input(tr("longitude"), value=77.20, format="%.4f")
        
        # Crop & Stage with formatters
        crop_opts = ["wheat", "rice", "maize", "sugarcane", "soybean", "mustard", "potato"]
        crop = st.selectbox(tr("crop"), crop_opts, format_func=format_crop)
        
        stage_opts = ["initial", "mid", "late"]
        stage = st.selectbox(tr("stage"), stage_opts, index=1, format_func=format_stage)

    with col2:
        st.subheader(tr("irrigation_soil_area"))
        
        soil_opts = ["sandy", "loam", "clay"]
        soil = st.selectbox(tr("soil_type"), soil_opts, index=1, format_func=format_soil)
        
        a1, a2 = st.columns([2, 1])
        area_value = a1.number_input(tr("area_value"), value=1.0, min_value=0.1)
        
        # Unit options
        area_unit = a2.selectbox(tr("area_unit"), ["acre", "hectare", "bigha_up", "sqm"], index=1)
        
        # Pump Selection
        p1, p2 = st.columns([1, 1])
        pump_hp = p1.selectbox(tr("pump_hp"), ["1_hp", "1.5_hp", "2_hp", "3_hp", "5_hp"], index=2)
        
        # Pump Efficiency (Indian Context)
        pump_cond_label = p2.selectbox(
            tr("pump_cond"),
            [
                "Submersible / New (90%)", 
                "Monoblock / Average (70%)", 
                "Old / Rewound (50%)"
            ],
            index=1
        )
        
        pump_eff_map = {
            "Submersible / New (90%)": 0.90,
            "Monoblock / Average (70%)": 0.70,
            "Old / Rewound (50%)": 0.50
        }
        pump_efficiency = pump_eff_map[pump_cond_label]

        # Application Efficiency
        irr_method_label = st.selectbox(
            tr("irr_method"),
            [
                "Surface/Flood (60%)", 
                "Sprinkler (75%)", 
                "Drip (90%)"
            ],
            index=0
        )
        app_eff_map = {
            "Surface/Flood (60%)": 0.60,
            "Sprinkler (75%)": 0.75,
            "Drip (90%)": 0.90
        }
        application_efficiency = app_eff_map[irr_method_label]

        # [NEW] Initial Deficit Input (Optional)
        st.markdown("---")
        st.caption(tr("opt_init_cond"))
        initial_deficit_input = st.number_input(
            tr("init_deficit_lbl"), 
            min_value=0.0, 
            value=0.0, 
            help=tr("init_deficit_hlp")
        )
        
        use_auto_deficit = st.checkbox(tr("auto_est_chk"), value=True)
        final_init_deficit = None if use_auto_deficit else initial_deficit_input

    submit = st.form_submit_button(tr("run_model"), type="primary")

# =====================================================================
# 6. MODEL EXECUTION
# =====================================================================
if submit:

    if not (-90 <= lat <= 90 and -180 <= lon <= 180):
        st.error(tr("err_inv_coords"))
        st.stop()

    with st.spinner(tr("processing")):
        try:
            #  Call Updated Engine with Efficiency Params AND Initial Deficit
            daily, meta = get_irrigation_plan(
                lat, lon, crop, stage, soil, area_value, area_unit, 
                pump_hp, pump_efficiency, application_efficiency,
                initial_deficit_mm=final_init_deficit
            )
        except Exception as e:
            st.error(f"{tr('err_engine_prefix')}: {e}")
            st.stop()

    # -------------------------------------------------------------
    #  FIX: DATE & DATA SYNCHRONIZATION
    # -------------------------------------------------------------
    # 1. Sort Data by Date
    daily = daily.sort_values("date").reset_index(drop=True)
    
    # 2.  GET TODAY'S ROW (Index 0) - This is the current date
    today = daily.iloc[0]

    # 3. Parameters
    rec = meta["recommendation"] # This is usually end-state recommendation
    params = meta["parameters"]
    metrics = meta.get("forecast_metrics")
    threshold_raw = params["raw_mm"] 

    # 4.  RE-EVALUATE STATUS FOR *TODAY* (First Row)
    # The 'state' in meta might be for the end of the simulation.
    # We want to display what is happening TODAY (Date 0).
    
    current_deficit = float(today['deficit_end'])
    is_stressed = current_deficit > threshold_raw
    
    if not is_stressed:
        # NO ACTION TODAY
        pump_time = 0.0
        status_text = tr("status_no_water")
        status_color = "#388e3c"
        rec_display = {
            "pump_hours": 0.0,
            "gross_irrigation_mm": 0.0,
            "water_volume_L": 0.0
        }
    else:
        # ACTION NEEDED TODAY
        status_text = tr("status_start_pump")
        status_color = "#d32f2f"
        
        # Calculate Logic on the Fly for Today's Deficit
        # Formula: Gross Depth = Deficit / App Efficiency
        gross_irrigation_mm = current_deficit / application_efficiency
        
        # Volume (L) = Depth (m) * Area (m2) * 1000
        # params["area_m2"] comes from engine logic
        water_volume_L = (gross_irrigation_mm / 1000.0) * params["area_m2"] * 1000.0
        
        # Flow (L/hr) = Pump Flow * Pump Efficiency
        effective_flow = pump_flow[pump_hp] * pump_efficiency
        
        if effective_flow > 0:
            pump_time = round(water_volume_L / effective_flow, 2)
        else:
            pump_time = 0.0
            
        rec_display = {
            "pump_hours": pump_time,
            "gross_irrigation_mm": round(gross_irrigation_mm, 2),
            "water_volume_L": round(water_volume_L, 2)
        }

    # -------------------------------
    # RESULT CARD
    # -------------------------------
    st.markdown(f"""
    <div class="glass-card" style="padding:20px; margin-top:10px; border-radius:16px; border-left: 10px solid {status_color};">
        <h3 style="margin:0; color:#333;">{tr("irrigation_plan")} — {today['date']}</h3>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric(tr("et0_today"), f"{today['et0']:.2f} mm") 
    c2.metric(tr("soil_deficit_mm"), f"{current_deficit:.2f} mm", help=f"{tr('lbl_threshold')}: {threshold_raw} mm")
    c3.metric(tr("pump_runtime"), f"{pump_time} {tr('units_hours')}")
    c4.markdown(f"<h3 style='color:{status_color}; text-align:center;'>{status_text}</h3>", unsafe_allow_html=True)

    st.markdown("---")

    # -------------------------------
    # EXPLANATION & VALIDATION
    # -------------------------------
    e1, e2 = st.columns([3, 2])
    
    with e1:
        st.subheader(tr("explanation"))
        if is_stressed:
            st.error(f"**{tr('status_needed_thresh')}**")
            st.markdown(f"""
            - **{tr('ex_etc_loss')}** {today['ETc']:.2f} mm
            - **{tr('ex_deficit_reached')}** {current_deficit:.2f} mm
            - **{tr('ex_threshold')}** {threshold_raw} mm
            
            *{tr('msg_stress_trigger')}*
            """)
        else:
            st.success(f"**{tr('status_sufficient')}**")
            st.markdown(f"""
            - **{tr('ex_soil_ok')}**
            - **{tr('ex_below_thresh')}** {current_deficit:.2f} mm < {threshold_raw} mm
            """)

    with e2:
        st.subheader(tr("accuracy_metrics"))
        if metrics:
            st.info(tr("accuracy_metrics"))
            m1, m2 = st.columns(2)
            m1.metric("RMSE (ET0)", f"{metrics.get('rmse_et0', 'N/A')} mm", delta_color="off")
            m2.metric("MAE (ET0)", f"{metrics.get('mae_et0', 'N/A')} mm", delta_color="off")
        else:
            st.warning(tr("forecast_unavailable"))

    # -------------------------------
    # GRAPHS
    # -------------------------------
    st.subheader(tr("graph_title"))
    g1, g2 = st.columns(2)

    with g1:
        fig1 = px.line(daily, x="date", y="ETc", markers=True, title=tr("graph_etc"))
        fig1.update_traces(line_color='#FF6D00')
        st.plotly_chart(fig1, use_container_width=True)

    with g2:
        fig2 = px.line(daily, x="date", y="deficit_end", markers=True, title=tr("graph_deficit"))
        # Add threshold line
        fig2.add_hline(y=threshold_raw, line_dash="dash", line_color="red", annotation_text="RAW Threshold")
        fig2.update_layout(yaxis_title="Deficit (mm)")
        st.plotly_chart(fig2, use_container_width=True)

    # -------------------------------
    # FORECAST SECTION
    # -------------------------------
    st.subheader(tr("forecast_title"))

    forecast_log = meta.get("forecast_log", [])

    if forecast_log:
        forecast_df = pd.DataFrame(forecast_log)
        
        # Visualizing Forecast
        f1, f2 = st.columns([2, 1])
        with f1:
            if "etc_pred" in forecast_df.columns:
                fig3 = px.bar(
                    forecast_df, x="date", y="etc_pred",
                    title=tr("graph_forecast"), text_auto=True,
                    labels={'etc_pred': tr("graph_forecast")}
                )
                fig3.update_traces(marker_color='#0277BD')
                st.plotly_chart(fig3, use_container_width=True)
        
        with f2:
            st.markdown(f"**{tr('next_irrigation')}**")
            
            predicted_date = meta.get("predicted_trigger_date")
            
            trigger_valid = False
            if predicted_date:
                # Verify against forecast log
                trigger_day_row = forecast_df[forecast_df["date"] == predicted_date]
                if not trigger_day_row.empty:
                    if trigger_day_row["stress_flag"].iloc[0]:
                        trigger_valid = True

            if trigger_valid:
                st.error(f" **{predicted_date}**")
                
                # Derive Area strictly from METADATA
                engine_area_m2 = params["area_m2"]

                # Get predicted future deficit
                trigger_day_row = forecast_df[forecast_df["date"] == predicted_date]
                future_deficit = float(trigger_day_row["deficit_pred"].iloc[0])
                
                #  PHYSICS CALCS
                gross_depth_mm = future_deficit / application_efficiency
                water_L = (gross_depth_mm / 1000.0) * engine_area_m2 * 1000.0
                effective_flow = pump_flow[pump_hp] * pump_efficiency
                
                est_runtime = 0.0
                if effective_flow > 0:
                    est_runtime = round(water_L / effective_flow, 2)
                
                st.markdown(f"{tr('forecast_runtime')}: **{est_runtime} {tr('units_hours')}**")
                st.caption(tr("runtime_note"))
            else:
                st.success(tr("no_trigger_next"))
            
            st.markdown("---")
            st.caption(tr("lbl_forecast_table"))
            st.dataframe(forecast_df[['date', 'et0_pred', 'deficit_pred', 'stress_flag']], use_container_width=True)

    # -------------------------------
    # RAW DEBUG VIEW
    # -------------------------------
    with st.expander(f"{tr('metadata_title')}"):
        st.json({
            "parameters": params,
            "state_today": {
                "date": today['date'],
                "deficit": current_deficit,
                "is_stressed": is_stressed
            },
            "recommendation_today": rec_display,
            "validation": metrics
        })

else:
    # Default State
    st.info(" Please configure the site parameters and run the simulation. ")