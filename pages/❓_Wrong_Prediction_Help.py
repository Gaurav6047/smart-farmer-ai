import streamlit as st
from utils.theme import load_theme
load_theme()

from utils.language import get_text

# --------------------------------------------------
# Language Selector
# --------------------------------------------------
lang = st.sidebar.selectbox("Language / भाषा", ["English", "Hindi"])
T = get_text(lang)

# --------------------------------------------------
# Premium Header
# --------------------------------------------------
st.markdown(f"""
<div class="header-box">
    <h2 style='margin:0;color:white;'>{T['wrong_prediction']}</h2>
    <p style='margin:0;color:white;'>Improve image quality for accurate predictions</p>
</div>
""", unsafe_allow_html=True)

# --------------------------------------------------
# Intro Text
# --------------------------------------------------
if lang == "English":
    st.markdown("""
AI models sometimes produce wrong results due to **image quality, lighting, angle, or visibility issues**.  
This guide helps you capture better photos and understand what went wrong.
""")
else:
    st.markdown("""
एआई मॉडल कभी–कभी **कमज़ोर इमेज क्वालिटी, रोशनी, एंगल या वस्तु सही से न दिखने** के कारण गलत परिणाम देते हैं।  
यह गाइड आपको बेहतर फोटो लेने और गलती समझने में मदद करेगा।
""")

# --------------------------------------------------
# Tabs
# --------------------------------------------------
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🔍 " + ("Common Issues" if lang=="English" else "सामान्य गलतियाँ"),
    "📸 " + ("How to Capture Good Images" if lang=="English" else "अच्छी फोटो कैसे लें"),
    "🌿 " + ("Leaf / Disease Issues" if lang=="English" else "पत्ती / बीमारी समस्याएँ"),
    "🐛 " + ("Pest Detection Issues" if lang=="English" else "कीट पहचान समस्याएँ"),
    "🍎 " + ("Fruit Image Issues" if lang=="English" else "फल से जुड़ी समस्याएँ"),
])


# --------------------------------------------------
# TAB 1 — Common Issues
# --------------------------------------------------
with tab1:
    st.header("🔍 " + ( "Common Causes of Wrong Predictions" if lang=="English" else "गलत भविष्यवाणी के सामान्य कारण" ))

    if lang == "English":
        st.markdown("""
### ❌ 1. Blurry or Out-of-Focus Image  
### ❌ 2. Too Much Background  
### ❌ 3. Wrong Camera Angle  
### ❌ 4. Poor Lighting  
### ❌ 5. Very Small Pest  
""")
    else:
        st.markdown("""
### ❌ 1. धुंधली / फोकस से बाहर फोटो  
### ❌ 2. बहुत ज़्यादा बैकग्राउंड  
### ❌ 3. गलत कैमरा एंगल  
### ❌ 4. खराब रोशनी  
### ❌ 5. बहुत छोटा कीट  
""")

# --------------------------------------------------
# TAB 2 — Good Image Guide
# --------------------------------------------------
with tab2:
    st.header("📸 " + ( "How to Capture Good Images" if lang=="English" else "अच्छी फोटो कैसे लें" ))

    if lang == "English":
        st.success("""
1. Keep camera 10–15 cm from object  
2. Ensure sharp focus  
3. Use natural daylight  
4. Keep background simple  
5. Object should cover 70–90% frame  
""")
    else:
        st.success("""
1. कैमरा 10–15 सेमी दूरी पर रखें  
2. साफ फोकस करें  
3. प्राकृतिक रोशनी का उपयोग करें  
4. बैकग्राउंड सरल रखें  
5. वस्तु 70–90% फ्रेम भरे  
""")

# --------------------------------------------------
# TAB 3 — Leaf Issues
# --------------------------------------------------
with tab3:
    st.header("🌿 " + ( "Leaf Troubleshooting" if lang=="English" else "पत्ती समस्या समाधान" ))

    if lang == "English":
        st.markdown("""
- Leaf partially visible  
- Overlapping leaves  
- Small disease patch  
- Wet or dirty leaf  
""")
    else:
        st.markdown("""
- पत्ती अधूरी दिखना  
- कई पत्तियाँ एक-दूसरे पर  
- बीमारी का छोटा दाग  
- गीली / धूल भरी पत्ती  
""")

# --------------------------------------------------
# TAB 4 — Pest Issues
# --------------------------------------------------
with tab4:
    st.header("🐛 " + ( "Pest Troubleshooting" if lang=="English" else "कीट समस्या समाधान" ))

    if lang == "English":
        st.markdown("""
- Pest too small  
- Pest hidden  
- Strong shadows  
- Low light  
""")
    else:
        st.markdown("""
- कीट बहुत छोटा  
- पत्ती के नीचे छिपा  
- तेज़ छाया  
- कम रोशनी  
""")
        
# --------------------------------------------------
# TAB 5 — Fruit Image Issues
# --------------------------------------------------
with tab5:
    st.header("🍎 " + ("Fruit Troubleshooting" if lang=="English" else "फल समस्या समाधान"))

    if lang == "English":
        st.markdown("""
### ❌ Common Problems:
- Fruit only partially visible  
- Too much background  
- Fruit not centered  
- Strong reflections on shiny fruits  
- Poor lighting makes color look wrong  
- Multiple fruits overlapping  
- Water droplets / dirt on fruit  
---

### ✔ Fix:
- Capture the full fruit  
- Keep the fruit centered  
- Use clear daylight  
- Avoid shiny reflections  
- Clean the fruit surface  
- Keep background simple  
""")
    else:
        st.markdown("""
### ❌ सामान्य समस्याएँ:
- फल पूरा फ्रेम में नहीं दिखता  
- बहुत ज़्यादा बैकग्राउंड  
- फल बीच में नहीं है  
- फलों पर तेज़ चमक / रिफ्लेक्शन  
- कम रोशनी से रंग गलत दिखता है  
- कई फल एक-दूसरे पर चढ़े होना  
- फल पर पानी / मिट्टी  
---

### ✔ समाधान:
- पूरा फल साफ-साफ दिखाएँ  
- फल को फ्रेम के बीच में रखें  
- प्राकृतिक रोशनी में फोटो लें  
- चमक से बचें  
- फल की सतह साफ करें  
- बैकग्राउंड सरल रखें  
""")

# --------------------------------------------------
# Final help
# --------------------------------------------------
st.markdown("---")

if lang == "English":
    st.subheader("💡 Still getting wrong predictions?")
    st.write("Try retaking the image with better lighting, focus and angle.")
else:
    st.subheader("💡 फिर भी गलत परिणाम मिल रहा है?")
    st.write("फोटो को बेहतर रोशनी, फोकस और सही एंगल से दोबारा क्लिक करें।")
