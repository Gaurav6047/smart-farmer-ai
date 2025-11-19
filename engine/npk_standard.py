import pandas as pd
from typing import Optional, Dict, Any
from .loader import load_standard_npk


class StandardNPKEngine:
    """
    Fetches standard fertilizer recommendations from CSV using:
    - Fuzzy crop matching
    - Condition/Variety matching
    """

    def __init__(self):
        self.df: pd.DataFrame = load_standard_npk()

        # Ensure columns exist to prevent runtime errors
        if not self.df.empty:
            required = {"Crop", "Condition_Variety", "N_kg_ha", "P_kg_ha", "K_kg_ha"}
            missing = required - set(self.df.columns)
            if missing:
                print(f"[WARN] Missing columns in standard_npk.csv: {missing}")

    # --------------------------------------------------------------------
    #  MAIN METHOD
    # --------------------------------------------------------------------
    def get_npk(self, crop_name: str, condition: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """
        Returns N, P2O5, K2O for the selected crop & condition.

        If multiple rows match:
            - Condition filters first
            - First matching row is selected
        """
        if self.df.empty:
            return None

        crop_name = crop_name.strip().lower()

        # ---------------------------
        # Step 1: fuzzy crop matching
        # ---------------------------
        mask = self.df["Crop"].str.lower().str.contains(crop_name, na=False)
        results = self.df[mask]

        if results.empty:
            return None

        # ---------------------------
        # Step 2: condition matching
        # ---------------------------
        if condition:
            cond = condition.lower().strip()
            cond_mask = results["Condition_Variety"].str.lower().str.contains(cond, na=False)
            filtered = results[cond_mask]

            if not filtered.empty:
                results = filtered

        # ---------------------------
        # Step 3: pick first best row
        # ---------------------------
        row = results.iloc[0]

        return {
            "N": float(row.get("N_kg_ha", 0)),
            "P2O5": float(row.get("P_kg_ha", 0)),
            "K2O": float(row.get("K_kg_ha", 0)),
            "Note": row.get("Agronomic_Notes", "")
        }
