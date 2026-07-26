from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent

CSV_FILE = PROJECT_ROOT / "simulations" / "baseline" / "eplusout.csv"

df = pd.read_csv(CSV_FILE)

print(df.head())

print("\nColumns:\n")

for col in df.columns:
    print(col)