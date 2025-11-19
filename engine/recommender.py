from typing import Dict, Optional, Any, List
from .thresholds import SoilThresholdEngine
from .npk_standard import StandardNPKEngine
from .stcr import STCREngine
from .organic_rules import OrganicAndSpecialRulesEngine
from .brand_converter import FertilizerBrandConverter


class FertilizerRecommender:
    """
    Main orchestrator that executes:
    1. Soil evaluation (macro + micro)
    2. STCR or Standard selection
    3. Organic credits
    4. Special rules (pH, EC, rotation, micros)
    5. Conversion to commercial fertilizers (Urea/DAP/MOP)
    """

    def __init__(self):
        self.soil_engine = SoilThresholdEngine()
        self.std_engine = StandardNPKEngine()
        self.stcr_engine = STCREngine()
        self.org_engine = OrganicAndSpecialRulesEngine()
        self.converter = FertilizerBrandConverter()

    # -----------------------------------------------------------------------
    # MAIN API
    # -----------------------------------------------------------------------
    def recommend(
        self,
        soil: Dict[str, float],
        crop: str,
        condition: str = "Irrigated",
        target_yield: Optional[float] = None,
        organic_inputs: Optional[Dict[str, float]] = None,
        meta: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:

        meta = meta or {}
        organic_inputs = organic_inputs or {}

        response = {
            "status": "success",
            "method_used": "",
            "alerts": [],
            "soil_status": {},
            "breakdown": {}
        }

        # ----------------------------------------------------------------
        # 1. SOIL STATUS (macro + micro)
        # ----------------------------------------------------------------
        macro_status = self.soil_engine.evaluate_macro(soil)
        micro_def = self.soil_engine.evaluate_micro(soil)

        response["soil_status"] = macro_status

        if micro_def:
            response["alerts"].append(
                f"Micronutrient Deficiency: {', '.join(micro_def)}. "
                f"Apply recommended micro mix (e.g., ZnSO4 for Zinc)."
            )

        # ----------------------------------------------------------------
        # 2. BASE NPK: STCR or STANDARD
        # ----------------------------------------------------------------
        base_npk = None

        # ---- STCR path ----
        if target_yield and target_yield > 0:
            key = meta.get("stcr_equation_key")
            if key:
                stcr_out = self.stcr_engine.calculate(
                    crop_key=key,
                    T=target_yield,
                    SN=soil.get("N", 0),
                    SP=soil.get("P", 0),
                    SK=soil.get("K", 0)
                )
                if stcr_out:
                    base_npk = {
                        "N": stcr_out["N"],
                        "P2O5": stcr_out["P2O5"],
                        "K2O": stcr_out["K2O"]
                    }
                    response["method_used"] = f"STCR (Target Yield: {target_yield} {stcr_out.get('Unit')})"
                    response["breakdown"]["stcr_meta"] = stcr_out

        # ---- STANDARD path (fallback) ----
        if not base_npk:
            std = self.std_engine.get_npk(crop, condition)
            if not std:
                return {
                    "status": "error",
                    "message": f"No recommendation found for crop '{crop}' under '{condition}' condition."
                }

            base_npk = {
                "N": std["N"],
                "P2O5": std["P2O5"],
                "K2O": std["K2O"]
            }

            response["method_used"] = "Standard Recommendation"

            if std.get("Note"):
                response["alerts"].append(f"Agronomic Note: {std['Note']}")

        response["breakdown"]["base_requirement_kg_ha"] = base_npk.copy()

        # ----------------------------------------------------------------
        # 3. ORGANIC CREDITS
        # ----------------------------------------------------------------
        after_org, credits = self.org_engine.apply_organic_credits(base_npk, organic_inputs)
        response["breakdown"]["organic_credits"] = credits
        response["breakdown"]["after_organic"] = after_org

        # ----------------------------------------------------------------
        # 4. SPECIAL RULES (pH, EC, rotation, micros)
        # ----------------------------------------------------------------
        final_npk, rule_alerts = self.org_engine.apply_special_rules(after_org, soil, meta)
        response["alerts"].extend(rule_alerts)
        response["breakdown"]["final_elemental_req"] = final_npk.copy()

        # ----------------------------------------------------------------
        # 5. CONVERSION TO COMMERCIAL FERTILIZERS
        # ----------------------------------------------------------------
        fert = self.converter.convert(
            N_req=final_npk["N"],
            P_req=final_npk["P2O5"],
            K_req=final_npk["K2O"]
        )

        response["commercial_fertilizer"] = fert

        return response
