# ============================================================
# fertilizer_convert.py — Nutrient to Fertilizer Converter
# Logic: DAP (P) -> Urea (Balance N) -> MOP (K)
# ============================================================

def convert_to_fertilizers(final_npk):
    """
    Converts final N, P2O5, K2O requirements (kg/ha) into commercial fertilizers.
    This module must NOT import anything from final_router to avoid circular loops.
    """
    N_req = final_npk.get("N", 0)
    P_req = final_npk.get("P2O5", 0)
    K_req = final_npk.get("K2O", 0)

    # Standard Composition
    N_DAP = 0.18    # 18% N in DAP
    P_DAP = 0.46    # 46% P2O5 in DAP
    N_Urea = 0.46   # 46% N in Urea
    K_MOP = 0.60    # 60% K2O in MOP

    # 1. Calculate DAP (Priority: Phosphorus)
    if P_req > 0:
        DAP_kg = P_req / P_DAP
    else:
        DAP_kg = 0

    # 2. Subtract N supplied by DAP
    N_from_DAP = DAP_kg * N_DAP
    N_balance = max(N_req - N_from_DAP, 0)
    
    # 3. Urea Calculation (Balance N)
    if N_balance > 0:
        Urea_kg = N_balance / N_Urea
    else:
        Urea_kg = 0

    # 4. MOP Calculation (Potash)
    if K_req > 0:
        MOP_kg = K_req / K_MOP
    else:
        MOP_kg = 0

    return {
        "DAP_kg": round(DAP_kg, 2),
        "Urea_kg": round(Urea_kg, 2),
        "MOP_kg": round(MOP_kg, 2),
    }