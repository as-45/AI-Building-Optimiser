"""
Creates baseline.json from virtual_sensors.csv
"""

import json
from pathlib import Path

import pandas as pd

# --------------------------------------------------------
# Paths
# --------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

CSV_FILE = PROJECT_ROOT / "outputs" / "virtual_sensors.csv"

BASELINE_FILE = PROJECT_ROOT / "config" / "baseline.json"

# --------------------------------------------------------
# Read CSV
# --------------------------------------------------------

df = pd.read_csv(CSV_FILE)

# --------------------------------------------------------
# Calculate Baseline Statistics
# --------------------------------------------------------

baseline = {

    "building_power": round(df["Building Power"].mean(), 2),

    "hvac_power": round(df["HVAC Power"].mean(), 2),

    "avg_temperature": round(df["Average Zone Temperature"].mean(), 2),

    "avg_humidity": round(df["Average Zone Humidity"].mean(), 2),

    "avg_cooling_load": round(df["Total Cooling Load"].mean(), 2),

    "avg_heating_load": round(df["Total Heating Load"].mean(), 2)

}

# --------------------------------------------------------
# Save JSON
# --------------------------------------------------------

with open(BASELINE_FILE, "w") as f:

    json.dump(baseline, f, indent=4)

print("\nBaseline Successfully Created\n")

print(json.dumps(baseline, indent=4))