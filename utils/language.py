def get_text(lang):
    TEXT = {

        "English": {
            # Home Page
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
            "crop_recommendation": "Crop Recommendation",
            "fertilizer_engine": "Fertilizer Recommendation",

            # Extra
            "take_photo": "Take Photo",
            "select_lang": "Language",
        },


        "Hindi": {
            # Home Page
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
            "crop_recommendation": "फसल सुझाव",
            "fertilizer_engine": "उर्वरक सिफारिश इंजन",

            # Extra
            "take_photo": "फोटो लें",
            "select_lang": "भाषा",
        }
    }

    return TEXT[lang]
