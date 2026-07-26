from pathlib import Path
import subprocess
import shutil

# -----------------------------
# Project Paths
# -----------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent

IDF_FILE = PROJECT_ROOT / "model" / "medium_office.idf"
WEATHER_FILE = PROJECT_ROOT / "weather" / "IND_Bangalore.432950_ISHRAE.epw"

OUTPUT_DIR = PROJECT_ROOT / "simulations" / "baseline"

# -----------------------------
# EnergyPlus Path
# CHANGE THIS ONLY IF REQUIRED
# -----------------------------
ENERGYPLUS_EXE = r"C:\EnergyPlusV26-1-0\energyplus.exe"

# -----------------------------
# Create Output Folder
# -----------------------------
if OUTPUT_DIR.exists():
    shutil.rmtree(OUTPUT_DIR)

OUTPUT_DIR.mkdir(parents=True)

# -----------------------------
# Command
# -----------------------------
command = [
    ENERGYPLUS_EXE,
    "-w",
    str(WEATHER_FILE),
    "-d",
    str(OUTPUT_DIR),
    str(IDF_FILE)
]

print("=" * 60)
print("Running EnergyPlus...")
print("=" * 60)

result = subprocess.run(command)

print("\nReturn Code:", result.returncode)

if result.returncode == 0:
    print("\nSimulation Completed Successfully!")
else:
    print("\nSimulation Failed!")