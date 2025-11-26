# ============================================================
# data_loader.py — SmartFert Engine
# FIX: Dynamic paths relative to engine folder.
# Works for structure:
#   /smart farmer multi webpage/
#       /data/  <-- JSONs here
#       /engine/ <-- Python scripts here
# ============================================================

import json
import os
import sys

# ------------------------------------------------------------
# DYNAMIC PATH CONFIGURATION
# ------------------------------------------------------------
# Get the directory where this script (data_loader.py) is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Go one level up and then into 'data'
DATA_DIR = os.path.join(BASE_DIR, "..", "data")

# Define Paths
PATH_MAIN = os.path.join(DATA_DIR, "production_dataset_final_ready.json")
PATH_ORGANIC = os.path.join(DATA_DIR, "organic_rules.json")
PATH_SOIL = os.path.join(DATA_DIR, "soil_fertility_thresholds.json")
# Note: Keeping the double extension as per your specific file
PATH_STCR_CONST = os.path.join(DATA_DIR, "stcr_equation_constants.json.json")


def load_json(path, required_keys=None):
    """
    Robust JSON loader that handles missing files and double extensions.
    """
    # 1. Check exact path
    if not os.path.exists(path):
        # 2. Check if .json.json needs to be .json
        if path.endswith(".json.json"):
            alt = path.replace(".json.json", ".json")
            if os.path.exists(alt):
                path = alt
        
        # 3. Final check
        if not os.path.exists(path):
            raise FileNotFoundError(f"❌ CRITICAL ERROR: Database file not found at: {path}")

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        raise ValueError(f"❌ JSON ERROR: Could not parse file {path}\nDetails: {e}")
    except Exception as e:
        raise Exception(f"❌ UNKNOWN ERROR loading {path}: {e}")

    # Validate Keys
    if required_keys:
        for key in required_keys:
            if key not in data:
                raise KeyError(f"❌ DATA ERROR: Key '{key}' missing in {path}")

    return data


def load_master_dataset():
    """Loads all SmartFert dataset components."""
    # print(f"🔍 System: Loading datasets from {DATA_DIR}...")
    
    main = load_json(PATH_MAIN, required_keys=["meta", "data"])
    organic = load_json(PATH_ORGANIC, required_keys=["organic_inputs", "special_rules"])
    soil = load_json(PATH_SOIL, required_keys=["critical_levels", "soil_fertility_thresholds"])
    stcr_const = load_json(PATH_STCR_CONST, required_keys=["stcr_equations"])

    MASTER = {
        "main": main,
        "data": main["data"],
        "organic_rules": organic,
        "soil_thresholds": soil,
        "stcr_constants": stcr_const,
    }
    return MASTER

# Test block
if __name__ == "__main__":
    try:
        M = load_master_dataset()
        print(f"✅ SUCCESS: Loaded {len(M['data'])} states successfully.")
    except Exception as e:
        print(f"🔥 FAIL: {e}")