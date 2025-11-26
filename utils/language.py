# ================================================================
# language.py — Bilingual Dictionary + Auto-Fallback System
# ================================================================

# ---------------------------
# ENGLISH TEXT
# ---------------------------
EN_TEXT = {
    "app_title": "Smart Farmer — AI Agriculture Assistant",
    "home_sub": "AI-powered Crop, Pest & Disease Assistant",
    "banner_missing": "Home banner missing → assets/ui/farm_banner.gif",

    "features": "Features",

    "feat_disease": "Plant Disease Detection",
    "feat_pest": "Pest Detection",
    "feat_fruit": "Fruit & Vegetable Classification",
    "feat_auto": "Smart Auto-Scan",
    "feat_model_info": "Model & Engine Info",
    "feat_crop": "Crop Recommendation",
    "feat_fertilizer": "Fertilizer Calculator",
    "feat_irrigation": "Irrigation Advisory System — Water need, crop stage, soil moisture & irrigation scheduling",

    "navigate_sidebar": "Use the Left Sidebar to navigate between Smart Farmer features.",


    # ----------------------------- AUTO ROUTER ------------------------------
    "auto_route": "Smart Auto-Scan",
    "auto_sub": "Automatically detect image type",
    "capture_img": "Capture Image",
    "upload": "Upload Image",
    "invalid_img": "Invalid image. Please upload a clear JPG/PNG.",
    "process": "Process",
    "processing_image": "Processing image...",
    "result": "Result",

    "leaf": "Leaf",
    "fruit": "Fruit",
    "pest": "Pest",
    "background": "Background",

    "background_msg": "This looks like background. Please take a clear photo.",
    "low_conf": "Low confidence — try a clearer image.",


    # ----------------------------- CROP RECO ------------------------------
    "crop_recommendation": "Crop Recommendation",
    "enter_soil_data": "Enter Soil & Climate Values",

    "nitrogen": "Nitrogen (N)",
    "phosphorus": "Phosphorus (P)",
    "potassium": "Potassium (K)",
    "temperature": "Temperature (°C)",
    "humidity": "Humidity (%)",
    "ph_level": "Soil pH",
    "rainfall": "Rainfall (mm)",

    "recommend_btn": "Recommend Crop",
    "recommended_crop": "Recommended Crop",


    # ----------------------------- FERTILIZER ENGINE ------------------------------
    "fert_title": "SmartFert Recommendation Engine",
    "fert_sub": "AI-based nutrient calculation using NPK + STCR",

    "npk_tab": "NPK Mode (Regional Standard)",
    "stcr_tab": "STCR Mode (Target Yield)",

    "npk_header": "NPK Mode — Soil Test Based Adjustment",
    "npk_no_states": "No NPK states available in dataset.",
    "select_state": "Select State",
    "select_crop": "Select Crop",
    "select_season": "Select Season",

    "npk_enter_soil": "Enter Soil Test Report Values (Leave empty if unknown)",
    "soil_test_details": "Soil Test Details",

    "soil_sn": "Available Nitrogen (N) kg/ha",
    "soil_sp": "Available Phosphorus (P) kg/ha",
    "soil_sk": "Available Potassium (K) kg/ha",
    "soil_ph": "Soil pH",
    "soil_ph_opt": "pH (Optional)",

    "soil_oc": "Organic Carbon (%)",
    "soil_ec": "EC (dS/m)",

    "soil_zn": "Zinc (ppm)",
    "soil_fe": "Iron (ppm)",
    "soil_s": "Sulphur (ppm)",

    "organic_inputs": "Organic Inputs (IPNS)",
    "organic_type": "Organic Source Used",
    "organic_qty": "Quantity (kg/ha)",

    "output_settings": "Output Settings",
    "rounding_mode": "Fertilizer Bag Rounding",
    "round_exact": "Exact (Scientific)",
    "round_field": "Field (Nearest 5kg)",
    "round_bag": "Bag (Nearest 25kg)",

    "btn_generate": "Generate Recommendation",
    "error_prefix": "Error",
    "success_generated": "Recommendation Generated Successfully",

    "final_nutrients": "Final Nutrients Needed (kg/ha)",
    "n_val": "Nitrogen (N)",
    "p_val": "Phosphorus (P₂O₅)",
    "k_val": "Potassium (K₂O)",

    "organic_credit": "Organic Credit",
    "manure_saved": "Manure saved:",
    "no_organic_credit": "No organic credit applied.",

    "fert_recommend": "Fertilizer Recommendations",
    "micronutrients": "Micronutrients",
    "no_micro_detected": "No micronutrient deficiencies detected.",

    "expert_advisories": "Expert Advisories",

    "stcr_header": "STCR Mode — Precision Farming (Target Yield)",
    "stcr_no_states": "No STCR data available.",
    "select_soil_type": "Select Soil Type",

    "target_yield": "Target Yield (q/ha)",
    "target_yield_note": "Enter realistic yield potential for your variety.",

    "stcr_mandatory": "For STCR, Soil Test Values (N, P, K) are MANDATORY.",

    "soil_test_values": "Soil Test Values",

    "btn_stcr_calc": "Calculate STCR Dose",
    "err_target_zero": "Target Yield must be greater than 0.",
    "err_stcr_empty": "Soil N, P, K values cannot be all zero for STCR.",

    "success_calculated": "Calculation Successful",

    "target_dose": "Target Nutrient Dose (kg/ha)",
    "manure_supplied": "Supplied by Manure:",
    "agronomist_notes": "Agronomist Notes",


    # ----------------------------- ADVISORIES ------------------------------
    "adv_stcr_mode": "Used Target Yield Equation (STCR) for highest precision.",
    "adv_npk_mode": "Used Regional NPK Standards adjusted for soil test values.",

    "adv_low_oc": "Low Organic Carbon: Soil health is poor. Add more FYM or Compost.",
    "adv_good_oc": "Good Organic Carbon levels.",

    "adv_low_n": "Low Nitrogen availability: Apply Urea in 3-4 split doses.",

    "adv_low_p_acidic": "Low Phosphorus in acidic soil: Use Rock Phosphate or DAP.",
    "adv_low_p": "Low Phosphorus: Apply SSP/DAP near the root zone.",

    "adv_micro_detected": "{micro} deficiency detected. Apply recommended micronutrient sources.",

    "adv_low_ph": "Acidic soil detected: Apply lime to improve nutrient uptake.",
    "adv_high_ph": "Alkaline soil detected: Gypsum application recommended.",
    "adv_high_ec": "High soil salinity detected: Improve drainage to avoid salt accumulation.",

    "advisory_title": "Expert Advisories",


    # ----------------------------- FRUIT MODEL ------------------------------
    "fruit_subtitle": "AI-based Fruit & Vegetable Recognition",
    "invalid_fruit_image": "Invalid or corrupted image. Please upload JPG/PNG.",
    "fruit_loading": "Identifying fruit...",

    "fruit_classes": {
        "apple": "Apple",
        "banana": "Banana",
        "beetroot": "Beetroot",
        "bell pepper": "Bell Pepper",
        "cabbage": "Cabbage",
        "capsicum": "Capsicum",
        "carrot": "Carrot",
        "cauliflower": "Cauliflower",
        "chilli pepper": "Chilli Pepper",
        "corn": "Corn",
        "cucumber": "Cucumber",
        "eggplant": "Eggplant",
        "garlic": "Garlic",
        "ginger": "Ginger",
        "grapes": "Grapes",
        "jalepeno": "Jalepeno",
        "kiwi": "Kiwi",
        "lemon": "Lemon",
        "lettuce": "Lettuce",
        "mango": "Mango",
        "onion": "Onion",
        "orange": "Orange",
        "paprika": "Paprika",
        "pear": "Pear",
        "peas": "Peas",
        "pineapple": "Pineapple",
        "pomegranate": "Pomegranate",
        "potato": "Potato",
        "raddish": "Raddish",
        "soy beans": "Soy Beans",
        "spinach": "Spinach",
        "sweetcorn": "Sweet Corn",
        "sweetpotato": "Sweet Potato",
        "tomato": "Tomato",
        "turnip": "Turnip",
        "watermelon": "Watermelon"
    },


    # ----------------------------- IRRIGATION ------------------------------
    "smart_irrigation": "Smart Irrigation Engine",
    "irrigation_subtitle": "Weather-Based ET₀ • ETc • Soil Deficit • Forecast",

    "explanation": "Explanation",

    "graph_title": "ETc & Soil Deficit Trends",
    "graph_etc": "Daily ETc (mm)",
    "graph_deficit": "Soil Water Deficit (mm)",
    "graph_forecast": "ETc Forecast (Next 3 Days)",

    "ex_etc_loss": "Crop water use (ETc):",
    "ex_deficit_reached": "Soil deficit has reached:",
    "ex_threshold": "Critical threshold:",
    "ex_soil_ok": "Soil still has enough moisture.",
    "ex_below_thresh": "Deficit is below threshold.",


    # ----------------------------- MODEL INFO PAGE ------------------------------
    "model_info": "Model & Engine Information",

    "model_info_desc": """
This page displays information about all the AI Models & Engines used in this system:<br><br>
• <b>Image Models:</b> Plant Disease, Pest Detection, Fruit Classification.<br>
• <b>Agronomic Engines:</b> Fertilizer Calculation, Irrigation Planning, Crop Recommendation.
""",

    "fert_engine": "Fertilizer Engine",
    "irrig_engine": "Irrigation Engine",
    "crop_reco_engine": "Crop Recommendation",

    "err_plant_csv": "Plant disease CSV missing in models/",
    "err_pest_csv": "pest_classes.csv missing in models/",
    "err_fruit_json": "fruit_class_names.json missing in models/",

    "total_classes": "Total Classes",
    "hint_leaf_upload": "Upload a clear leaf image with good lighting",
    "hint_pest_close": "Bring camera close to pest!",
    "hint_fruit_center": "Use good lighting and keep fruit centered.",

    "fert_engine_desc": """
<strong>About this Engine:</strong><br>
A hybrid recommendation engine that calculates precise fertilizer dosages.<br><br>
• <b>Methodology:</b> Uses STCR equations.<br>
• <b>Fallback:</b> Regional NPK standards.<br>
• <b>Organic Logic:</b> Subtracts manure nutrients.<br>
• <b>Output:</b> Urea, DAP, MOP bag requirements.<br>
• <b>Advisory:</b> Soil pH, OC health checks.<br>
""",

    "irrig_engine_desc": """
<strong>About this Engine:</strong><br>
A system that tells you when to irrigate and how long to run your pump.<br><br>
• Uses FAO-56 Penman-Monteith.<br>
• 3-day ETc forecast using ML.<br>
• Pump runtime based on HP.<br>
• Clear action: Start Pump / Do Not Water.<br>
""",

    "crop_reco_desc": """
<strong>About this Engine:</strong><br>
Suggests the best crop based on soil and weather conditions.<br><br>
• Based on Random Forest ML.<br>
• Inputs: N, P, K, Temp, Humidity, pH, Rainfall.<br>
• Supports 22 crops.<br>
• Matches climate → best crop choice.<br>
""",


    # ----------------------------- PEST DETECTION ------------------------------
    "pest_subtitle": "YOLO-based Insect Detection",
    "pest_loading": "Detecting pests...",
    "no_pest_found": "No pest detected!",
    "detected_pests": "Detected Pests:",

    "plant_disease": "Plant Disease Detection",
    "plant_disease_sub": "AI-based Leaf Disease Detection",

    "invalid_img": "Invalid or corrupted image.",
    "processing_image": "Analyzing image...",
    "no_image": "Upload an image or capture from camera to start.",


    # ----------------------------- DISEASE CLASSES ------------------------------
    "disease_classes": {
        "Apple – Apple Scab": "Apple – Apple Scab",
        "Apple – Black Rot": "Apple – Black Rot",
        "Apple – Cedar Apple Rust": "Apple – Cedar Apple Rust",
        "Apple – Healthy Leaf": "Apple – Healthy Leaf",
        "Blueberry – Healthy Leaf": "Blueberry – Healthy Leaf",
        "Cherry – Powdery Mildew": "Cherry – Powdery Mildew",
        "Cherry – Healthy Leaf": "Cherry – Healthy Leaf",
        "Corn – Cercospora Leaf Spot (Gray Leaf Spot)": "Corn – Cercospora Leaf Spot (Gray Leaf Spot)",
        "Corn – Common Rust": "Corn – Common Rust",
        "Corn – Northern Leaf Blight": "Corn – Northern Leaf Blight",
        "Corn – Healthy Leaf": "Corn – Healthy Leaf",
        "Grape – Black Rot": "Grape – Black Rot",
        "Grape – Esca (Black Measles)": "Grape – Esca (Black Measles)",
        "Grape – Leaf Blight (Isariopsis Leaf Spot)": "Grape – Leaf Blight (Isariopsis Leaf Spot)",
        "Grape – Healthy Leaf": "Grape – Healthy Leaf",
        "Orange – Citrus Greening (Haunglongbing)": "Orange – Citrus Greening (Haunglongbing)",
        "Peach – Bacterial Spot": "Peach – Bacterial Spot",
        "Peach – Healthy Leaf": "Peach – Healthy Leaf",
        "Bell Pepper – Bacterial Spot": "Bell Pepper – Bacterial Spot",
        "Bell Pepper – Healthy Leaf": "Bell Pepper – Healthy Leaf",
        "Potato – Early Blight": "Potato – Early Blight",
        "Potato – Late Blight": "Potato – Late Blight",
        "Potato – Healthy Leaf": "Potato – Healthy Leaf",
        "Raspberry – Healthy Leaf": "Raspberry – Healthy Leaf",
        "Soybean – Healthy Leaf": "Soybean – Healthy Leaf",
        "Squash – Powdery Mildew": "Squash – Powdery Mildew",
        "Strawberry – Leaf Scorch": "Strawberry – Leaf Scorch",
        "Strawberry – Healthy Leaf": "Strawberry – Healthy Leaf",
        "Tomato – Bacterial Spot": "Tomato – Bacterial Spot",
        "Tomato – Early Blight": "Tomato – Early Blight",
        "Tomato – Late Blight": "Tomato – Late Blight",
        "Tomato – Leaf Mold": "Tomato – Leaf Mold",
        "Tomato – Septoria Leaf Spot": "Tomato – Septoria Leaf Spot",
        "Tomato – Spider Mites (Two-Spotted Spider Mite)": "Tomato – Spider Mites (Two-Spotted Spider Mite)",
        "Tomato – Target Spot": "Tomato – Target Spot",
        "Tomato – Yellow Leaf Curl Virus": "Tomato – Yellow Leaf Curl Virus",
        "Tomato – Mosaic Virus": "Tomato – Mosaic Virus",
        "Tomato – Healthy Leaf": "Tomato – Healthy Leaf"
    }
}


