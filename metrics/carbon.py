"""
carbon.py

Evaluates carbon emissions using
building power and the configured
grid emission factor.
"""

import json
from pathlib import Path

# --------------------------------------------------------
# Load Config
# --------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

CONFIG = PROJECT_ROOT / "config" / "building_config.json"

BASELINE = PROJECT_ROOT / "config" / "baseline.json"

with open(CONFIG) as f:
    config = json.load(f)

with open(BASELINE) as f:
    baseline = json.load(f)

EMISSION_FACTOR = config["carbon"]["grid_emission_factor"]

TARGET = config["carbon"]["target_reduction_percent"]

BASELINE_POWER = baseline["building_power"]

# --------------------------------------------------------
# Evaluation
# --------------------------------------------------------

def evaluate_carbon(current_power):

    # Convert W → kW
    current_kw = current_power / 1000

    baseline_kw = BASELINE_POWER / 1000

    current_carbon = current_kw * EMISSION_FACTOR

    baseline_carbon = baseline_kw * EMISSION_FACTOR

    reduction = ((baseline_carbon-current_carbon)/baseline_carbon)*100

    if reduction >= TARGET:

        score = 100
        status = "Excellent"

    elif reduction >= 10:

        score = 90
        status = "Good"

    elif reduction >= 5:

        score = 80
        status = "Acceptable"

    elif reduction >= 0:

        score = 70
        status = "No Improvement"

    else:

        score = max(0,70+reduction)
        status = "Higher Carbon"

    return {

        "metric":"carbon",

        "score":round(score,2),

        "status":status,

        "reason":[

            f"Current Carbon = {current_carbon:.2f} kg CO₂",

            f"Baseline Carbon = {baseline_carbon:.2f} kg CO₂",

            f"Reduction = {reduction:.2f}%"

        ],

        "details":{

            "baseline_carbon":round(baseline_carbon,2),

            "current_carbon":round(current_carbon,2),

            "reduction_percent":round(reduction,2)

        }

    }