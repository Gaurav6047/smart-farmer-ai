
# Smart Farmer AI — Technical Documentation

---

## 1. Purpose and Intended Audience

This document provides a complete scientific and implementation-level explanation of the Smart Farmer AI system. It is written for:

- Academic supervisors and project evaluators  
- Engineers who wish to reproduce or extend the system  
- Domain experts who want to examine the agronomic logic  

The document covers system architecture, model pipelines, equations, preprocessing, training and evaluation methodology, data flow, reproducibility steps, limitations, and future extensions.

---

## 2. System Overview (End-to-End Flow)

High-level processing flow:

User (image + soil report + location + metadata)
├── Image Router → {Plant Disease, Pest Detection, Fruit Classification}
├── Crop Recommendation Model ← Soil & Climate Features
└── Agronomy Engines
├── Fertilizer Engine (STCR / NPK / Organic Rules)
└── Irrigation Engine (FAO-56 + ML Forecast)

Final Output → Structured Advisory (JSON / PDF)

pgsql
Copy code

Each module operates independently and returns a structured output. A final aggregator combines these results into a complete advisory report.

---

## 3. Vision Pipeline

### 3.1 Automatic Image Router

**Purpose:**  
Automatically classifies an input image as `leaf`, `pest`, or `fruit` to select the correct vision model.

**Model:**  
Lightweight CNN (3–4 convolution layers), input size 64×64.

**Preprocessing:**  
- Resize to 64×64  
- Normalize pixel values to 0–1  
- RGB channel order  

**Inference:**  
Softmax output → highest probability class selected.

**Thresholding:**  
If confidence < 0.55, the image is rejected as poor-quality/background.

**Rationale:**  
Early routing prevents unnecessary execution of heavy detection models and simplifies the user workflow.

---

### 3.2 Plant Disease Detection (TFLite)

**Objective:**  
Classify plant leaf images into disease categories.

**Model Type:**  
Convolutional Neural Network trained in TensorFlow/Keras and exported to TensorFlow Lite for CPU deployment.

**Preprocessing Steps:**
1. Load image using PIL/OpenCV  
2. Resize to input resolution (e.g., 224×224)  
3. Normalize pixel values (0–1)  
4. Add batch dimension  

**Inference (conceptual):**
- Load TFLite interpreter  
- Pass input tensor  
- Extract probability vector  
- Select class with maximum probability  

**Output Format:**
```json
{
  "label": "Bacterial_blight",
  "confidence": 0.92,
  "advice": "Remove affected leaves and apply recommended control"
}
Evaluation Requirements:

Classification report (Precision, Recall, F1-score)

Confusion matrix

Top-1 accuracy

3.3 Pest Detection (YOLO)
Objective:
Detect pests in images with bounding boxes.

Framework:
Ultralytics YOLOv8 (PyTorch)

Inference Pipeline:

Input image resized with aspect preservation

Forward pass through YOLO network

Non-Max Suppression (NMS)

Bounding box extraction

Output Example:

json
Copy code
[
  {"label": "aphid", "confidence": 0.81, "bbox": [x1, y1, x2, y2]}
]
Evaluation Metrics:

mAP@0.5

Precision and Recall per class

PR curves

Deployment Note:
Optimized for CPU inference with reduced image size. Real-time camera usage is recommended only in local environments.

3.4 Fruit and Vegetable Classification
The fruit classification module follows the same TFLite workflow as plant disease detection:

Resize → Normalize → TFLite inference → Softmax → Label mapping

Evaluation through per-class confusion matrices and accuracy.

4. Crop Recommendation System (Random Forest)
Objective:
Predict the most suitable crop based on soil and climatic parameters.

Input Features:

Nitrogen (N)

Phosphorus (P)

Potassium (K)

pH

Temperature

Humidity

Rainfall

Soil type / region (encoded)

Preprocessing:

Feature scaling using scaler.pkl

Categorical encoding using label_encoder.pkl

Model:
RandomForestClassifier trained using supervised learning.

Inference Logic:

python
Copy code
X_scaled = scaler.transform(X_raw)
probs = model.predict_proba(X_scaled)
prediction = class_with_max_probability
Evaluation:

k-fold cross-validation

Confusion matrix

Feature importance analysis

5. Fertilizer Recommendation Engine (STCR / NPK / Organic)
This engine converts soil test values into actionable fertilizer advice using agronomic principles.

5.1 STCR (Soil Test Crop Response) Concept
Nutrient requirement is estimated using linear response equations:

ini
Copy code
Sx = ax × (Yt − Yb) + bx
Where:

Sx = nutrient requirement (kg/ha)

Yt = target yield (t/ha)

Yb = baseline yield from soil fertility

ax, bx = crop-specific coefficients

5.2 Processing Steps
Normalize all soil and unit inputs

Select computation mode (AUTO/STCR/NPK)

Compute nutrient demand

Subtract soil-available nutrients

Apply organic nutrient credits

Detect micronutrient deficiencies

Convert nutrients to fertilizer bags

Generate explainable advisory output

5.3 Fertilizer Conversions
Urea (46% N): Urea = N / 0.46

DAP (46% P₂O₅): DAP = P₂O₅ / 0.46

MOP (60% K₂O): MOP = K₂O / 0.60

5.4 Output Structure
json
Copy code
{
  "mode": "STCR",
  "nutrient_gap": {"N": 120, "P2O5": 60, "K2O": 40},
  "fertilizer_bags": {"Urea": 260, "DAP": 130, "MOP": 67},
  "micronutrients": {"Zn": "Apply 25 kg ZnSO4/ha"},
  "explanation": "Full calculation breakdown"
}
6. Irrigation Engine (FAO-56 + Forecast)
6.1 FAO-56 Equation
ini
Copy code
ETc = Kc × ET0
Where:

ET0 = reference evapotranspiration

Kc = crop coefficient

ETc = crop water requirement

6.2 Soil Water Balance
mathematica
Copy code
ΔS = P_eff + I − ETc − D
6.3 Pump Runtime Calculation
ini
Copy code
Hours = Water_volume / Pump_discharge
6.4 Forecasting
A short-term XGBoost model forecasts ETc for 3 days using historical weather features.

7. Training and Evaluation
Each model must document:

Dataset size and splits

Augmentations

Training hyperparameters

Loss curves

Evaluation metrics

8. Reproducibility
bash
Copy code
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
9. Limitations and Responsible Use
The system provides advisory support only

Vision models depend heavily on image quality

Soil values must be laboratory tested

Forecasting depends on weather data accuracy

10. Supervisor Evaluation Checklist
Live demo of application

Review of engine code

Confusion matrices and mAP metrics

At least 3 documented case studies

11. Extensions
Regional STCR calibration

Mobile app deployment

NDVI and satellite integration

Cost optimization of fertilizer selection

12. Files Expected in Repository
kotlin
Copy code
README.md  
docs/TECHNICAL.md  
models/  
data/  
results/  
notebooks/  
app.py  
requirements.txt  
LICENSE  
