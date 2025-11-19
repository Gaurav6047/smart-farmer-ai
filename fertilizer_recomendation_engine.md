```markdown
# 🌱 Smart Fertilizer Engine  
### Precision NPK Recommendation using STCR + IPNS + Soil Test Analysis

The Smart Fertilizer Engine is a **production-grade, modular, rule-based agronomy system** that generates accurate fertilizer recommendations for Indian crops.  
It supports both **Standard NPK guidelines** and **STCR (Soil Test Crop Response)** targeted-yield calculations.

This engine powers a Streamlit UI and an optional FastAPI backend.

---

# 🚀 Features

### ✔ Scientific NPK Recommendation  
- Standard agronomic values (ICAR/SAU)
- STCR equations for targeted yields  
- Soil-test based corrections

### ✔ Soil Analysis  
- Macro nutrients (N, P, K)  
- Micro nutrients (Zn, Fe, Mn, Cu, B, S)  
- pH & EC evaluation  
- Soil-type logic (acidic/alkaline)

### ✔ IPNS Organic Nutrient Credits  
- FYM  
- Vermicompost  
- Oilseed cakes  
- Auto deduction of organic nutrient contributions

### ✔ Special Agronomic Rules  
- pH correction (lime/gypsum recommendations)  
- EC warnings (salinity)  
- Legume rotation N credit  
- Micronutrient deficiency alerts  

### ✔ Bag Conversion (Farmer-Friendly Output)  
Converts elemental N-P₂O₅-K₂O into:

- Urea (46% N, 45 kg bag)
- DAP (18% N, 46% P₂O₅, 50 kg bag)
- MOP (60% K₂O, 50 kg bag)

### ✔ Smart Crop Suggestion  
Auto-suggests crops based on:

- State  
- Season (Kharif, Rabi, Zaid)

---

# 🧠 System Architecture

```

engine/
│── thresholds.py          # Soil macro/micro evaluation
│── npk_standard.py        # Standard NPK recommendations
│── stcr.py                # STCR targeted-yield model
│── organic_rules.py       # Organic credits + special rules
│── brand_converter.py     # Urea/DAP/MOP conversion
│── auto_crop.py           # Crop suggestions
│── recommender.py         # Main orchestrator
│── loader.py              # JSON/CSV loader with caching

models/
│── soil_fertility.json
│── organic_rules.json
│── stcr_equations.json
│── standard_npk.csv

pages/
│── 🧪_Fertilizer_Recommendation.py   # Streamlit UI

api/
│── main.py
│── schemas.py
│── routes/
└── fertilizer.py

````

---

# 📊 How the Engine Works

## 1. Soil Analysis (thresholds.py)
Classifies soil as **Low / Medium / High** for N, P, K using JSON thresholds.  
Detects micronutrient deficiencies using critical limits.

Example output:
```json
{"N": "Low", "P": "Medium", "K": "High"}
````

---

## 2. Standard NPK (npk_standard.py)

Reads `standard_npk.csv` and finds the correct N-P₂O₅-K₂O based on:

* Crop name (fuzzy match)
* Condition (irrigated / rainfed)

```json
{"N": 120, "P2O5": 60, "K2O": 40}
```

---

## 3. STCR Targeted Yield (stcr.py)

Uses government STCR equations:

```
N = 4.5*T - 0.32*SN
```

Produces:

```json
{"N": 110, "P2O5": 55, "K2O": 65}
```

---

## 4. Organic Credits (organic_rules.py)

Subtracts nutrients supplied by organics:

* FYM
* Vermicompost
* Oilseed cakes

Also applies:

* pH alerts
* EC alerts
* Legume rotation N credit
* Micronutrient triggers

---

## 5. Fertilizer Bag Conversion (brand_converter.py)

Converts N-P₂O₅-K₂O into bags:

```json
{
  "bags": {"Urea": 2.0, "DAP": 2.6, "MOP": 1.2},
  "kg": {"Urea": 90, "DAP": 130, "MOP": 60}
}
```

---

## 6. Recommender Orchestration (recommender.py)

This is the master engine combining all steps:

1. Soil thresholds
2. Micronutrient warnings
3. STCR or Standard
4. Organic credits
5. Special rules
6. Bag conversion
7. Final structured output

---

# 🖥 Streamlit UI

Located at:

```
pages/🧪_Fertilizer_Recommendation.py
```

Features:

* English/Hindi switch
* Soil input
* State + season
* Auto crop suggestion
* Custom crop
* STCR support
* Organic input section
* Results with bags + warnings + breakdown

---

# 🔌 FastAPI Backend (Optional)

## Endpoint:

```
POST /api/v1/recommend
```

## Request:

```json
{
  "crop": "Wheat",
  "soil": { "N": 180, "P": 20, "K": 150 },
  "target_yield": 45,
  "organic_inputs": { "FYM": 2000 },
  "meta": { "state": "Punjab", "season": "Rabi" }
}
```

## Response:

Full recommendation JSON.

---

# 📚 Data Authenticity

### The engine uses real agronomy values from:

* ICAR STCR methodology
* State Agricultural Universities (SAU)
* Soil Health Card norms
* Indian fertilizer bag composition standards
* IPNS organic manure composition

It is scientifically reliable for most Indian conditions.

---

# 🛠 Installation

```
pip install -r requirements.txt
streamlit run main.py
```

---

# 🧪 Running the API

```
uvicorn api.main:app --reload --port 8000
```

---

# 🤝 Contributing

This project is fully modular.
You can extend:

* More crops
* State-specific STCR equations
* More micronutrient data
* Additional organic manure types
* UI improvements
* ML-based nutrient prediction

---

# 📄 License

All Rights Reserved © 2025 Gaurav  
This project is not open-source.  
Unauthorized copying, modification, or commercial use is prohibited.

---

# 💬 Contact

For improvements, collaboration, or issues, please open an issue in this repository.  
You can also connect here:

📧 Email: gk917675@gmail.com
