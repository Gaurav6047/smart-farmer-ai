import math
from typing import Dict


class FertilizerBrandConverter:
    """
    Converts elemental N-P2O5-K2O requirement (kg/ha) into
    commercial fertilizers: Urea, DAP, MOP.
    """

    # Bag weights (India standard)
    BAG_WT_UREA = 45
    BAG_WT_DAP = 50
    BAG_WT_MOP = 50

    # Nutrient composition
    N_UREA = 0.46           # 46% N
    N_DAP = 0.18            # 18% N
    P_DAP = 0.46            # 46% P2O5
    K_MOP = 0.60            # 60% K2O

    def convert(self, N_req: float, P_req: float, K_req: float) -> Dict[str, Dict[str, float]]:
        """
        Converts nutrient requirements to fertilizer bags + kg.
        """

        # -----------------------------
        # Step 1: P2O5 via DAP
        # -----------------------------
        if P_req > 0:
            dap_kg = P_req / self.P_DAP
            n_from_dap = dap_kg * self.N_DAP
        else:
            dap_kg = 0
            n_from_dap = 0

        # -----------------------------
        # Step 2: Remaining Nitrogen via Urea
        # -----------------------------
        n_remaining = N_req - n_from_dap

        if n_remaining > 0:
            urea_kg = n_remaining / self.N_UREA
        else:
            urea_kg = 0  # If DAP oversupplies N, do not apply Urea

        # -----------------------------
        # Step 3: K2O via MOP
        # -----------------------------
        if K_req > 0:
            mop_kg = K_req / self.K_MOP
        else:
            mop_kg = 0

        # -----------------------------
        # Output dict (kg + bags)
        # -----------------------------
        return {
            "kg": {
                "Urea": round(urea_kg, 2),
                "DAP": round(dap_kg, 2),
                "MOP": round(mop_kg, 2)
            },
            "bags": {
                "Urea": round(urea_kg / self.BAG_WT_UREA, 1),
                "DAP": round(dap_kg / self.BAG_WT_DAP, 1),
                "MOP": round(mop_kg / self.BAG_WT_MOP, 1)
            }
        }
