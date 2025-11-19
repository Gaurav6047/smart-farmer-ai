from typing import List


class AutoCropEngine:
    """
    Suggest crops based on Indian states + season.
    Simple rule-based heuristic (not ML).
    """

    def __init__(self):
        # Season-wise major crops (India)
        self.kharif = [
            "Rice", "Maize", "Cotton", "Sorghum (Jowar)", "Bajra",
            "Soybean", "Groundnut", "Pigeon Pea (Arhar)", "Urad", "Moong"
        ]

        self.rabi = [
            "Wheat", "Barley", "Mustard", "Chickpea (Chana)",
            "Pea", "Lentil (Masoor)", "Potato", "Onion", "Garlic"
        ]

        self.zaid = [
            "Pumpkin", "Cucumber", "Bitter Gourd", "Watermelon",
            "Muskmelon", "Summer Moong", "Groundnut (Zaid)"
        ]

        # State-based heuristics (light influence)
        self.state_bias = {
            "Punjab": ["Wheat", "Rice", "Maize"],
            "Haryana": ["Wheat", "Rice", "Mustard"],
            "UP": ["Wheat", "Rice", "Potato", "Sugarcane"],
            "Bihar": ["Maize", "Rice", "Pulses"],
            "MP": ["Soybean", "Wheat", "Gram"],
            "Maharashtra": ["Cotton", "Soybean", "Jowar"],
            "Gujarat": ["Groundnut", "Cotton", "Castor"],
            "Rajasthan": ["Bajra", "Mustard", "Moong"],
            "Tamil Nadu": ["Rice", "Sugarcane", "Groundnut"],
            "Karnataka": ["Ragi", "Maize", "Pulses"],
            "AP": ["Rice", "Groundnut", "Red Gram"],
            "Telangana": ["Cotton", "Maize", "Tur"],
            "West Bengal": ["Rice", "Jute", "Potato"],
            "Odisha": ["Rice", "Pulses"],
            "Chhattisgarh": ["Rice", "Maize"],
            "Jharkhand": ["Rice", "Maize", "Pulses"],
        }

    # ----------------------------------------------------------------------
    def suggest(self, state: str, season: str) -> List[str]:
        """
        Returns a crop list based on season + state preferences.
        """

        season = (season or "").lower()
        state = (state or "").strip()

        # Determine season set
        if "kharif" in season or "monsoon" in season:
            base = self.kharif
        elif "rabi" in season or "winter" in season:
            base = self.rabi
        elif "zaid" in season or "summer" in season:
            base = self.zaid
        else:
            base = self.kharif + self.rabi  # fallback

        # Apply state bias (if exists)
        if state in self.state_bias:
            bias = self.state_bias[state]
            # Put state-priority crops at front (unique)
            final = list(dict.fromkeys(bias + base))
        else:
            final = base

        return final
