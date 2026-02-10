# ==================================================================================
# 🔥 SMART FARMER ENGINE — REWRITTEN FOR "FINAL_HARD_NORMALIZED" DATASET
# ==================================================================================

import json
import os
import ast
import operator
from pathlib import Path

# =============================================================================
# 1. CONFIGURATION & DATA LOADING
# =============================================================================

# Define file names based on your upload
FILE_MAIN = "final_hard_normalized.json"
FILE_ORG  = "organic_rules.json"
FILE_SOIL = "soil_fertility_thresholds.json"

# Dynamic Path Setup (Works on any machine)
BASE_DIR = Path(__file__).parent if "__file__" in locals() else Path.cwd()
DATA_DIR = BASE_DIR / "data"  # Assuming JSONs are in a 'data' subfolder

def load_json_safe(filename):
    """Loads JSON from data directory with error handling."""
    path = DATA_DIR / filename
    # Fallback to current directory if data folder doesn't exist
    if not path.exists():
        path = BASE_DIR / filename
    
    if not path.exists():
        print(f"❌ CRITICAL ERROR: File not found: {filename}")
        return {}
    
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ ERROR: Could not parse {filename}. Reason: {e}")
        return {}

# =============================================================================
# 2. NORMALIZATION UTILITIES (CRITICAL FOR YOUR DATASET)
# =============================================================================

def standardize_key(text):
    """Converts 'Andhra Pradesh' -> 'andhra_pradesh' to match your JSON keys."""
    if not text: return ""
    return str(text).strip().lower().replace(" ", "_")

# Mapping user input soil names to your JSON's specific keys
SOIL_MAP = {
    "red": "red_soil",
    "red soil": "red_soil",
    "black": "black_soil",
    "black soil": "black_soil",
    "vertisol": "vertisol",  # Some entries in your JSON use scientific names
    "alfisol": "alfisol",
    "alluvial": "alluvial",
    "sandy": "sandy",
    "laterite": "lateritic",
    "lateritic": "lateritic",
    "calcareous": "calcareous"
}

def normalize_soil_type(user_input):
    clean = str(user_input).strip().lower()
    return SOIL_MAP.get(clean, clean)

def safe_float(val):
    try:
        return float(val)
    except:
        return 0.0

# =============================================================================
# 3. MATH ENGINE (AST EVALUATOR)
# =============================================================================

_ALLOWED_OPS = {
    ast.Add: operator.add, ast.Sub: operator.sub,
    ast.Mult: operator.mul, ast.Div: operator.truediv,
    ast.USub: operator.neg
}

def solve_equation(equation_str, variables):
    """Safely solves equations like '4.38*T - 0.28*SN' using soil data."""
    if not equation_str or not isinstance(equation_str, str):
        return 0.0
    try:
        tree = ast.parse(equation_str, mode='eval')
        
        def _eval(node):
            if isinstance(node, ast.Constant): return node.value
            if isinstance(node, ast.Name): return variables.get(node.id, 0.0)
            if isinstance(node, ast.BinOp):
                return _ALLOWED_OPS[type(node.op)](_eval(node.left), _eval(node.right))
            if isinstance(node, ast.UnaryOp):
                return _ALLOWED_OPS[type(node.op)](_eval(node.operand))
            return 0.0
            
        return max(0.0, _eval(tree.body)) # Never return negative fertilizer
    except Exception as e:
        # print(f"Math Error in '{equation_str}': {e}")
        return 0.0

# =============================================================================
# 4. CORE LOGIC COMPONENT
# =============================================================================

