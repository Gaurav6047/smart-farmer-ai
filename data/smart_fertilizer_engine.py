import json
import os
import ast
import logging
import math

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SmartFertilizerEngine:
    # --- TEXT TEMPLATES FOR MULTI-LANGUAGE COMPATIBILITY ---
    # Hum yahan keys define kar rahe hain taaki language.py inhe pakad sake
    MSG_ACIDIC = "Acidic Soil Detected (pH {ph}): Apply Lime."
    MSG_ALKALINE = "Alkaline Soil Detected (pH {ph}): Apply Gypsum."
    MSG_SALINITY = "High Salinity (EC {ec} dS/m): Expect {red}% yield reduction."
    MSG_LEGUME = "Legume Rotation Credit: Reduced Nitrogen dose by {n} kg/ha."
    MSG_LEGUME_ZERO = "Legume credit note: Nitrogen dose is already zero."
    MSG_DRIP = "Drip Fertigation: Nutrient dose reduced to {eff}% due to high efficiency."
    MSG_DRIP_SCH = "Fertigation Schedule: Apply in {splits}."
    MSG_SANDY = "Sandy Soil: Apply Nitrogen in {split} to prevent leaching."
    MSG_MICRO = "Micronutrient Deficiency ({nut}): Apply {nut} sulfate/chelate."
    MSG_ZERO_FERT = "No chemical fertilizer required (Organic inputs & Soil fertility are sufficient)."

    def __init__(self):
        self.data_master = {}
        self.data_organic = {}
        self.data_thresholds = {}
        self.data_stcr_fallback = {}
        
        # --- PATH FIX: Get directory of THIS script ---
        base_dir = os.path.dirname(os.path.abspath(__file__))

        # File paths (Absolute paths)
        self.files = {
            "master": os.path.join(base_dir, "final_hard_normalized.json"),
            "organic": os.path.join(base_dir, "organic_rules.json"),
            "thresholds": os.path.join(base_dir, "soil_fertility_thresholds.json"),
            "stcr_fallback": os.path.join(base_dir, "stcr_equation_constants.json")
        }

    def load_all_datasets(self):
        """Loads all 4 JSON files."""
        try:
            with open(self.files["master"], 'r') as f: self.data_master = json.load(f)
            
            with open(self.files["organic"], 'r') as f: 
                self.data_organic = json.load(f)
                if "organic_inputs" not in self.data_organic: raise ValueError("Schema Error: organic_rules")

            with open(self.files["thresholds"], 'r') as f:
                self.data_thresholds = json.load(f)
                if "soil_fertility_thresholds" not in self.data_thresholds: raise ValueError("Schema Error: thresholds")

            stcr_file = self.files["stcr_fallback"]
            if os.path.exists(stcr_file):
                with open(stcr_file, 'r') as f: self.data_stcr_fallback = json.load(f)
            else:
                logger.warning(f"STCR fallback file {stcr_file} not found.")

            logger.info("All datasets loaded successfully.")
        except Exception as e:
            logger.error(f"Dataset Loading Error: {str(e)}")
            raise

    def get_available_states(self, mode):
        if not self.data_master: return []
        available_states = []
        for state, crops in self.data_master.items():
            if state == "regions": continue 
            has_mode = False
            for crop_data in crops.values():
                if mode == "npk" and crop_data.get("npk_available"): has_mode = True; break
                elif mode == "stcr" and crop_data.get("stcr_available"): has_mode = True; break
            if has_mode: available_states.append(state)
        return sorted(available_states)

    def get_available_crops(self, state, mode):
        if state not in self.data_master: return []
        available_crops = []
        crops = self.data_master[state]
        for crop_name, details in crops.items():
            if mode == "npk" and details.get("npk_available"): available_crops.append(crop_name)
            elif mode == "stcr" and details.get("stcr_available"): available_crops.append(crop_name)
        return sorted(available_crops)

    def get_valid_seasons_and_soils(self, state, crop, mode):
        results = {"seasons": set(), "soils": set()}
        try:
            crop_data = self.data_master.get(state, {}).get(crop, {})
            if mode == "npk":
                for entry in crop_data.get("npk", []):
                    if "season" in entry: results["seasons"].add(entry["season"])
                    if "soil_type" in entry: results["soils"].add(entry["soil_type"])
            elif mode == "stcr":
                for entry in crop_data.get("stcr", []):
                    if "Soil_Type" in entry: results["soils"].add(entry["Soil_Type"])
                results["seasons"].add("Any") 
        except Exception: return {"seasons": [], "soils": []}
        return {"seasons": sorted(list(results["seasons"])), "soils": sorted(list(results["soils"]))}

    def classify_soil_fertility(self, soil_test_input, thresholds=None):
        if thresholds is None: thresholds = self.data_thresholds.get("soil_fertility_thresholds", {})
        report = {}
        
        # Standardized Status Keys (Compatible with language.py)
        def get_status(value, rules):
            if value <= rules["low"]["max"]: return "Low"
            if "high" in rules and value >= rules["high"]["min"]: return "High"
            return "Medium"

        if "OC" in soil_test_input:
            oc_rules = thresholds.get("organic_carbon", {}).get("thresholds", {})
            if oc_rules: report["OC_Status"] = get_status(soil_test_input["OC"], oc_rules)

        macro_rules = thresholds.get("macronutrients", {})
        if "SN" in soil_test_input:
            report["N_Status"] = get_status(soil_test_input["SN"], macro_rules.get("nitrogen", {}).get("thresholds", {}))
        
        if "SP" in soil_test_input:
            ph = soil_test_input.get("pH", 7.0)
            p_key = "phosphorus_alkaline" if ph > 6.5 else "phosphorus_acidic"
            report["P_Status"] = get_status(soil_test_input["SP"], macro_rules.get(p_key, {}).get("thresholds", {}))

        if "SK" in soil_test_input:
            report["K_Status"] = get_status(soil_test_input["SK"], macro_rules.get("potassium", {}).get("thresholds", {}))

        micro_rules = thresholds.get("micronutrients", {})
        micro_map = {"Zn": "zinc", "Fe": "iron", "Mn": "manganese", "Cu": "copper", "B": "boron", "S": "sulphur"}
        deficiency_report = {}
        
        for input_key, rule_key in micro_map.items():
            if input_key in soil_test_input:
                val = soil_test_input[input_key]
                crit = micro_rules.get(rule_key, {}).get("critical_limit", 0)
                # Standardized Deficiency Keys
                deficiency_report[input_key] = "Deficient" if val < crit else "Sufficient"
        
        return report, deficiency_report

    def apply_organic_credit(self, fertilizer_dict, organic_inputs, applied_organics):
        credit = {"N": 0.0, "P2O5": 0.0, "K2O": 0.0}
        sources = organic_inputs.get("manure", []) + organic_inputs.get("oilseed_cakes", [])
        
        for org_name, applied_kg in applied_organics.items():
            if applied_kg <= 0: continue
            source_data = next((item for item in sources if item["name"] == org_name), None)
            if source_data:
                credit["N"] += (applied_kg * source_data.get("N_percent", 0)) / 100
                credit["P2O5"] += (applied_kg * source_data.get("P2O5_percent", 0)) / 100
                credit["K2O"] += (applied_kg * source_data.get("K2O_percent", 0)) / 100

        final_dict = fertilizer_dict.copy()
        final_dict["N"] = max(0, final_dict.get("N", 0) - credit["N"])
        final_dict["P2O5"] = max(0, final_dict.get("P2O5", 0) - credit["P2O5"])
        final_dict["K2O"] = max(0, final_dict.get("K2O", 0) - credit["K2O"])
        return final_dict, credit

    def compute_npk_recommendation(self, state, crop, season, soil_type):
        try:
            entries = self.data_master.get(state, {}).get(crop, {}).get("npk", [])
            for row in entries:
                row_season = row.get("season", "").lower()
                row_soil = row.get("soil_type", "").lower()
                match_season = (season.lower() == row_season) or (row_season == "any")
                match_soil = (soil_type.lower() == row_soil) or (row_soil == "any") or (not soil_type)
                if match_season and match_soil:
                    return {"N": float(row.get("N_kg_ha", 0)), "P2O5": float(row.get("P2O5_kg_ha", 0)), "K2O": float(row.get("K2O_kg_ha", 0))}
            
            if entries:
                row = entries[0]
                return {"N": float(row.get("N_kg_ha", 0)), "P2O5": float(row.get("P2O5_kg_ha", 0)), "K2O": float(row.get("K2O_kg_ha", 0))}
            return {"N": 0.0, "P2O5": 0.0, "K2O": 0.0}
        except Exception: return {"N": 0.0, "P2O5": 0.0, "K2O": 0.0}

    def compute_stcr_recommendation(self, state, crop, soil_type, target_yield, soil_test_values, organic_nutrients):
        try:
            entries = self.data_master.get(state, {}).get(crop, {}).get("stcr", [])
            selected_eq = None
            for row in entries:
                if row.get("Soil_Type", "").lower() == soil_type.lower():
                    selected_eq = row.get("equations", {}); break
            
            if not selected_eq and entries: selected_eq = entries[0].get("equations", {})
            if not selected_eq: return {"N": 0, "P2O5": 0, "K2O": 0}, False

            context = {
                "T": float(target_yield), "SN": float(soil_test_values.get("SN", 0)),
                "SP": float(soil_test_values.get("SP", 0)), "SK": float(soil_test_values.get("SK", 0)),
                "ON": float(organic_nutrients.get("N", 0)), "OP": float(organic_nutrients.get("P2O5", 0)), "OK": float(organic_nutrients.get("K2O", 0))
            }
            result = {}
            organic_terms_used = {"N": False, "P2O5": False, "K2O": False}

            for nutrient in ["N", "P2O5", "K2O"]:
                eq_str = selected_eq.get(nutrient, "0")
                if not eq_str: result[nutrient] = 0.0; continue
                
                if nutrient == "N" and "ON" in eq_str: organic_terms_used["N"] = True
                if nutrient == "P2O5" and "OP" in eq_str: organic_terms_used["P2O5"] = True
                if nutrient == "K2O" and "OK" in eq_str: organic_terms_used["K2O"] = True

                safe_expr = eq_str.replace(" ", "")
                if not set(safe_expr).issubset(set("0123456789.+-*/()TSNPOK")): result[nutrient] = 0.0; continue
                try: result[nutrient] = max(0.0, eval(safe_expr, {"__builtins__": None}, context))
                except Exception: result[nutrient] = 0.0
            return result, organic_terms_used
        except Exception: return {"N": 0.0, "P2O5": 0.0, "K2O": 0.0}, False

    def calculate_fertilizer_bags(self, final_dose):
        n_req = final_dose.get("N", 0); p_req = final_dose.get("P2O5", 0); k_req = final_dose.get("K2O", 0)
        dap_kg = p_req / 0.46 if p_req > 0 else 0
        n_from_dap = dap_kg * 0.18
        urea_kg = max(0, n_req - n_from_dap) / 0.46
        mop_kg = k_req / 0.60 if k_req > 0 else 0
        
        def kg_to_bags(val): return math.ceil((val / 50.0) * 100) / 100 if val > 0 else 0.0
        return {"Urea_bags": kg_to_bags(urea_kg), "DAP_bags": kg_to_bags(dap_kg), "MOP_bags": kg_to_bags(mop_kg)}

    def apply_special_rules(self, fertilizer_dict, special_rules, soil_data, irrigation_type, previous_crop):
        advisories = []
        final_dict = fertilizer_dict.copy()
        adjustments_log = {}

        # 1. pH Correction (Using Templates)
        ph = soil_data.get("pH", 7.0)
        if ph < 5.5: advisories.append(self.MSG_ACIDIC.format(ph=ph))
        if ph >= 8.5: advisories.append(self.MSG_ALKALINE.format(ph=ph))

        # 2. EC Salinity (Using Templates)
        ec = soil_data.get("EC", 0.0)
        if ec > 2.0:
            yield_adj = special_rules.get("EC", {}).get("saline", {}).get("yield_adjustment", 0) 
            advisories.append(self.MSG_SALINITY.format(ec=ec, red=abs(yield_adj)*100))
            adjustments_log["EC_yield_reduction"] = yield_adj

        # 3. Legume Rotation (Using Templates)
        if previous_crop and previous_crop.lower() in ["legume", "pulse", "soybean", "groundnut", "chickpea", "lentil"]:
            n_credit = special_rules.get("rotation", {}).get("legume_credit", {}).get("N_minus", 0)
            if final_dict["N"] > n_credit:
                final_dict["N"] = max(0, final_dict["N"] - n_credit)
                advisories.append(self.MSG_LEGUME.format(n=n_credit))
                adjustments_log["legume_N_credit"] = n_credit
            else:
                advisories.append(self.MSG_LEGUME_ZERO)

        # 4. Fertigation (Using Templates)
        if irrigation_type and irrigation_type.lower() == "drip":
            fert_rules = special_rules.get("fertigation", {}).get("drip", {})
            reduce_factor = fert_rules.get("reduce_factor", 1.0)
            final_dict["N"] *= reduce_factor; final_dict["P2O5"] *= reduce_factor; final_dict["K2O"] *= reduce_factor
            
            advisories.append(self.MSG_DRIP.format(eff=reduce_factor*100))
            if "split_doses" in fert_rules:
                advisories.append(self.MSG_DRIP_SCH.format(splits=fert_rules["split_doses"]))
            adjustments_log["fertigation_factor"] = reduce_factor

        # 5. Sandy Soil (Using Templates)
        if "sandy" in str(soil_data.get("soil_type_input", "")).lower():
            sandy_rule = special_rules.get("soil_type_rules", {}).get("sandy", {})
            if "N_split" in sandy_rule:
                advisories.append(self.MSG_SANDY.format(split=sandy_rule["N_split"]))

        return final_dict, advisories, adjustments_log

    def generate_final_recommendation(self, input_payload):
        state = input_payload.get("state", "").lower().replace(" ", "_")
        crop = input_payload.get("crop", "").lower()
        mode = input_payload.get("mode", "npk")
        soil_test = input_payload.get("soil_test", {})
        soil_test["soil_type_input"] = input_payload.get("soil_type", "alluvial")
        target_yield = input_payload.get("target_yield", 0)

        response = {
            "mode": mode, "state": state, "crop": crop, "soil_type": soil_test["soil_type_input"],
            "advisory": [], "special_adjustments": {}, "calculation_trace": {}
        }

        # Classification
        fertility_status, deficiencies = self.classify_soil_fertility(soil_test)
        response["soil_fertility_status"] = fertility_status
        response["deficiency_report"] = deficiencies
        
        # Micro Advisories (Using Templates)
        micro_rules = self.data_organic.get("special_rules", {}).get("micronutrients", {})
        for nut, status in deficiencies.items():
            if status == "Deficient" and nut in micro_rules:
                response["advisory"].append(self.MSG_MICRO.format(nut=nut))

        # Organic Credit
        dummy_base = {"N": 0, "P2O5": 0, "K2O": 0}
        _, organic_credits = self.apply_organic_credit(dummy_base, self.data_organic.get("organic_inputs", {}), input_payload.get("organic_applied", {}))
        response["organic_credit_applied"] = {k: round(v, 2) for k, v in organic_credits.items()}

        # Base Calc
        base_rec = {"N": 0, "P2O5": 0, "K2O": 0}
        if mode == "stcr":
            ec_val = soil_test.get("EC", 0)
            if ec_val > 2.0:
                 yield_adj = self.data_organic.get("special_rules", {}).get("EC", {}).get("saline", {}).get("yield_adjustment", 0)
                 target_yield = target_yield * (1 + yield_adj)
            stcr_res, org_terms_used = self.compute_stcr_recommendation(state, crop, soil_test["soil_type_input"], target_yield, soil_test, organic_credits)
            base_rec = stcr_res
            final_dose = base_rec.copy()
            for nut in ["N", "P2O5", "K2O"]:
                if not org_terms_used.get(nut, False): final_dose[nut] = max(0, final_dose[nut] - organic_credits[nut])
            current_dose = final_dose
        else:
            base_rec = self.compute_npk_recommendation(state, crop, input_payload.get("season", "kharif"), soil_test["soil_type_input"])
            current_dose, _ = self.apply_organic_credit(base_rec, self.data_organic.get("organic_inputs", {}), input_payload.get("organic_applied", {}))

        response["base_recommendation"] = {k: round(v, 2) for k, v in base_rec.items()}
        
        # Special Rules
        final_dose_after_special, special_advisories, adj_log = self.apply_special_rules(
            current_dose, self.data_organic.get("special_rules", {}), soil_test, 
            input_payload.get("irrigation_type", "Flood"), input_payload.get("previous_crop", "")
        )
        response["advisory"].extend(special_advisories)
        response["special_adjustments"].update(adj_log)
        
        # Rounding
        final_dose_rounded = {k: round(v, 2) for k, v in final_dose_after_special.items()}
        response["final_fertilizer_dose"] = final_dose_rounded

        # Zero Advisory (Using Template)
        if all(v == 0 for v in final_dose_rounded.values()):
            response["advisory"].append(self.MSG_ZERO_FERT)

        response["fertilizer_bags"] = self.calculate_fertilizer_bags(final_dose_rounded)
        return response