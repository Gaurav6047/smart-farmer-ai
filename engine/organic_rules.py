from typing import Dict, Tuple, List, Any
from .loader import load_organic_rules


class OrganicAndSpecialRulesEngine:
    """
    Handles:
    - Organic nutrient credit deduction
    - Special agronomic rules (pH, EC, rotation, micronutrients, fertigation)
    """

    def __init__(self):
        raw = load_organic_rules()
        self.org = raw.get("organic_inputs", {})
        self.rules = raw.get("special_rules", {})

        self.manures = self.org.get("manure", [])
        self.cakes = self.org.get("oilseed_cakes", [])

        # Map for quick lookup
        self.org_map = {item["name"]: item for item in (self.manures + self.cakes)}

    # ---------------------------------------------------------------------
    # ORGANIC CREDIT CALCULATION
    # ---------------------------------------------------------------------
    def apply_organic_credits(
        self,
        base_npk: Dict[str, float],
        applied: Dict[str, float]
    ) -> Tuple[Dict[str, float], Dict[str, float]]:
        """
        Deduct nutrients supplied by FYM, Vermicompost, Cakes etc.
        Formula:
            nutrient_kg = (applied_kg * percent) / 100
        """

        credits = {"N": 0, "P2O5": 0, "K2O": 0}

        # Loop over inputs applied by farmer
        for name, qty in applied.items():
            if qty <= 0:
                continue

            key = name.strip()
            if key not in self.org_map:
                continue

            src = self.org_map[key]

            credits["N"] += qty * src.get("N_percent", 0) / 100
            credits["P2O5"] += qty * src.get("P2O5_percent", 0) / 100
            credits["K2O"] += qty * src.get("K2O_percent", 0) / 100

        # Final elemental requirement = base - credits (not < 0)
        final = {
            "N": max(0, base_npk["N"] - credits["N"]),
            "P2O5": max(0, base_npk["P2O5"] - credits["P2O5"]),
            "K2O": max(0, base_npk["K2O"] - credits["K2O"]),
        }

        return final, credits

    # ---------------------------------------------------------------------
    # SPECIAL RULES (pH, EC, ROTATION, MICROS, SOIL-TYPE)
    # ---------------------------------------------------------------------
    def apply_special_rules(
        self,
        base_npk: Dict[str, float],
        soil: Dict[str, float],
        meta: Dict[str, Any]
    ) -> Tuple[Dict[str, float], List[str]]:
        """
        Applies special rules:
            - pH warnings
            - EC (salinity)
            - legume rotation N-credit
            - micronutrient advisory
        """

        alerts = []
        final = base_npk.copy()

        # ---------------------------
        # pH Rules
        # ---------------------------
        ph = soil.get("pH")
        ph_rules = self.rules.get("pH", {})

        if ph is not None:
            if ph < 5.5:
                rec = ph_rules.get("acidic_critical", {}).get("recommend")
                if rec:
                    alerts.append(f"Soil acidic (pH {ph}): {rec}")
            elif ph >= 8.5:
                rec = ph_rules.get("alkaline_critical", {}).get("recommend")
                if rec:
                    alerts.append(f"Soil alkaline (pH {ph}): {rec}")

        # ---------------------------
        # EC (Salinity)
        # ---------------------------
        ec = soil.get("EC")
        ec_rules = self.rules.get("EC", {})

        if ec is not None and ec > 2.0:
            adj = ec_rules.get("saline", {}).get("yield_adjustment", 0)
            alerts.append(
                f"High salinity (EC {ec}): ~{abs(adj)*100:.0f}% yield loss possible. Use salt-tolerant varieties."
            )

        # ---------------------------
        # Rotation: Legume → N credit
        # ---------------------------
        if meta:
            if meta.get("previous_crop_type") == "Legume":
                rot = self.rules.get("rotation", {})
                credit = rot.get("legume_credit", {}).get("N_minus", 0)
                if credit > 0:
                    final["N"] = max(0, final["N"] - credit)
                    alerts.append(f"Legume rotation: Nitrogen reduced by {credit} kg/ha.")

        # ---------------------------
        # Micronutrient Advisory
        # ---------------------------
        micro_rules = self.rules.get("micronutrients", {})
        for micro, rule in micro_rules.items():
            val = soil.get(micro) or soil.get(micro.upper()) or soil.get(micro.capitalize())
            if val is None:
                continue

            trigger = rule.get("trigger")
            if not trigger:
                continue

            try:
                # Example trigger: "< 0.6"
                op, thresh = trigger.split()
                thresh = float(thresh)

                if op == "<" and val < thresh:
                    alerts.append(f"{micro} deficiency: {rule.get('apply', '')}")
            except:
                pass

        return final, alerts
