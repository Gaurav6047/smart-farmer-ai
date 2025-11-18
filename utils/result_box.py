import streamlit as st

def show_result(label, conf, T):
    html = f"""
    <div style="
        padding:20px;
        border-radius:12px;
        background-color:#f0fff4;
        border-left:8px solid #22c55e;
        box-shadow:0px 4px 12px rgba(0,0,0,0.08);
        margin-top:15px;
    ">
        <h3 style="margin:0;color:#166534;font-size:24px;font-weight:600;">
            {T['result']}: {label}
        </h3>

        <p style="margin:6px 0 0 0;font-size:18px;color:#064e3b;">
            {T['confidence']}: <b>{conf:.2f}</b>
        </p>
    </div>
    """
    st.components.v1.html(html, height=140)
    st.markdown(f"### {T['conf_meter']}")
    st.progress(conf)
