# Smart Farmer AI

Smart Farmer AI is an integrated, modular agricultural decision-support system that combines image-based diagnostics (disease, pest, and produce classification) with data-driven crop recommendation and scientifically grounded agronomy engines for fertilizer and irrigation planning. The system is designed for CPU execution and is exposed through a unified Streamlit interface to support complete end-to-end operation.

This document describes the project purpose, architectural design, core components, execution workflow, known limitations, and the minimum requirements for academic evaluation.

---

## Purpose and Scope

Smart Farmer AI is intended as a **decision-assistance system**, not an automated control platform. It generates explainable advisories based on multiple data sources and machine learning models so that users can understand the reasoning behind each recommendation.

The project demonstrates:

- Practical integration of multiple ML and deep learning models into a single application  
- Transparent agronomic calculations using scientific formulations (STCR, soil fertility thresholds, organic credits)  
- Irrigation scheduling based on FAO-56 principles with a short-term machine learning forecast  

It is suitable for:
- Final year engineering / MCA / BCA projects  
- Precision agriculture research demonstrations  
- Applied AI and computer vision integration studies  

---

## High-Level System Architecture (Conceptual)

User interaction is divided into three main processing pipelines:

### 1. Image Analysis Pipeline  
User images are automatically routed to the correct vision model. Depending on image type, the system performs:
- Plant disease classification  
- Pest detection using object detection  
- Fruit and vegetable classification  

Outputs include the predicted label, confidence score, and visual overlays for detected objects.

### 2. Crop Recommendation Pipeline  
Numerical soil and environmental inputs are scaled and passed to a trained Random Forest model. The system predicts the most suitable crop along with a confidence score. This module runs completely offline once the trained model files are available.

### 3. Agronomy Engines  
Two independent but coordinated engines operate:

- **Fertilizer engine**: Uses STCR equations, organic nutrient adjustments, micronutrient rules, soil correction logic, and fertilizer bag conversion. It outputs a complete nutrient prescription and agronomic advisory.  
- **Irrigation engine**: Implements FAO-56 ET₀ and ETc computation, soil water balance, pump-based irrigation duration, and a 3-day XGBoost-based irrigation forecast.

---

## Major Software Components

### Application Entry and Interface
- `app.py` serves as the main Streamlit entry point and controls global UI, routing, and language handling.

### Vision Modules
- Automatic image router for model selection  
- TFLite-based plant disease classifier  
- YOLO-based pest detection module  
- TFLite-based fruit and vegetable classifier  

### Crop Recommendation Module
- Soil parameter input form  
- Feature scaling and Random Forest inference  
- Multilingual output of predicted crop  

### Fertilizer Recommendation Engine
- STCR-based nutrient computation  
- Organic nutrient credit adjustments  
- Micronutrient deficiency detection  
- Soil correction warnings (pH, EC)  
- Commercial fertilizer bag conversion  
- Structured final advisory generation  

### Irrigation Engine
- FAO-56 ET₀ and ETc computation  
- Daily soil water balance  
- Rainfall correction  
- Pump horsepower-based irrigation duration  
- Short-term ML-based irrigation forecasting  

---

## Inputs and Outputs (Summary)

### Crop Recommendation
- **Input:** N, P, K, pH, temperature, humidity, rainfall  
- **Output:** Recommended crop with confidence score  

### Fertilizer Engine
- **Input:** Location, crop, season, soil values, organic input, target yield (optional)  
- **Output:** Nutrient gaps, fertilizer bags (urea, DAP, MOP), micronutrient alerts, and advisory notes  

### Irrigation Engine
- **Input:** Geographic location, crop stage, soil type, pump horsepower, field area  
- **Output:** Daily ETc, water requirement, irrigation duration, and short-term irrigation forecast  

### Vision Modules
- **Input:** Uploaded image or camera frame  
- **Output:** Class label, confidence score, and visualization  

---

## Reproducibility and Local Execution

A virtual environment is recommended.

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
If large model files are tracked using Git LFS, Git LFS must be installed and initialized before cloning.

Practical Limitations
Camera-based live inference works only in local environments

Vision model accuracy depends on lighting conditions and image quality

Soil health values are assumed to be laboratory-tested inputs

The system provides decision support, not guaranteed yield predictions

These limitations are acknowledged as part of responsible deployment.

Academic Evaluation Requirements
To make the project defensible for examination or publication, the following must be documented:

Classification reports and confusion matrices for all models

mAP, precision, and recall for the pest detection system

At least three real or simulated farmer case studies

Documentation of training datasets, splits, and evaluation strategy

Author
Gaurav
Machine Learning Engineer (India)

This project is developed to demonstrate how artificial intelligence can be applied at multiple levels of agricultural decision-making.

License
MIT License
Free for educational and research use.
