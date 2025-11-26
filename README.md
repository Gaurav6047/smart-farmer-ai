---
title: "Smart Farmer AI"
emoji: "🚜"
colorFrom: "green"
colorTo: "yellow"
sdk: "gradio"
sdk_version: "4.31.4"
app_file: "main.py"
pinned: false
---

# Smart Farmer AI


# 🌱 **Smart Farmer AI**

### AI-Powered Crop Recommendation, Plant Disease Detection, Pest Detection, Fruit Classification & Scientific Fertilizer Engine

<p align="center">
  <img src="assets/banner.png" width="90%" />
</p>

<p align="center">
  <b>Streamlit • TFLite • YOLOv8 • RandomForest • Scientific STCR Engine</b>
</p>

---

# ⭐ **Badges**

<p align="center">
  <img src="https://img.shields.io/badge/Streamlit-App-brightgreen?style=for-the-badge">
  <img src="https://img.shields.io/badge/TFLite-Models-blue?style=for-the-badge">
  <img src="https://img.shields.io/badge/YOLOv8-Pest Detection-orange?style=for-the-badge">
  <img src="https://img.shields.io/badge/Fertilizer-STCR Engine-red?style=for-the-badge">
  <img src="https://img.shields.io/badge/ML-RandomForest-yellow?style=for-the-badge">
</p>

---

# 📌 **Overview**

**Smart Farmer AI** is a full-stack agricultural intelligence system designed for real-world farmers.
It integrates **multiple AI models**, scientific agriculture datasets, and a rule-based fertilizer engine — all inside one beautiful, mobile-optimized Streamlit UI.

✔ Photo → Disease/Pest/Fruit detection
✔ Soil data → Best Crop → Full Fertilizer Plan
✔ Works offline
✔ Lightweight + Fast
✔ Multilingual (English + Hindi)

---

# 🧠 **Features**

---

## 🌿 **Plant Disease Detection**

* 38-class **PlantVillage TFLite** model
* CPU-optimized (5–20 ms inference)
* High accuracy + mobile-friendly
* Full confidence score + alerts

---

## 🐛 **Pest Detection (YOLOv8)**

* Custom-trained YOLOv8 model
* Real-time detection
* Bounding boxes + confidence
* Works for Indian farm pests

---

## 🍎 **Fruit & Vegetable Classification**

* 36-class TFLite classifier
* Preprocessed for low-power devices
* High accuracy on common fruits/vegetables

---

## 🔀 **Auto Image Router**

Automatically routes image to:

* Plant Disease Page
* Pest Detection Page
* Fruit Classification Page
* Or Background Warning

Powered by **64×64 tiny CNN** — fast and lightweight.

---

## 🌾 **Crop Recommendation System (ML Model)**

A machine learning system trained using:

* N, P, K
* pH
* Rainfall
* Temperature
* Soil Type
* Region Data

Model Used: **RandomForestClassifier**

✔ Predicts best crop
✔ Provides confidence score
✔ Uses scaler for normalization
✔ Works offline
✔ Hindi + English support

Files:

```
models/crop_rf_final.pkl
models/scaler.pkl
```

---

## 🧪 **Scientific Fertilizer Recommendation Engine**

A professional-grade fertilizer engine built using:

* **STCR equations**
* **Indian soil fertility thresholds**
* **Micronutrient critical levels**
* **Organic nutrient substitution logic**
* **Legume rotation credits**
* **pH + EC correction rules**
* **Commercial NPK-to-bags conversion**

Outputs include:

✔ N, P₂O₅, K₂O (kg/ha)
✔ Organic credits deduction
✔ Urea, DAP, MOP bags
✔ Micronutrient recommendations
✔ Soil correction alerts
✔ Agronomic notes
✔ Full calculation breakdown

Uses the following datasets:

```
models/soil_fertility.json
models/standard_npk.csv
models/stcr_equations.json
models/organic_rules.json
```

---
# 📁 **Project Structure**

```
smart-farmer/
│── main.py
│── router.py
│── requirements.txt
│
│── pages/
│   ├── 🌿_Plant_Disease.py
│   ├── 🐛_Pest_Detection.py
│   ├── 🍎_Fruit_Classification.py
│   ├── 🔀_Auto_Routing.py
│   ├── 📊_Crop_Recommendation.py
│   ├── 🧪_Fertilizer_Recommendation.py
│   └── 📘_Fertilizer_Engine_Info.py
│
│── engine/
│   ├── recommender.py
│   ├── stcr.py
│   ├── organic_rules.py
│   ├── brand_converter.py
│   ├── thresholds.py
│   ├── loader.py
│   └── auto_crop.py
│
│── models/
│   ├── plant_disease.tflite
│   ├── fruit_model.tflite
│   ├── pest_model.pt
│   ├── router_model.tflite
│   ├── soil_fertility.json
│   ├── standard_npk.csv
│   ├── stcr_equations.json
│   ├── organic_rules.json
│   ├── crop_rf_final.pkl
│   └── scaler.pkl
│
│── utils/
│   ├── theme.py
│   ├── language.py
│   ├── result_box.py
│   ├── preprocess.py
│   ├── postprocess.py
│   └── model_loader.py
│
└── assets/
```

---

# ⚙️ Installation

```bash
pip install -r requirements.txt
streamlit run main.py
```

---

# ☁️ Deploy on Streamlit Cloud

1. Upload to GitHub
2. Go to [https://share.streamlit.io](https://share.streamlit.io)
3. Select `main.py`
4. Deploy → Done 🎉

---

# 📱 Mobile-Optimized

✔ Touch-friendly
✔ Responsive grid
✔ Camera input
✔ Smooth animations
✔ Dark/Light friendly

---

# 🔮 Future Enhancements

* AI Voice Assistant (Hindi + English)
* Offline Android App
* Weather-aware crop planning
* Yield prediction model
* Auto fertilizer schedule based on NDVI

---

# ✨ Author

**Gaurav — Machine Learning Engineer**
Building practical & intelligent AI for agriculture 🌱

---

