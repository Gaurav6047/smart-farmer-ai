import pandas as pd
import json
import os
import re

class FertilizerEngine:
    def __init__(self):
        # Paths relative to the main.py execution
        self.base_path = "models"
        self.rdf_df = self.load_csv("standard_npk.csv")
        self.stcr_data = self.load_json("stcr_equations.json")
        self.fertility_data = self.load_json("soil_fertility.json")
        self.rules_data = self.load_json("organic_rules.json")

    def load_csv(self, filename):
        try:
            return pd.read_csv(os.path.join(self.base_path, filename))
        except:
            return pd.DataFrame()

    def load_json(self, filename):
        try:
            with open(os.path.join(self.base_path, filename), 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {}

    # --- HELPER: Determine Low/Medium/High ---
    def get_soil_status(self, nutrient, value):
        """Determines soil status based on soil_fertility.json"""
        try:
            # Mapping nutrient names to json keys
            key_map = {'N': 'nitrogen', 'P': 'phosphorus_alkaline', 'K': 'potassium', 'OC': 'organic_carbon'}
            key = key_map.get(nutrient)
            
            if not key: return "Medium"

            thresholds = self.fertility_data['soil_fertility_thresholds']['macronutrients'].get(key, {}).get('thresholds')
            if nutrient == 'OC':
                thresholds = self.fertility_data['soil_fertility_thresholds']['organic_carbon']['thresholds']

            if not thresholds: return "Medium"

            # Logic
            low_max = thresholds['low'].get('max', 0)
            high_min = thresholds['high'].get('min', 9999)

            if value < low_max: return "Low"
            elif value > high_min: return "High"
            else: return "Medium"
        except:
            return "Medium"

    # --- MODE 1: STCR (Targeted Yield) ---
    def calculate_stcr(self, equation_key, target_yield, sn, sp, sk):
        eq_data = self.stcr_data.get('stcr_equations', {}).get('crops', {}).get(equation_key, {})
        
        if not eq_data:
            return None, "Equation not found for selected region."

        equations = eq_data.get('equations', {})
        
        # Secure Equation Solver
        def solve(eq_str, T, SN, SP, SK):
            if not eq_str: return 0
            # Replace variables
            safe_str = eq_str.replace('T', str(T)).replace('SN', str(SN)).replace('SP', str(SP)).replace('SK', str(SK))
            # Remove anything that isn't a number or operator for security
            if not re.match(r'^[\d\.\+\-\*\/\s\(\)]+$', safe_str):
                return 0
            try:
                val = eval(safe_str)
                return max(0, val) # Negative dose not possible
            except:
                return 0

        n_rec = solve(equations.get('N', '0'), target_yield, sn, sp, sk)
        p_rec = solve(equations.get('P2O5', '0'), target_yield, sn, sp, sk)
        k_rec = solve(equations.get('K2O', '0'), target_yield, sn, sp, sk)

        return {
            "N": round(n_rec, 2),
            "P": round(p_rec, 2),
            "K": round(k_rec, 2),
            "Source": f"STCR Equation ({eq_data.get('region', 'Unknown')})",
            "Unit": eq_data.get('unit', 'q/ha')
        }, None

    # --- MODE 2: RDF (General Recommendation) ---
    def calculate_rdf(self, crop_name, sn, sp, sk):
        if self.rdf_df.empty:
            return None, "Standard NPK Data missing."
            
        row = self.rdf_df[self.rdf_df['Crop'] == crop_name]
        if row.empty:
            return None, "Selected crop not found in database."
        
        row = row.iloc[0]
        base_n, base_p, base_k = row['N_kg_ha'], row['P_kg_ha'], row['K_kg_ha']

        # Determine Status
        n_status = self.get_soil_status('N', sn)
        p_status = self.get_soil_status('P', sp)
        k_status = self.get_soil_status('K', sk)

        # Adjustment Logic (Low = +25%, High = -25%)
        def adjust(val, status):
            if status == "Low": return val * 1.25
            elif status == "High": return val * 0.75
            return val

        return {
            "N": round(adjust(base_n, n_status), 2),
            "P": round(adjust(base_p, p_status), 2),
            "K": round(adjust(base_k, k_status), 2),
            "Source": "General RDF (Soil Adjusted)",
            "Status": f"N:{n_status}, P:{p_status}, K:{k_status}"
        }, None

    # --- CHECK SPECIAL RULES (pH, Micro) ---
    def check_rules(self, ph, ec, micro_values):
        alerts = []
        rules = self.rules_data.get('special_rules', {})

        # pH Logic
        ph_rules = rules.get('pH_rules', {})
        if ph < 5.5:
            alerts.append(("🔴 Acidic Soil Alert", ph_rules.get('acidic_critical', {}).get('recommendation', 'Apply Lime')))
        elif ph > 8.5:
            alerts.append(("🔴 Alkaline Soil Alert", ph_rules.get('alkaline_critical', {}).get('recommendation', 'Apply Gypsum')))

        # EC Logic
        if ec > 2.0:
            alerts.append(("⚠️ High Salinity", "Reduce yield target, improve drainage."))

        # Micronutrient Logic
        micro_rules = rules.get('micronutrient_rules', {})
        for nutrient, val in micro_values.items():
            key = nutrient.lower()
            if key in micro_rules:
                trigger_str = micro_rules[key].get('trigger', '0').split('<')[-1].replace('ppm','').strip()
                try:
                    limit = float(trigger_str)
                    if val < limit:
                        prod = micro_rules[key].get('product', 'Fertilizer')
                        dose = micro_rules[key].get('dose_soil', 'Check generic dose')
                        alerts.append((f"🟠 Low {nutrient}", f"Apply {prod} @ {dose}"))
                except:
                    pass
        
        return alerts