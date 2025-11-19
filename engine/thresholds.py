from typing import Dict, List, Any
from .loader import load_soil_fertility


class SoilThresholdEngine:
    """
    Evaluates soil fertility levels:
    - Macronutrients (N, P, K)
    - Micronutrient critical limits (Zn, Fe, Cu, Mn, B, S)
    """

    def __init__(self):
        self.raw = load_soil_fertility()

        # JSON is stored under soil_fertility_thresholds
        self.data = self.raw.get("soil_fertility_thresholds", {})

        # Extract macro + micro sections
        self.macro = self.data.get("macronutrients", {})
        self.micro = self.data.get("micronutrients", {})

    # ---------------------------------------------------------
    #  MACRO NPK EVALUATION
    # ---------------------------------------------------------
    def evaluate_macro(self, soil: Dict[str, float]) -> Dict[str, str]:
        """
        Evaluate N, P, K as Low/Medium/High using JSON thresholds.
        Falls back to Indian defaults if thresholds missing.
        """
        status = {}

        # Fallback defaults (in case JSON missing)
        defaults = {
            "N": {"low": 280, "high": 560},
            "P": {"low": 11, "high": 22},
            "K": {"low": 118, "high": 280}
        }

        # ---- Nitrogen ----
        n_val = soil.get("N", 0)
        n_thr = self._extract_threshold(self.macro.get("nitrogen", {}), defaults["N"])
        status["N"] = self._evaluate_value(n_val, n_thr)

        # ---- Phosphorus: depends on pH ----
        p_val = soil.get("P", 0)
        pH = soil.get("pH", None)

        if pH is not None:
            if pH > 6.5:
                p_data = self.macro.get("phosphorus_alkaline", {})
            else:
                p_data = self.macro.get("phosphorus_acidic", {})
        else:
            p_data = self.macro.get("phosphorus_alkaline", {})

        p_thr = self._extract_threshold(p_data, defaults["P"])
        status["P"] = self._evaluate_value(p_val, p_thr)

        # ---- Potassium ----
        k_val = soil.get("K", 0)
        k_data = self.macro.get("potassium", {})
        k_thr = self._extract_threshold(k_data, defaults["K"])
        status["K"] = self._evaluate_value(k_val, k_thr)

        return status

    # ---------------------------------------------------------
    #  MICRO NUTRIENT EVALUATION
    # ---------------------------------------------------------
    def evaluate_micro(self, soil: Dict[str, float]) -> List[str]:
        """
        Returns list of micronutrients that are below critical limits.
        Uses JSON critical_limit values.
        """
        deficiencies = []

        for nutrient, info in self.micro.items():
            if not isinstance(info, dict):
                continue

            crit = info.get("critical_limit", None)
            if crit is None:
                continue

            val = soil.get(nutrient.capitalize()) or soil.get(nutrient.upper()) or soil.get(nutrient)

            if val is None:
                continue

            if val < crit:
                deficiencies.append(nutrient.upper())

        return deficiencies

    # ---------------------------------------------------------
    #  INTERNAL HELPERS
    # ---------------------------------------------------------
    @staticmethod
    def _extract_threshold(node: Dict[str, Any], fallback: Dict[str, float]) -> Dict[str, float]:
        """
        Converts JSON threshold format:
        { "low": {"max": 280}, "medium": {...}, "high": {...} }
        into a simple dict:
        { "low": 280, "high": 560 }
        """
        low = node.get("thresholds", {}).get("low", {}).get("max", fallback["low"])
        high = node.get("thresholds", {}).get("high", {}).get("min", fallback["high"])
        return {"low": low, "high": high}

    @staticmethod
    def _evaluate_value(val: float, thr: Dict[str, float]) -> str:
        """
        Classifies a value as Low/Medium/High.
        """
        if val < thr["low"]:
            return "Low"
        elif val > thr["high"]:
            return "High"
        else:
            return "Medium"