class SmartFarmerEngine:
    def __init__(self):
        # Load datasets
        self.main_data = load_json_safe(FILE_MAIN)
        self.organic_data = load_json_safe(FILE_ORG)
        self.soil_data = load_json_safe(FILE_SOIL)

    def get_organic_credit(self, manure_name, qty_kg):
        """Calculates NPK supplied by organic manure."""
        if not manure_name or qty_kg <= 0:
            return {"N": 0, "P2O5": 0, "K2O": 0}
        
        # Search in manure and oilseed_cakes lists
        sources = self.organic_data.get("organic_inputs", {}).get("manure", []) + \
                  self.organic_data.get("organic_inputs", {}).get("oilseed_cakes", [])
        
        for source in sources:
            # Fuzzy match name
            if manure_name.lower() in source["name"].lower():
                return {
                    "N": (safe_float(source.get("N_percent")) / 100) * qty_kg,
                    "P2O5": (safe_float(source.get("P2O5_percent")) / 100) * qty_kg,
                    "K2O": (safe_float(source.get("K2O_percent")) / 100) * qty_kg
                }
        return {"N": 0, "P2O5": 0, "K2O": 0}

    def check_micronutrients(self, soil_test):
        """Checks thresholds from soil_fertility_thresholds.json."""
        recommendations = {}
        thresholds = self.soil_data.get("critical_levels", {})
        
        # Logic: If Soil Value < Critical Limit -> Recommend
        if safe_float(soil_test.get("Zn")) < safe_float(thresholds.get("Zn_critical", 0.6)):
            recommendations["Zinc"] = "Apply ZnSO4 @ 25 kg/ha"
            
        if safe_float(soil_test.get("Fe")) < safe_float(thresholds.get("Fe_critical", 4.5)):
            recommendations["Iron"] = "Apply FeSO4 @ 50 kg/ha"
            
        if safe_float(soil_test.get("S")) < safe_float(thresholds.get("S_critical", 10.0)):
            recommendations["Sulphur"] = "Apply Gypsum @ 40 kg/ha"

        if safe_float(soil_test.get("B")) < 0.5: # Hardcoded fallback if missing in JSON
             recommendations["Boron"] = "Apply Borax @ 10 kg/ha"

        return recommendations

    def recommend(self, state, crop, season, soil_test, organic_input=None):
        """
        Main Engine Function.
        """
        # 1. Normalize Inputs
        std_state = standardize_key(state)
        std_crop = standardize_key(crop)
        std_season = standardize_key(season)
        std_soil_type = normalize_soil_type(soil_test.get("Soil_Type"))

        # 2. Validate Data Existence
        if std_state not in self.main_data:
            return {"status": "error", "msg": f"State '{state}' not found in database."}
        
        state_data = self.main_data[std_state]
        if std_crop not in state_data:
            return {"status": "error", "msg": f"Crop '{crop}' not found for {state}."}
        
        crop_data = state_data[std_crop]

        # 3. Calculate Organic Credits
        org_name = organic_input.get("name") if organic_input else None
        org_qty = organic_input.get("qty", 0) if organic_input else 0
        credits = self.get_organic_credit(org_name, org_qty)

        # Prepare variables for STCR Equation (T, SN, SP, SK, ON, OP, OK)
        calc_vars = {
            "T": safe_float(soil_test.get("Target_Yield")),
            "SN": safe_float(soil_test.get("SN")),
            "SP": safe_float(soil_test.get("SP")),
            "SK": safe_float(soil_test.get("SK")),
            "ON": credits["N"],
            "OP": credits["P2O5"],
            "OK": credits["K2O"]
        }

        final_npk = {"N": 0, "P2O5": 0, "K2O": 0}
        method_used = "None"

        # ==========================================================
        # STRATEGY A: STCR (Soil Test Crop Response) - PREFERRED
        # ==========================================================
        stcr_found = False
        if crop_data.get("stcr_available") and calc_vars["T"] > 0:
            stcr_list = crop_data.get("stcr", [])
            for entry in stcr_list:
                # Check if soil type matches (normalization is key here)
                json_soil = normalize_soil_type(entry.get("Soil_Type"))
                
                # We allow partial match (e.g. 'vertisol' matches 'black_soil' logic if mapped)
                if json_soil == std_soil_type or (std_soil_type == 'black_soil' and json_soil == 'vertisol'):
                    eqs = entry.get("equations", {})
                    final_npk["N"] = solve_equation(eqs.get("N"), calc_vars)
                    final_npk["P2O5"] = solve_equation(eqs.get("P2O5"), calc_vars)
                    final_npk["K2O"] = solve_equation(eqs.get("K2O"), calc_vars)
                    method_used = "STCR (Target Yield Equation)"
                    stcr_found = True
                    break
        
        # ==========================================================
        # STRATEGY B: RDF (Recommended Dose of Fertilizer) - FALLBACK
        # ==========================================================
        if not stcr_found:
            npk_list = crop_data.get("npk", [])
            selected_rdf = None

            # Filter logic 1: Exact Season + Exact Soil
            for row in npk_list:
                row_season = standardize_key(row.get("season"))
                row_soil = normalize_soil_type(row.get("soil_type"))
                
                if (row_season == std_season or row_season == "any") and row_soil == std_soil_type:
                    selected_rdf = row
                    break
            
            # Filter logic 2: Exact Season (Ignore Soil mismatch)
            if not selected_rdf:
                for row in npk_list:
                    row_season = standardize_key(row.get("season"))
                    if row_season == std_season:
                        selected_rdf = row
                        break
            
            # Filter logic 3: First available entry
            if not selected_rdf and npk_list:
                selected_rdf = npk_list[0]

            if selected_rdf:
                # Calculate Net Requirement (RDF - Organic Credit)
                final_npk["N"] = max(0, safe_float(selected_rdf.get("N_kg_ha")) - credits["N"])
                final_npk["P2O5"] = max(0, safe_float(selected_rdf.get("P2O5_kg_ha")) - credits["P2O5"])
                final_npk["K2O"] = max(0, safe_float(selected_rdf.get("K2O_kg_ha")) - credits["K2O"])
                method_used = f"Standard RDF ({selected_rdf.get('season')} season)"
            else:
                return {"status": "error", "msg": "No data available for this crop scenario."}

        # 4. Calculate Micronutrients
        micros = self.check_micronutrients(soil_test)

        # 5. Fertilizer Bags Calculation (Commercial conversion)
        # Simple Logic: DAP covers P first, Balance N by Urea, K by MOP
        req_p = final_npk["P2O5"]
        req_n = final_npk["N"]
        req_k = final_npk["K2O"]

        dap_qty = req_p / 0.46
        n_supplied_by_dap = dap_qty * 0.18
        remaining_n = max(0, req_n - n_supplied_by_dap)
        urea_qty = remaining_n / 0.46
        mop_qty = req_k / 0.60

        return {
            "status": "success",
            "meta": {
                "state": state,
                "crop": crop,
                "soil_type": std_soil_type,
                "method": method_used
            },
            "nutrients_needed_kg_ha": {
                "N": round(final_npk["N"], 2),
                "P": round(final_npk["P2O5"], 2),
                "K": round(final_npk["K2O"], 2)
            },
            "fertilizer_bags_approx": {
                "Urea": f"{round(urea_qty, 1)} kg",
                "DAP": f"{round(dap_qty, 1)} kg",
                "MOP": f"{round(mop_qty, 1)} kg"
            },
            "organic_credit_applied": {
                "N": round(credits["N"], 2),
                "P": round(credits["P2O5"], 2),
                "K": round(credits["K2O"], 2)
            },
            "micronutrient_alerts": micros
        }

