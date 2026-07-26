"""
metrics_engine.py

Reads every timestep from virtual_sensors.csv,
evaluates all engineering metrics,
and generates an engineering report.
"""

import pandas as pd
from pathlib import Path

from comfort import evaluate_comfort
from energy import evaluate_energy
from carbon import evaluate_carbon
from hvac import HVACMetric

# -------------------------------------------------------
# Paths
# -------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

CSV_FILE = PROJECT_ROOT / "outputs" / "virtual_sensors.csv"

REPORT_DIR = PROJECT_ROOT / "reports"
REPORT_DIR.mkdir(exist_ok=True)

REPORT_FILE = REPORT_DIR / "engineering_report.csv"

# -------------------------------------------------------
# Read sensor data
# -------------------------------------------------------

df = pd.read_csv(CSV_FILE)

hvac_metric = HVACMetric()

engineering_report = []

# -------------------------------------------------------
# Evaluate every hour
# -------------------------------------------------------

for _, row in df.iterrows():

    temperature = row["Average Zone Temperature"]

    humidity = row["Average Zone Humidity"]

    building_power = row["Building Power"]

    hvac_power = row["HVAC Power"]

    comfort = evaluate_comfort(temperature)

    energy = evaluate_energy(building_power)

    carbon = evaluate_carbon(building_power)

    hvac = hvac_metric.evaluate(

        current_hvac_power=hvac_power,

        current_temperature=temperature,

        comfort_result=comfort

    )

    engineering_report.append({

        "DateTime": row["DateTime"],

        # --------------------------
        # Sensor Values
        # --------------------------

        "Temperature": temperature,

        "Humidity": humidity,

        "Building Power": building_power,

        "HVAC Power": hvac_power,

        # --------------------------
        # Engineering Scores
        # --------------------------

        "Comfort Score": comfort["score"],

        "Comfort Status": comfort["status"],

        "Energy Score": energy["score"],

        "Energy Status": energy["status"],

        "Carbon Score": carbon["score"],

        "Carbon Status": carbon["status"],

        "HVAC Score": hvac["score"],

        "HVAC Status": hvac["status"]

    })

# -------------------------------------------------------
# Save Report
# -------------------------------------------------------

report = pd.DataFrame(engineering_report)

report.to_csv(

    REPORT_FILE,

    index=False

)

print("\nEngineering Report Created Successfully!\n")

print(report.head())