"""
energy.py

Energy evaluation using the automatically generated baseline.
"""

import json
from pathlib import Path

# ---------------------------------------------------
# Load Baseline
# ---------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

BASELINE_FILE = PROJECT_ROOT / "config" / "baseline.json"

with open(BASELINE_FILE, "r") as f:
    baseline = json.load(f)

BASELINE_POWER = baseline["building_power"]

# ---------------------------------------------------
# Evaluation
# ---------------------------------------------------

def evaluate_energy(current_power):

    saving = BASELINE_POWER - current_power

    saving_percent = (saving / BASELINE_POWER) * 100

    if saving_percent >= 20:
        score = 100
        status = "Excellent"

    elif saving_percent >= 10:
        score = 90
        status = "Good"

    elif saving_percent >= 5:
        score = 80
        status = "Acceptable"

    elif saving_percent >= 0:
        score = 70
        status = "No Improvement"

    else:
        score = max(0, 70 + saving_percent)
        status = "Higher Consumption"

    return {

        "metric":"energy",

        "score":round(score,2),

        "status":status,

        "reason":[

            f"Baseline Power : {BASELINE_POWER:.2f} W",

            f"Current Power : {current_power:.2f} W",

            f"Saving : {saving_percent:.2f}%"

        ],

        "details":{

            "baseline":BASELINE_POWER,

            "current":current_power,

            "saving_percent":round(saving_percent,2)

        }

    }