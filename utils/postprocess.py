import streamlit as st

def show_result(label, conf):
    st.markdown(f"""
        <div style="padding:15px; background:#f0fff4; border-left:6px solid #22c55e; border-radius:10px;">
            <h3 style="margin:0; color:#166534;">{label}</h3>
            <p style="font-size:18px; margin:5px 0;">Confidence: <b>{conf:.2f}</b></p>
        </div>
    """, unsafe_allow_html=True)

    st.progress(conf)
