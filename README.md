# 🌱 Smart Farmer AI

### **AI-Powered Plant Disease, Pest Detection, Fruit Classification & Intelligent Fertilizer Recommendations**

**Smart Farmer AI** is an end-to-end agricultural intelligence system designed for real-world farmers.
It brings together multiple AI models — **Plant Disease Classifier, Pest Detector, Fruit Classifier, Image Router**, and a **Rule-Based Fertilizer + INM Engine** — all inside one clean, mobile-first Streamlit UI.

The goal is simple:
**Help farmers take a photo → get instant diagnosis → get treatment → get fertilizer plan.**

---

## 🚀 Key Features

### 🌿 Plant Disease Detection

* 38-class **PlantVillage** TFLite model
* Optimized for mobile (fast 224×224 classifier)
* High accuracy with extremely small footprint

### 🐛 Pest Detection (YOLOv8)

* Custom-trained YOLOv8 model
* Real-time insect detection
* Bounding boxes + confidence scores
* Works on images & live camera

### 🍎 Fruit & Vegetable Classification

* 36-class TFLite Fruit & Veg model
* < 5 ms inference on CPU
* Ideal for mobile devices & low-power boards

### 🔀 Auto Image Routing (Router Model)

A custom lightweight CNN automatically decides whether the image is of a:

* Leaf
* Pest
* Fruit/Vegetable
* Or irrelevant background

Based on this, the user is automatically routed to the correct page.

### 🧪 Fertilizer Recommendation Engine (NEW)

A complete rule-based engine built from:

* STCR equations
* Soil fertility rating rules
* Micronutrient critical limits
* ACZ-specific INM packages
* Organic substitution rules (FYM, compost, oilcake)
* Environmental & soil constraints (acidic/alkali/P-rich soils)

Outputs:
✔ Recommended N, P₂O₅, K₂O (kg/ha)
✔ Micronutrient doses (Zn, Fe, S, Mn, B)
✔ Organic fertilizer equivalents
✔ Soil correction measures
✔ And expected economic benefits

### 📘 Model Classes Information

* Dynamic loading of class names from CSV/JSON
* Clean UI for browsing all categories

### ⚠️ Wrong Prediction Troubleshooting

Helps farmers click better photos
(focus, lighting, angle, zoom, leaf clarity)

---

## 🌐 Tech Stack Overview

| Component         | Technology                              |
| ----------------- | --------------------------------------- |
| Web UI            | Streamlit                               |
| Disease Model     | TensorFlow Lite                         |
| Fruit Model       | TFLite                                  |
| Pest Model        | YOLOv8                                  |
| Router Model      | TFLite (64×64 CNN)                      |
| Fertilizer Engine | Python rule-based + scientific datasets |
| Data              | CSV/JSON/YAML                           |
| Deployment        | Streamlit Cloud                         |

---

## 📁 Project Structure

```
smart-farmer/
│── main.py
│── pages/
│   ├── plant_disease.py
│   ├── pest_detection.py
│   ├── fruit_classifier.py
│   ├── fertilizer_engine.py
│── models/
│   ├── plant_disease.tflite
│   ├── fruit_model.tflite
│   ├── router_model.tflite
│   └── pest_model.pt
│── utils/
│   ├── image_preprocessing.py
│   ├── fertilizer_rules.py
│   └── classes_loader.py
│── assets/
│── datasets/
│── requirements.txt
└── README.md
```

---

## 🧠 Models Included

| Model                  | Purpose                               |
| ---------------------- | ------------------------------------- |
| `plant_disease.tflite` | 38-class PlantVillage classifier      |
| `pest_model.pt`        | YOLOv8 insect detector                |
| `fruit_model.tflite`   | 36-class fruit & vegetable classifier |
| `router_model.tflite`  | Auto image routing CNN                |

---

## 📦 Installation

```bash
pip install -r requirements.txt
streamlit run main.py
```

---

## 🚀 Deployment on Streamlit Cloud

1. Push project to GitHub
2. Visit [https://share.streamlit.io](https://share.streamlit.io)
3. Connect your repo
4. Select `main.py`
5. Deploy instantly — done 🎉

---

## 📱 Mobile-Optimized UI

* Fully responsive
* Camera input support
* Premium green theme
* Smooth animations
* Touch-friendly controls

---

## 🔮 Future Roadmap

* Soil Nutrient Classification (image + text input)
* NPK-Based Crop Recommendation ML Model
* Yield Prediction Module (Regression + Rules)
* Offline Android App (Kivy/Flutter)
* Voice-based Farmer Assistant (Hindi + English)
* Weather-aware fertilizer scheduling

---

## 🧑‍💻 Author

**Gaurav – Machine Learning Engineer**
Smart AI tools for next-gen agriculture 🌱

---
