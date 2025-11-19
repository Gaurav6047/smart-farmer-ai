def get_text(lang):

    TEXT = {

        # ===============================================================
        # ==========================  ENGLISH  ===========================
        # ===============================================================
        "English": {

            # -------------------------
            # Home Page
            # -------------------------
            "app_title": "Smart Farmer — AI Agriculture Assistant",
            "home_sub": "AI-powered Crop, Pest & Disease Assistant",
            "features": "Features",
            "upload": "Upload Image",
            "capture": "Capture from Camera",

            # Buttons
            "analyze": "Analyze",
            "detect": "Detect",
            "classify": "Classify",
            "process": "Process",
            "recommend_btn": "Recommend Crop",
            "result": "Result",
            "confidence": "Confidence",
            "conf_meter": "Confidence Meter",

            # Routing
            "auto_route": "Auto Routing",
            "low_conf": "Low confidence — please try again.",
            "background_msg": "This looks like background. Please retake the photo.",
            "invalid_img": "Invalid image. Please upload a clear image.",

            # Pages
            "plant_disease": "Plant Disease Detection",
            "pest_detection": "Pest Detection",
            "fruit_classification": "Fruit Classification",
            "model_info": "Model Classes Information",
            "wrong_prediction": "Troubleshooting Guide",

            # Crop Recommendation Page
            "crop_recommendation": "Crop Recommendation",
            "enter_soil_data": "Enter Soil & Climate Values",
            "recommended_crop": "Recommended Crop",

            # -------------------------
            # Fertilizer Page (UI)
            # -------------------------
            "fertilizer_engine": "Fertilizer Recommendation",
            "fert_header": "Fertilizer Recommendation Engine",
            "fert_subheader": "AI-powered nutrient recommendation based on STCR + IPNS.",

            "soil_report": "🌱 Soil Test Report",
            "nitrogen": "Nitrogen (N) kg/ha",
            "phosphorus": "Phosphorus (P) kg/ha",
            "potassium": "Potassium (K) kg/ha",
            "soil_ph": "pH Level",
            "soil_ec": "EC (dS/m)",

            "micronutrients": "Micronutrients (optional)",
            "zinc": "Zinc (Zn) ppm",
            "iron": "Iron (Fe) ppm",

            "crop_section": "🌾 Crop Selection",
            "state": "State",
            "season": "Season",
            "suggested_crops": "Suggested Crops",
            "custom_crop": "Custom Crop (optional)",

            "method": "Calculation Method",
            "method_standard": "Standard Recommendation",
            "method_stcr": "STCR (Targeted Yield)",
            "target_yield": "Target Yield (q/ha)",
            "stcr_model": "STCR Model",

            "organic_inputs": "🍃 Organic Inputs (IPNS)",
            "fym": "FYM (kg/ha)",
            "vermi": "Vermicompost (kg/ha)",
            "prev_crop": "Previous Crop",

            "submit_fert": "🚀 Generate Recommendation",
            "processing": "Processing agronomic algorithms...",

            "fert_bags": "🎒 Fertilizer Bags (per hectare)",
            "alert_title": "⚠️ Important Alerts",
            "breakdown_title": "🔬 Technical Breakdown",
            "breakdown_table_title": "Nutrient Requirement Flow",
            "base_req": "Base Requirement",
            "organic_deduct": "Organic Credits Deducted",
            "final_req": "Final Requirement",

            # ----------------------------------------------------
            # Fertilizer Engine Info Page (English)
            # ----------------------------------------------------
            "info_title": "Fertilizer Engine — Technical Overview",

            "info_intro": """
This engine is a scientifically-designed, multi-layer fertilizer recommendation system
combining soil science, STCR, IPNS, organic credits, micronutrient analysis and 
commercial fertilizer conversion. It is similar to systems used in major agritech
platforms like DeHaat, AgroStar and BharatAgri.
""",

            "info_problem": "Problem This Engine Solves",
            "info_problem_text": """
Farmers often apply incorrect fertilizer doses due to:
• No soil interpretation  
• No STCR targeted yield calculation  
• No organic nutrient deduction  
• No NPK → Urea/DAP/MOP conversion  

This engine automates the entire science and gives accurate, professional results.
""",

            "info_arch": "Engine Architecture",
            "info_arch_text": """
The engine consists of 7 interconnected modules:
1. SoilThresholdEngine  
2. StandardNPKEngine  
3. STCREngine  
4. OrganicRulesEngine  
5. BrandConverter  
6. AutoCropEngine  
7. FertilizerRecommender  
""",

            "info_data": "Data Sources",
            "info_data_text": """
• soil_fertility.json  
• standard_npk.csv  
• stcr_equations.json  
• organic_rules.json  
""",

            "info_workflow": "Internal Workflow",
            "info_level": "What Level of Engine Is This?",
            "info_future": "Future Enhancements",
        },

        # ===============================================================
        # ===========================  HINDI  ============================
        # ===============================================================

        "Hindi": {

            # -------------------------
            # Home Page
            # -------------------------
            "app_title": "Smart Farmer — एआई कृषि सहायक",
            "home_sub": "फसल, कीट और बीमारी पहचान के लिए AI आधारित सहायक",
            "features": "फ़ीचर्स",
            "upload": "चित्र अपलोड करें",
            "capture": "कैमरा से फोटो लें",

            # Buttons
            "analyze": "विश्लेषण करें",
            "detect": "पता लगाएँ",
            "classify": "वर्गीकृत करें",
            "process": "प्रोसेस करें",
            "recommend_btn": "फसल सुझाव दें",
            "result": "परिणाम",
            "confidence": "विश्वास स्तर",
            "conf_meter": "विश्वास मीटर",

            # Routing
            "auto_route": "ऑटो रूटिंग",
            "low_conf": "कम विश्वास — कृपया दोबारा प्रयास करें।",
            "background_msg": "यह बैकग्राउंड जैसा लगता है। कृपया दोबारा फोटो लें।",
            "invalid_img": "अमान्य छवि। कृपया साफ फोटो अपलोड करें।",

            # Pages
            "plant_disease": "पौधे की बीमारी पहचान",
            "pest_detection": "कीट पहचान",
            "fruit_classification": "फल पहचान",
            "model_info": "मॉडल क्लास जानकारी",
            "wrong_prediction": "गलत भविष्यवाणी — सहायता",

            # Crop Recommendation
            "crop_recommendation": "फसल सुझाव",
            "enter_soil_data": "मिट्टी और जलवायु डेटा दर्ज करें",
            "recommended_crop": "सुझाई गई फसल",

            # -------------------------
            # Fertilizer UI Page
            # -------------------------
            "fertilizer_engine": "उर्वरक सिफारिश इंजन",
            "fert_header": "उर्वरक सिफ़ारिश इंजन",
            "fert_subheader": "एसटीसीआर + आईपीएनएस आधारित एआई-संचालित पोषक तत्व सिफारिश।",

            "soil_report": "🌱 मृदा परीक्षण रिपोर्ट",
            "nitrogen": "नाइट्रोजन (N) किग्रा/हे.",
            "phosphorus": "फॉस्फोरस (P) किग्रा/हे.",
            "potassium": "पोटैशियम (K) किग्रा/हे.",
            "soil_ph": "pH स्तर",
            "soil_ec": "EC (dS/m)",

            "micronutrients": "सूक्ष्म पोषक तत्व (वैकल्पिक)",
            "zinc": "जिंक (Zn) पीपीएम",
            "iron": "आयरन (Fe) पीपीएम",

            "crop_section": "🌾 फसल चयन",
            "state": "राज्य",
            "season": "मौसम",
            "suggested_crops": "सुझाई गई फसलें",
            "custom_crop": "कस्टम फसल (वैकल्पिक)",

            "method": "गणना विधि",
            "method_standard": "मानक सिफारिश",
            "method_stcr": "एसटीसीआर (लक्ष्य उपज)",
            "target_yield": "लक्ष्य उपज (क्विंटल/हे.)",
            "stcr_model": "एसटीसीआर मॉडल",

            "organic_inputs": "🍃 जैविक इनपुट (IPNS)",
            "fym": "एफवाईएम (किग्रा/हे.)",
            "vermi": "वर्मीकम्पोस्ट (किग्रा/हे.)",
            "prev_crop": "पिछली फसल",

            "submit_fert": "🚀 सिफ़ारिश प्राप्त करें",
            "processing": "कृषि एल्गोरिदम प्रोसेस हो रहे हैं...",

            "fert_bags": "🎒 उर्वरक बैग (प्रति हेक्टेयर)",
            "alert_title": "⚠️ महत्वपूर्ण चेतावनी",
            "breakdown_title": "🔬 तकनीकी विवरण",
            "breakdown_table_title": "पोषक तत्व आवश्यकता फ्लो",
            "base_req": "आधार आवश्यकता",
            "organic_deduct": "जैविक कटौती",
            "final_req": "अंतिम आवश्यकता",

            # -------------------------
            # Fertilizer INFO PAGE
            # -------------------------

            "info_title": "उर्वरक इंजन — तकनीकी विवरण",

            "info_intro": """
यह इंजन एक वैज्ञानिक रूप से डिज़ाइन किया गया, बहु-स्तरीय उर्वरक सिफ़ारिश प्रणाली है
जो मृदा विज्ञान, STCR, IPNS, जैविक पोषक तत्व कटौती, सूक्ष्म पोषक विश्लेषण 
और वाणिज्यिक उर्वरक रूपांतरण को जोड़ता है।
यह DeHaat, AgroStar और BharatAgri जैसी कंपनियों द्वारा उपयोग किए जाने
वाले सिस्टम जैसा है।
""",

            "info_problem": "यह इंजन किस समस्या का समाधान करता है",
            "info_problem_text": """
किसान अक्सर गलत मात्रा में उर्वरक डालते हैं क्योंकि:
• मृदा विश्लेषण सही नहीं  
• STCR गणना नहीं  
• जैविक कटौती नहीं  
• NPK → उर्वरक बैग रूपांतरण का अभाव  

यह इंजन पूरी प्रक्रिया को स्वचालित करता है और वैज्ञानिक रूप से सही परिणाम देता है।
""",

            "info_arch": "इंजन की संरचना",
            "info_arch_text": """
यह इंजन 7 मुख्य मॉड्यूल से बना है:
1. SoilThresholdEngine  
2. StandardNPKEngine  
3. STCREngine  
4. OrganicRulesEngine  
5. BrandConverter  
6. AutoCropEngine  
7. FertilizerRecommender  
""",

            "info_data": "डेटा स्रोत",
            "info_data_text": """
• soil_fertility.json  
• standard_npk.csv  
• stcr_equations.json  
• organic_rules.json  
""",

            "info_workflow": "आंतरिक कार्यप्रणाली",
            "info_level": "यह इंजन किस स्तर का है?",
            "info_future": "भविष्य में सुधार",
        }
    }

    return TEXT[lang]