# =============================================================================
# 5. EXECUTION EXAMPLE
# =============================================================================

if __name__ == "__main__":
    # Initialize Engine
    engine = SmartFarmerEngine()

    # TEST CASE 1: Andhra Pradesh -> Groundnut (Has STCR)
    print("\n--- TEST 1: Andhra Pradesh / Groundnut (STCR) ---")
    result1 = engine.recommend(
        state="Andhra Pradesh",
        crop="Groundnut",
        season="Rabi",
        soil_test={
            "Soil_Type": "Red Soil",
            "Target_Yield": 25,  # q/ha
            "SN": 180, "SP": 20, "SK": 150, # NPK in soil
            "Zn": 0.4, "Fe": 6.0, "S": 8.0, "B": 0.4 # Micronutrients
        },
        organic_input={"name": "Farm Yard Manure (FYM)", "qty": 5000} # 5 tons
    )
    print(json.dumps(result1, indent=2))

    # TEST CASE 2: Punjab -> Rice (Has NPK fallback only in some contexts)
    print("\n--- TEST 2: Punjab / Rice (RDF Fallback) ---")
    result2 = engine.recommend(
        state="Punjab",
        crop="Rice",
        season="Kharif",
        soil_test={
            "Soil_Type": "Alluvial",
            "Target_Yield": 0, # No target yield triggers RDF
            "SN": 150, "SP": 15, "SK": 100,
            "Zn": 1.2, "Fe": 5.0, "S": 12.0, "B": 1.0
        }
    )
    print(json.dumps(result2, indent=2))