from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent

INPUT_CSV = PROJECT_ROOT / "simulations" / "baseline" / "eplusout.csv"
OUTPUT_CSV = PROJECT_ROOT / "outputs" / "virtual_sensors.csv"

OUTPUT_CSV.parent.mkdir(exist_ok=True)

df = pd.read_csv(INPUT_CSV)

temperature_cols = [
    c for c in df.columns
    if "Zone Air Temperature" in c
]

humidity_cols = [
    c for c in df.columns
    if "Zone Air Relative Humidity" in c
]

cooling_cols = [
    c for c in df.columns
    if "Cooling Rate" in c
]

heating_cols = [
    c for c in df.columns
    if "Heating Rate" in c
]

building_power = [
    c for c in df.columns
    if "Facility Total Electricity Demand Rate" in c
][0]

hvac_power = [
    c for c in df.columns
    if "Facility Total HVAC Electricity Demand Rate" in c
][0]

wind_speed = [
    c for c in df.columns
    if "Wind Speed" in c
][0]

humidity_outdoor = [
    c for c in df.columns
    if "Outdoor Air Relative Humidity" in c
][0]

solar = [
    c for c in df.columns
    if "Solar Radiation Rate" in c
][0]

virtual = pd.DataFrame()

virtual["DateTime"] = df["Date/Time"]

virtual["Average Zone Temperature"] = df[temperature_cols].mean(axis=1)

virtual["Average Zone Humidity"] = df[humidity_cols].mean(axis=1)

virtual["Total Cooling Load"] = df[cooling_cols].sum(axis=1)

virtual["Total Heating Load"] = df[heating_cols].sum(axis=1)

virtual["Building Power"] = df[building_power]

virtual["HVAC Power"] = df[hvac_power]

virtual["Outdoor Humidity"] = df[humidity_outdoor]

virtual["Wind Speed"] = df[wind_speed]

virtual["Solar Radiation"] = df[solar]

virtual.to_csv(OUTPUT_CSV, index=False)

print("="*60)
print("Virtual Sensors Created Successfully")
print("="*60)

print(virtual.head())

print("\nSaved to:\n")

print(OUTPUT_CSV)