# ---------------------------
# HINDI TEXT
# ---------------------------
HI_TEXT = {
        "app_title": "स्मार्ट फ़ार्मर — एआई कृषि सहायक",
    "home_sub": "फसल, कीट और रोग पहचान के लिए एआई आधारित सहायक",
    "banner_missing": "होम बैनर गायब है → assets/ui/farm_banner.gif",

    "features": "फ़ीचर्स",

    "feat_disease": "पौध रोग पहचान",
    "feat_pest": "कीट पहचान",
    "feat_fruit": "फल-सब्ज़ी पहचान",
    "feat_auto": "स्मार्ट ऑटो-स्कैन",
    "feat_model_info": "मॉडल और इंजन जानकारी",
    "feat_crop": "फसल सिफारिश",
    "feat_fertilizer": "खाद का हिसाब",
    "feat_irrigation": "सिंचाई सलाह — पानी की ज़रूरत, फसल अवस्था, मिट्टी की नमी और सिंचाई शेड्यूलिंग",

    "navigate_sidebar": "स्मार्ट फ़ार्मर के सभी टूल्स देखने के लिए बाएं साइडबार का उपयोग करें।",


    # --------------------- AUTO ROUTER ---------------------
    "auto_route": "स्मार्ट ऑटो-स्कैन",
    "auto_sub": "फोटो का प्रकार अपने-आप पहचानें",
    "capture_img": "कैमरा से फोटो लें",
    "upload": "फोटो अपलोड करें",
    "invalid_img": "छवि खराब है या सही नहीं। कृपया साफ JPG/PNG अपलोड करें।",
    "process": "प्रोसेस करें",
    "processing_image": "फोटो का विश्लेषण हो रहा है...",
    "result": "परिणाम",

    "leaf": "पत्ती",
    "fruit": "फल / सब्ज़ी",
    "pest": "कीट",
    "background": "बैकग्राउंड",

    "background_msg": "यह बैकग्राउंड जैसा लग रहा है। कृपया साफ फोटो लें।",
    "low_conf": "विश्वास स्तर कम है — कृपया साफ फोटो लें।",


    # --------------------- CROP RECO ---------------------
    "crop_recommendation": "फसल सिफारिश",
    "enter_soil_data": "मिट्टी और मौसम से जुड़े मान दर्ज करें",

    "nitrogen": "नाइट्रोजन (N)",
    "phosphorus": "फॉस्फोरस (P)",
    "potassium": "पोटैशियम (K)",
    "temperature": "तापमान (°C)",
    "humidity": "नमी (%)",
    "ph_level": "मिट्टी का pH",
    "rainfall": "वर्षा (mm)",

    "recommend_btn": "फसल सुझाएँ",
    "recommended_crop": "सुझाई गई फसल",

    "crop_classes": {
        "apple": "सेब",
        "banana": "केला",
        "beetroot": "चुकंदर",
        "bell pepper": "शिमला मिर्च",
        "cabbage": "पत्ता गोभी",
        "capsicum": "कैप्सिकम",
        "carrot": "गाजर",
        "cauliflower": "फूलगोभी",
        "chilli pepper": "हरी मिर्च",
        "corn": "मक्का",
        "cucumber": "खीरा",
        "eggplant": "बैंगन",
        "garlic": "लहसुन",
        "ginger": "अदरक",
        "grapes": "अंगूर",
        "jalepeno": "जलेपेनो",
        "kiwi": "कीवी",
        "lemon": "नींबू",
        "lettuce": "सलाद पत्ता",
        "mango": "आम",
        "onion": "प्याज",
        "orange": "संतरा",
        "paprika": "पपरिका",
        "pear": "नाशपाती",
        "peas": "मटर",
        "pineapple": "अनानास",
        "pomegranate": "अनार",
        "potato": "आलू",
        "raddish": "मूली",
        "soy beans": "सोयाबीन",
        "spinach": "पालक",
        "sweetcorn": "मीठा मक्का",
        "sweetpotato": "शकरकंद",
        "tomato": "टमाटर",
        "turnip": "शलजम",
        "watermelon": "तरबूज"
    },


    # --------------------- FERTILIZER ENGINE ---------------------
    "fert_title": "SmartFert उर्वरक सिफारिश इंजन",
    "fert_sub": "NPK + STCR आधारित AI पोषक तत्व गणना",

    "npk_tab": "NPK मोड (मानक सिफारिश)",
    "stcr_tab": "STCR मोड (लक्ष्य उपज)",

    "npk_header": "NPK मोड — मिट्टी परीक्षण आधारित समायोजन",
    "npk_no_states": "डेटासेट में NPK राज्यों का डेटा उपलब्ध नहीं है।",

    "select_state": "राज्य चुनें",
    "select_crop": "फसल चुनें",
    "select_season": "मौसम चुनें",

    "npk_enter_soil": "मिट्टी परीक्षण मान दर्ज करें (अज्ञात हो तो खाली छोड़ें)",
    "soil_test_details": "मिट्टी परीक्षण विवरण",

    "soil_sn": "उपलब्ध नाइट्रोजन (N) kg/ha",
    "soil_sp": "उपलब्ध फॉस्फोरस (P) kg/ha",
    "soil_sk": "उपलब्ध पोटैशियम (K) kg/ha",
    "soil_ph": "मिट्टी pH",
    "soil_ph_opt": "pH (वैकल्पिक)",

    "soil_oc": "जैविक कार्बन (%)",
    "soil_ec": "EC (dS/m)",

    "soil_zn": "जिंक (ppm)",
    "soil_fe": "आयरन (ppm)",
    "soil_s": "सल्फर (ppm)",

    "organic_inputs": "जैविक इनपुट (IPNS)",
    "organic_type": "प्रयोग किया गया जैविक स्रोत",
    "organic_qty": "मात्रा (kg/ha)",

    "output_settings": "आउटपुट सेटिंग्स",
    "rounding_mode": "खाद बैग राउंडिंग",
    "round_exact": "वैज्ञानिक (सटीक)",
    "round_field": "फील्ड (सबसे नज़दीकी 5kg)",
    "round_bag": "बैग (सबसे नज़दीकी 25kg)",

    "btn_generate": "सिफारिश तैयार करें",
    "error_prefix": "त्रुटि",
    "success_generated": "सिफारिश सफलतापूर्वक तैयार की गई",

    "final_nutrients": "आवश्यक पोषक तत्व (kg/ha)",
    "n_val": "नाइट्रोजन (N)",
    "p_val": "फॉस्फोरस (P₂O₅)",
    "k_val": "पोटैशियम (K₂O)",

    "organic_credit": "जैविक क्रेडिट",
    "manure_saved": "जैविक खाद से बचत:",
    "no_organic_credit": "कोई जैविक क्रेडिट लागू नहीं।",

    "fert_recommend": "उर्वरक सिफारिशें",
    "micronutrients": "सूक्ष्म पोषक तत्व",
    "no_micro_detected": "कोई सूक्ष्म पोषक कमी नहीं मिली।",

    "expert_advisories": "विशेषज्ञ सलाह",

    "stcr_header": "STCR मोड — सटीक खेती (लक्ष्य उपज)",
    "stcr_no_states": "STCR डेटा उपलब्ध नहीं है।",

    "select_soil_type": "मिट्टी का प्रकार चुनें",

    "target_yield": "लक्ष्य उपज (q/ha)",
    "target_yield_note": "अपनी किस्म के अनुसार वास्तविक उपज क्षमता दर्ज करें।",

    "stcr_mandatory": "STCR के लिए Soil N, P, K मान अनिवार्य हैं।",

    "soil_test_values": "मिट्टी परीक्षण मान",

    "btn_stcr_calc": "STCR खुराक गणना करें",
    "err_target_zero": "लक्ष्य उपज 0 से अधिक होनी चाहिए।",
    "err_stcr_empty": "STCR के लिए N, P, K तीनों शून्य नहीं हो सकते।",

    "success_calculated": "गणना सफल",

    "target_dose": "लक्ष्य पोषक खुराक (kg/ha)",
    "manure_supplied": "जैविक खाद द्वारा उपलब्ध:",
    "agronomist_notes": "कृषि विशेषज्ञ नोट्स",


    # --------------------- ADV ---------------------
    "adv_stcr_mode": "उच्च सटीकता के लिए STCR लक्ष्य-उपज समीकरण का उपयोग किया गया।",
    "adv_npk_mode": "मिट्टी परीक्षण के आधार पर क्षेत्रीय NPK मानकों का उपयोग किया गया।",

    "adv_low_oc": "कम ऑर्गेनिक कार्बन: मिट्टी का स्वास्थ्य कमजोर है। FYM या कम्पोस्ट बढ़ाएँ।",
    "adv_good_oc": "ऑर्गेनिक कार्बन स्तर अच्छे हैं।",

    "adv_low_n": "कम नाइट्रोजन उपलब्धता: यूरिया 3-4 बार विभाजित खुराक में दें।",

    "adv_low_p_acidic": "अम्लीय मिट्टी में फॉस्फोरस की कमी: रॉक फॉस्फेट या DAP का उपयोग करें।",
    "adv_low_p": "फॉस्फोरस कम है: SSP/DAP जड़ क्षेत्र के पास डालें।",

    "adv_micro_detected": "{micro} की कमी पाई गई। अनुशंसित सूक्ष्म पोषक स्रोत डालें।",

    "adv_low_ph": "मिट्टी अम्लीय है: पोषक अवशोषण सुधारने हेतु चूना डालें।",
    "adv_high_ph": "मिट्टी क्षारीय है: जिप्सम डालना लाभदायक है।",

    "adv_high_ec": "उच्च लवणता पाई गई: जल निकासी सुधारें ताकि नमक न जमे।",

    "advisory_title": "विशेषज्ञ सलाह",


    # --------------------- FRUIT MODEL ---------------------
    "fruit_subtitle": "एआई आधारित फल और सब्ज़ी पहचान",
    "invalid_fruit_image": "इमेज खराब है। कृपया JPG/PNG अपलोड करें।",
    "fruit_loading": "फल की पहचान हो रही है...",

    "fruit_classes": {
        "apple": "सेब",
        "banana": "केला",
        "beetroot": "चुकंदर",
        "bell pepper": "शिमला मिर्च",
        "cabbage": "पत्ता गोभी",
        "capsicum": "कैप्सिकम",
        "carrot": "गाजर",
        "cauliflower": "फूलगोभी",
        "chilli pepper": "हरी मिर्च",
        "corn": "मक्का",
        "cucumber": "खीरा",
        "eggplant": "बैंगन",
        "garlic": "लहसुन",
        "ginger": "अदरक",
        "grapes": "अंगूर",
        "jalepeno": "जलेपेनो मिर्च",
        "kiwi": "कीवी",
        "lemon": "नींबू",
        "lettuce": "लेट्यूस",
        "mango": "आम",
        "onion": "प्याज़",
        "orange": "संतरा",
        "paprika": "पाप्रिका",
        "pear": "नाशपाती",
        "peas": "मटर",
        "pineapple": "अनानास",
        "pomegranate": "अनार",
        "potato": "आलू",
        "raddish": "मूली",
        "soy beans": "सोयाबीन",
        "spinach": "पालक",
        "sweetcorn": "मीठा मक्का",
        "sweetpotato": "शकरकंद",
        "tomato": "टमाटर",
        "turnip": "शलगम",
        "watermelon": "तरबूज"
    },


    # --------------------- IRRIGATION ---------------------
    "smart_irrigation": "स्मार्ट सिंचाई इंजन",
    "irrigation_subtitle": "मौसम आधारित ET₀ • ETc • मृदा घाटा • पूर्वानुमान",

    "explanation": "व्याख्या",

    "graph_title": "ETc और मृदा घाटा ग्राफ़",
    "graph_etc": "दैनिक ETc (मिमी)",
    "graph_deficit": "मृदा जल घाटा (मिमी)",
    "graph_forecast": "आने वाले 3 दिनों का ETc पूर्वानुमान",

    "ex_etc_loss": "फसल द्वारा पानी की खपत (ETc):",
    "ex_deficit_reached": "मृदा घाटा पहुंच गया:",
    "ex_threshold": "सुरक्षा सीमा:",
    "ex_soil_ok": "मिट्टी में पर्याप्त नमी मौजूद है।",
    "ex_below_thresh": "घाटा अभी सीमा से कम है।",


    # --------------------- MODEL INFO ---------------------
    "model_info": "मॉडल और इंजन जानकारी",

    "model_info_desc": """
यह पेज इस सिस्टम में उपयोग किए गए सभी AI मॉडल और इंजनों की जानकारी दिखाता है:<br><br>
• <b>इमेज मॉडल:</b> पौधा रोग, कीट पहचान, फल वर्गीकरण।<br>
• <b>कृषि इंजन:</b> खाद गणना, सिंचाई योजना, फसल सुझाव।<br>
""",

    "fert_engine": "खाद इंजन",
    "irrig_engine": "सिंचाई इंजन",
    "crop_reco_engine": "फसल सुझाव इंजन",

    "err_plant_csv": "पौधा रोग CSV models/ में नहीं मिला",
    "err_pest_csv": "pest_classes.csv models/ में नहीं मिला",
    "err_fruit_json": "fruit_class_names.json models/ में नहीं मिला",

    "total_classes": "कुल क्लास",
    "hint_leaf_upload": "स्पष्ट और अच्छी रोशनी वाली पत्ती की इमेज अपलोड करें",
    "hint_pest_close": "कीट की फोटो पास से लें!",
    "hint_fruit_center": "फल को बीच में रखें और अच्छी रोशनी का उपयोग करें।",

    "fert_engine_desc": """
<strong>इस इंजन के बारे में:</strong><br>
यह एक हाइब्रिड सिस्टम है जो खाद की सही मात्रा की गणना करता है।<br><br>
• <b>तकनीक:</b> STCR समीकरण।<br>
• <b>बैकअप:</b> क्षेत्रीय NPK मानक।<br>
• <b>जैविक लॉजिक:</b> गोबर खाद पोषक तत्व घटाता है।<br>
• <b>आउटपुट:</b> यूरिया, DAP, MOP बोरियों की गणना।<br>
• <b>सलाह:</b> मिट्टी का pH और कार्बन जांच।<br>
""",

    "irrig_engine_desc": """
<strong>इस इंजन के बारे में:</strong><br>
यह सिस्टम बताता है कि पानी कब देना है और पंप कितनी देर चलाना है।<br><br>
• FAO-56 Penman-Monteith आधारित।<br>
• 3-दिन ETc पूर्वानुमान।<br>
• पंप HP के अनुसार रन-टाइम।<br>
• साफ निर्णय: पंप चलाएं / पानी न दें।<br>
""",

    "crop_reco_desc": """
<strong>इस इंजन के बारे में:</strong><br>
मिट्टी और मौसम के आधार पर सबसे उपयुक्त फसल सुझाता है।<br><br>
• Random Forest मशीन लर्निंग।<br>
• इनपुट: N, P, K, तापमान, नमी, pH, वर्षा।<br>
• 22 फसलों के लिए सिफारिश।<br>
• खेत की स्थिति के अनुसार सर्वोत्तम फसल।<br>
""",

        "pest_detection": "कीट पहचान",       
        "fruit_classification": "फल-सब्ज़ी पहचान",


    # --------------------- PEST ---------------------
    "pest_subtitle": "YOLO आधारित कीट पहचान",
    "pest_loading": "कीट पहचान की जा रही है...",
    "no_pest_found": "कोई कीट नहीं मिला!",
    "detected_pests": "पहचाने गए कीट:",

    "pest_classes": {
        "Prenolepis imparis": "प्रेनोलेपिस इमपारिस",
        "Pyrrhocoris apterus": "पायरोकोरिस एप्टरस",
        "Linepithema humile": "लाइनेपिथेमा ह्यूमाइल",
        "Oncopeltus fasciatus": "ऑन्कोपेल्टस फासियाटस",
        "Marpesia petreus": "मार्पेसिया पेट्रेयस",
        "Vespula germanica": "वेस्पुला जर्मानिका",
        "Magicicada septendecim": "मैजिकिकाडा सेप्टेंडिसिम",
        "Plecia nearctica": "प्लेशिया नियरक्टिका",
        "Oxythyrea funesta": "ऑक्सिथ्रिया फुनेस्टा",
        "Bombus rufocinctus": "बॉम्बस रूफोसिंक्टस",
        "Rhagonycha fulva": "रैगोनाइका फुल्वा",
        "Boisea trivittata": "बोइसेआ ट्राइविटाटा",
        "Orthemis ferruginea": "ओर्थेमिस फेरुगिनिया",
        "Enallagma cyathigerum": "एनालाग्मा सियाथिगेरम",
        "Coenagrion puella": "कोएनेग्रिऑन पुयेला",
        "Autographa gamma": "ऑटोग्राफा गामा",
        "Xylocopa virginica": "जाइलोकोपा वर्जिनिका",
        "Romalea microptera": "रोमालिया माइक्रोप्टेरा",
        "Vespula vulgaris": "वेस्पुला वल्गारिस",
        "Hetaerina americana": "हेटरिना अमेरिकाना"
    },


    # --------------------- PLANT DISEASE ---------------------
    "plant_disease": "पत्ती रोग पहचान",
    "plant_disease_sub": "एआई आधारित पत्ती की बीमारी पहचान",

    "invalid_img": "इमेज सही नहीं है। कृपया साफ JPG/PNG डालें।",
    "processing_image": "इमेज चेक की जा रही है...",
    "no_image": "शुरू करने के लिए फोटो अपलोड करें या कैमरे से लें।",

    "disease_classes": {
        "Apple – Apple Scab": "सेब – स्कैब रोग",
        "Apple – Black Rot": "सेब – काला सड़न रोग",
        "Apple – Cedar Apple Rust": "सेब – जंग रोग",
        "Apple – Healthy Leaf": "सेब – स्वस्थ पत्ती",

        "Blueberry – Healthy Leaf": "ब्लूबेरी – स्वस्थ पत्ती",

        "Cherry – Powdery Mildew": "चेरी – झुलसा (सफेद फफूंदी)",
        "Cherry – Healthy Leaf": "चेरी – स्वस्थ पत्ती",

        "Corn – Cercospora Leaf Spot (Gray Leaf Spot)": "मक्का – ग्रे लीफ स्पॉट",
        "Corn – Common Rust": "मक्का – जंग रोग",
        "Corn – Northern Leaf Blight": "मक्का – लीफ ब्लाइट",
        "Corn – Healthy Leaf": "मक्का – स्वस्थ पत्ती",

        "Grape – Black Rot": "अंगूर – ब्लैक रॉट",
        "Grape – Esca (Black Measles)": "अंगूर – एस्का रोग",
        "Grape – Leaf Blight (Isariopsis Leaf Spot)": "अंगूर – लीफ ब्लाइट",
        "Grape – Healthy Leaf": "अंगूर – स्वस्थ पत्ती",

        "Orange – Citrus Greening (Haunglongbing)": "संतरा – ग्रीनिंग रोग (एचएलबी)",

        "Peach – Bacterial Spot": "पीच – बैक्टीरियल धब्बा",
        "Peach – Healthy Leaf": "पीच – स्वस्थ पत्ती",

        "Bell Pepper – Bacterial Spot": "शिमला मिर्च – बैक्टीरियल धब्बा",
        "Bell Pepper – Healthy Leaf": "शिमला मिर्च – स्वस्थ पत्ती",

        "Potato – Early Blight": "आलू – अर्ली ब्लाइट",
        "Potato – Late Blight": "आलू – लेट ब्लाइट",
        "Potato – Healthy Leaf": "आलू – स्वस्थ पत्ती",

        "Raspberry – Healthy Leaf": "रास्पबेरी – स्वस्थ पत्ती",

        "Soybean – Healthy Leaf": "सोयाबीन – स्वस्थ पत्ती",

        "Squash – Powdery Mildew": "स्क्वैश – सफेद फफूंदी",

        "Strawberry – Leaf Scorch": "स्ट्रॉबेरी – लीफ स्कॉर्च",
        "Strawberry – Healthy Leaf": "स्ट्रॉबेरी – स्वस्थ पत्ती",

        "Tomato – Bacterial Spot": "टमाटर – बैक्टीरियल धब्बा",
        "Tomato – Early Blight": "टमाटर – अर्ली ब्लाइट",
        "Tomato – Late Blight": "टमाटर – लेट ब्लाइट",
        "Tomato – Leaf Mold": "टमाटर – लीफ मोल्ड",
        "Tomato – Septoria Leaf Spot": "टमाटर – सेप्टोरिया लीफ स्पॉट",
        "Tomato – Spider Mites (Two-Spotted Spider Mite)": "टमाटर – स्पाइडर माइट्स",
        "Tomato – Target Spot": "टमाटर – टार्गेट स्पॉट",
        "Tomato – Yellow Leaf Curl Virus": "टमाटर – येलो लीफ कर्ल वायरस",
        "Tomato – Mosaic Virus": "टमाटर – मोज़ेक वायरस",
        "Tomato – Healthy Leaf": "टमाटर – स्वस्थ पत्ती"

    
    }

}


# ================================================================
# AUTO-FALLBACK GETTER
# ================================================================
def get_text(lang: str):
    """
    Returns the correct language dictionary.
    Fallback priority:
        1) Hindi → if missing → English
        2) English → if missing → key returned
    """

    if lang.lower() == "hindi":
        return FallbackDict(HI_TEXT, EN_TEXT)
    else:
        return FallbackDict(EN_TEXT, EN_TEXT)


# ================================================================
# FALLBACK DICTIONARY CLASS
# ================================================================
class FallbackDict(dict):
    """
    A dict wrapper which looks up:
        Hindi → else English → else key
    Supports nested dicts also.
    """

    def __init__(self, primary: dict, fallback: dict):
        super().__init__(primary)
        self._primary = primary
        self._fallback = fallback

    def get(self, key, default=None):
        # If exists in primary (Hindi)
        if key in self._primary:
            return self._primary[key]

        # If exists in English fallback
        if key in self._fallback:
            return self._fallback[key]

        # If missing everywhere → return key itself
        return key

    # Nested dict fallback
    def __getitem__(self, key):
        if key in self._primary:
            return self._primary[key]

        if key in self._fallback:
            return self._fallback[key]

        return key
