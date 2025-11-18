# 🌱 Smart Farmer AI  
### AI-Powered Plant Disease, Pest Detection & Fruit Classification

Smart Farmer AI is a multi-model agricultural assistant built using **Streamlit**, **TensorFlow Lite**, and **YOLOv8**.  
It helps farmers identify **plant diseases, pests, fruits/vegetables**, and provides **auto routing + troubleshooting guides** — all in a simple mobile-friendly UI.

---

## 🚀 Features

### 🌿 Plant Disease Detection (TFLite Model)
- 38 PlantVillage disease classes  
- Fast, mobile-friendly 224×224 classifier  
- High accuracy model optimized for deployment  

### 🐛 Pest Detection (YOLOv8)
- Real-time insect detection  
- Bounding boxes + confidence score  
- 20 labeled pest classes  

### 🍎 Fruit & Vegetable Classification
- 36-class Fruit & Veg classifier  
- TFLite inference < 5ms  
- Works perfectly on low-end devices  

### 🔀 Auto Image Routing
- Automatically decides:
  - Leaf  
  - Fruit  
  - Pest  
  - Background  
- Routes user to the correct model page  

### 📘 Model Classes Information
- Lists all classes from all models  
- CSV + JSON based dynamic loading  

### ❓ Wrong Prediction Troubleshooting
- Helps users retake better quality photos  
- Covers focus, lighting, angle & visibility  

---

## 🌐 Tech Stack

| Component | Technology |
|----------|------------|
| Web UI | Streamlit |
| Plant Model | TensorFlow Lite |
| Fruit Model | TFLite |
| Pest Model | YOLOv8 |
| Router Model | TFLite 64×64 CNN |
| Theme | Custom CSS + Premium UI |
| Deployment | Streamlit Cloud |

---

## 📁 Project Structure
smart-farmer/
│── main.py
│── pages/
│── utils/
│── models/
│── assets/
│── requirements.txt
│── README.md


---

## 🧠 Models Used
- `plant_desease.tflite` — 38-class PlantVillage  
- `pest_model.pt` — YOLOv8 custom trained  
- `fruit_model.tflite` — 36-class fruits/veg  
- `router_model.tflite` — image type classifier  

---

## 📦 Installation
pip install -r requirements.txt
streamlit run main.py


---

## 🌍 Deployment (Streamlit Cloud)
1. Upload project to GitHub  
2. Go to: https://share.streamlit.io  
3. Connect GitHub repo  
4. Select `main.py`  
5. Deploy 🎉  

---

## 📱 Mobile-Optimized UI
- Fully responsive  
- Camera input supported  
- Glassmorphism theme  
- Premium green color palette  

---

## 🔮 Future Features
- Soil Nutrient Classification  
- NPK-Based Crop Recommendation  
- Fertilizer Recommendation Engine  
- Yield Prediction Model  
- Offline Android App (Kivy/Flutter)  

---

## 🧑‍💻 Author
**Gaurav (Machine Learning Engineer)**  
Smart AI tools for agriculture 🌱  
