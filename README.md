# Smart Farmer AI

Smart Farmer AI is a multi-module agricultural decision support system designed to demonstrate how Machine Learning, Deep Learning, and scientific agronomy models can be combined into a single practical application for real farming conditions.

The project focuses on **decision assistance**, not just prediction. It integrates image-based diagnosis, soil-based crop planning, scientific fertilizer calculation, and irrigation scheduling into one unified workflow.

This system is developed as a **serious academic and applied AI project**, suitable for:
- Final year engineering / MCA / BCA projects  
- Precision agriculture research demonstrations  
- ML + Computer Vision integration showcases  

---

## Project Objective

The primary objective of Smart Farmer AI is to assist farmers (or agriculture researchers) in making **data-driven decisions** related to:

- Crop selection based on soil and climate  
- Disease and pest identification using images  
- Fertilizer planning using scientific equations  
- Irrigation scheduling using FAO-56 methodology  

Instead of using a single AI model, this project demonstrates how **multiple independent AI systems can work together as one intelligent pipeline**.

---

## Key Capabilities

### Plant Disease Detection  
A deep learning model based on TensorFlow Lite is used to classify plant leaf diseases. The model is optimized for CPU inference and supports multiple crop disease classes. The output includes both the predicted label and confidence score.

### Pest Detection  
A YOLO-based object detection model is used to detect agricultural pests from images. It provides bounding boxes and confidence values, making it suitable for real-time pest monitoring scenarios.

### Fruit and Vegetable Classification  
A lightweight classification model identifies different fruits and vegetables from images. This module demonstrates practical computer vision deployment for agricultural produce recognition.

### Automatic Image Routing  
A small CNN-based router automatically decides whether an uploaded image belongs to disease detection, pest detection, or fruit classification. This removes the need for manual user selection and improves workflow automation.

---

## Crop Recommendation System

This module is built using a supervised machine learning approach.  
It predicts the most suitable crop using multiple soil and environmental parameters:

- Nitrogen (N)  
- Phosphorus (P)  
- Potassium (K)  
- Soil pH  
- Rainfall  
- Temperature  
- Soil type / region  

The model uses a Random Forest classifier and works entirely offline once deployed. The result is presented in both English and Hindi.

---

## Fertilizer Recommendation Engine (STCR Based)

This is one of the most technically significant parts of the project.

The fertilizer engine is not a simple lookup system. It is built using:

- Targeted yield based STCR equations  
- Indian soil fertility threshold values  
- Organic nutrient adjustment rules  
- Micronutrient deficiency logic  
- Soil pH and EC correction rules  
- Commercial fertilizer bag conversion  

The engine calculates:
- Required N, P₂O₅, K₂O (kg/ha)  
- Organic nutrient deductions  
- Urea, DAP, and MOP bag quantities  
- Zinc, Boron and other deficiency alerts  
- Agronomic advisory notes  

All calculations are shown step-by-step, making the model transparent and explainable.

---

## Irrigation Scheduling System (FAO-56)

The irrigation module is based on the FAO-56 methodology. It includes:

- Reference evapotranspiration (ET₀)  
- Crop coefficient (Kc) based crop evapotranspiration (ETc)  
- Daily soil water balance  
- Rainfall adjustments  
- Irrigation duration based on pump horsepower  
- A short-term 3-day irrigation forecast using XGBoost  

This module simulates how irrigation planning is performed in scientific agronomy.

---

## System Characteristics

- Fully offline after setup  
- CPU-only deployment  
- Multilingual output (English and Hindi)  
- Suitable for low-resource environments  
- Modular architecture  
- Designed for clarity, not black-box prediction  

---

## Installation and Local Execution

```bash
pip install -r requirements.txt
streamlit run app.py
