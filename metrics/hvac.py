"""
hvac.py

HVAC efficiency evaluation
"""

import json
from pathlib import Path

# --------------------------------------------------------
# Load Baseline
# --------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

BASELINE_FILE = PROJECT_ROOT / "config" / "baseline.json"

with open(BASELINE_FILE, "r") as f:
    baseline = json.load(f)

BASELINE_HVAC = baseline["hvac_power"]


# --------------------------------------------------------
# HVAC Metric
# --------------------------------------------------------

class HVACMetric:

    def evaluate(
        self,
        current_hvac_power,
        current_temperature,
        comfort_result
    ):

        saving = (
            (BASELINE_HVAC - current_hvac_power)
            / BASELINE_HVAC
        ) * 100

        comfort_ok = comfort_result["score"] >= 90

        # --------------------------------------------------

        if comfort_ok:

            if saving >= 15:

                score = 100
                status = "Excellent"

            elif saving >= 8:

                score = 90
                status = "Efficient"

            elif saving >= 0:

                score = 80
                status = "Acceptable"

            else:

                score = 60
                status = "Higher Consumption"

        else:

            if saving > 10:

                score = 55
                status = "Too Aggressive"

            else:

                score = 40
                status = "Poor Comfort"

        # --------------------------------------------------

        return {

            "metric": "hvac",

            "score": round(score, 2),

            "status": status,

            "reason": [

                f"Baseline HVAC = {BASELINE_HVAC:.2f} W",

                f"Current HVAC = {current_hvac_power:.2f} W",

                f"HVAC Saving = {saving:.2f}%",

                f"Comfort Level = {comfort_result['comfort_level']}",

                f"PMV = {float(comfort_result['pmv'])}",

                f"PPD = {float(comfort_result['ppd'])}%",

                f"Indoor Temperature = {current_temperature:.2f}°C"

            ],

            "details": {

                "baseline_hvac": BASELINE_HVAC,

                "current_hvac": current_hvac_power,

                "saving_percent": round(saving, 2),

                "temperature": current_temperature

            }

        }