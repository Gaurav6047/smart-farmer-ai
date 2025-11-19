import json
import pandas as pd
import os
from functools import lru_cache
from typing import Dict, Any

# ---------------------------------------
# Base Directory Resolver
# ---------------------------------------
# Resolves the project root based on this file's location
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELS_DIR = os.path.join(BASE_DIR, "models")


# ---------------------------------------
# DataLoader (Singleton via LRU Cache)
# ---------------------------------------
class DataLoader:
    """
    Handles all JSON/CSV loading with caching.
    Ensures files are loaded once per session.
    """

    @staticmethod
    @lru_cache(maxsize=1)
    def load_soil_fertility() -> Dict[str, Any]:
        """Load soil fertility thresholds JSON."""
        path = os.path.join(MODELS_DIR, "soil_fertility.json")
        if not os.path.exists(path):
            print(f"[WARN] Missing file: {path}")
            return {}
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"[ERROR] soil_fertility.json load failed: {e}")
            return {}

    @staticmethod
    @lru_cache(maxsize=1)
    def load_standard_npk() -> pd.DataFrame:
        """Load standard NPK CSV table."""
        path = os.path.join(MODELS_DIR, "standard_npk.csv")
        if not os.path.exists(path):
            print(f"[WARN] Missing file: {path}")
            return pd.DataFrame()
        try:
            return pd.read_csv(path)
        except Exception as e:
            print(f"[ERROR] standard_npk.csv load failed: {e}")
            return pd.DataFrame()

    @staticmethod
    @lru_cache(maxsize=1)
    def load_stcr_equations() -> Dict[str, Any]:
        """Load STCR equations JSON."""
        path = os.path.join(MODELS_DIR, "stcr_equations.json")
        if not os.path.exists(path):
            print(f"[WARN] Missing file: {path}")
            return {"crops": {}}
        try:
            return json.load(open(path, "r", encoding="utf-8"))
        except Exception as e:
            print(f"[ERROR] stcr_equations.json load failed: {e}")
            return {"crops": {}}

    @staticmethod
    @lru_cache(maxsize=1)
    def load_organic_rules() -> Dict[str, Any]:
        """Load Organic + Special rule JSON."""
        path = os.path.join(MODELS_DIR, "organic_rules.json")
        if not os.path.exists(path):
            print(f"[WARN] Missing file: {path}")
            return {"organic_inputs": {}, "special_rules": {}}
        try:
            return json.load(open(path, "r", encoding="utf-8"))
        except Exception as e:
            print(f"[ERROR] organic_rules.json load failed: {e}")
            return {"organic_inputs": {}, "special_rules": {}}


# ---------------------------------------
# Functional Shorthands (Cleaner Imports)
# ---------------------------------------
def load_soil_fertility(): return DataLoader.load_soil_fertility()
def load_standard_npk(): return DataLoader.load_standard_npk()
def load_stcr_equations(): return DataLoader.load_stcr_equations()
def load_organic_rules(): return DataLoader.load_organic_rules()
