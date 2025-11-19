import math
from typing import Dict, Optional, Any
from .loader import load_stcr_equations


class STCREngine:
    """
    Soil Test Crop Response (Targeted Yield) Calculator.
    Reads equations from stcr_equations.json and computes:
        N, P2O5, K2O requirement based on T, SN, SP, SK
    """

    def __init__(self):
        self.raw = load_stcr_equations()
        self.crops = self.raw.get("stcr_equations", {}).get("crops", {})

    # -------------------------------------------------------
    # SAFE EVALUATOR (very strict, secure)
    # -------------------------------------------------------
    def _eval(self, equation: str, vars_map: Dict[str, float]) -> float:
        """
        Safely evaluates a mathematical STCR equation string.
        Allows only math ops + limited functions.
        """

        # Disallow any malicious patterns
        if any(bad in equation for bad in ["__", "import", "os.", "sys.", "lambda"]):
            return 0

        # Allowed math context
        safe_context = {
            "math": math,
            "abs": abs,
            "max": max,
            "min": min,
            **vars_map
        }

        try:
            return float(eval(equation, {"__builtins__": {}}, safe_context))
        except Exception as e:
            print(f"[STCR ERROR] Equation failed: '{equation}', reason: {e}")
            return 0.0

    # -------------------------------------------------------
    # MAIN METHOD
    # -------------------------------------------------------
    def calculate(
        self,
        crop_key: str,
        T: float,
        SN: float,
        SP: float,
        SK: float
    ) -> Optional[Dict[str, Any]]:
        """
        Compute STCR based fertilizer requirement for:
            - crop_key: e.g., "rice_alluvial"
            - T: Target yield (q/ha or t/ha)
            - SN, SP, SK: Soil test values
        """

        if crop_key not in self.crops:
            return None

        node = self.crops[crop_key]

        eq = node.get("equations", {})
        if not eq:
            return None

        vars_map = {
            "T": T,
            "SN": SN,
            "SP": SP,
            "SK": SK
        }

        # Evaluate safely
        N = self._eval(eq.get("N", "0"), vars_map)
        P = self._eval(eq.get("P2O5", "0"), vars_map)
        K = self._eval(eq.get("K2O", "0"), vars_map)

        # Negative values allowed? NO → soil test > crop demand
        N = max(0, round(N, 2))
        P = max(0, round(P, 2))
        K = max(0, round(K, 2))

        return {
            "N": N,
            "P2O5": P,
            "K2O": K,
            "Equation_Ref": node.get("ref", "N/A"),
            "Unit": node.get("unit", "q/ha"),
            "Region": node.get("region", "")
        }
