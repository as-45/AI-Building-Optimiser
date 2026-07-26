from pathlib import Path

# ==========================================================
# Paths
# ==========================================================
PROJECT_ROOT = Path(__file__).resolve().parent.parent

IDF_FILE = PROJECT_ROOT / "model" / "medium_office.idf"

# ==========================================================
# Variables required for our AI Building Management System
# ==========================================================
OUTPUT_VARIABLES = [
    "Site Outdoor Air Drybulb Temperature",
    "Site Outdoor Air Relative Humidity",
    "Site Wind Speed",
    "Site Direct Solar Radiation Rate per Area",

    "Zone Air Temperature",
    "Zone Air Relative Humidity",

    "Facility Total Electricity Demand Rate",
    "Facility Total HVAC Electricity Demand Rate",

    "InteriorLights Electricity Rate",
    "InteriorEquipment Electricity Rate",

    "People Occupant Count",

    "Zone Air System Sensible Cooling Rate",
    "Zone Air System Sensible Heating Rate"
]

# ==========================================================
# Read IDF
# ==========================================================
with open(IDF_FILE, "r", encoding="utf-8") as f:
    idf_text = f.read()

added = 0

for variable in OUTPUT_VARIABLES:

    if variable in idf_text:
        print(f"[Already Exists] {variable}")
        continue

    block = f"""

Output:Variable,
    *,
    {variable},
    Hourly;

"""

    idf_text += block
    added += 1
    print(f"[Added] {variable}")

# ==========================================================
# Save
# ==========================================================
with open(IDF_FILE, "w", encoding="utf-8") as f:
    f.write(idf_text)

print("\n======================================")
print(f"Added {added} new Output Variables")
print("IDF Updated Successfully.")
print("======================================")