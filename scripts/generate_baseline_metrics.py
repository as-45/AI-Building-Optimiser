#!/usr/bin/env python3
"""
Generate baseline_metrics.json using extract_metrics.py helpers.

Place this file in scripts/ and run:
  python3 scripts/generate_baseline_metrics.py
It will write outputs/baseline_metrics.json and reports/baseline_metrics.json (create dirs if needed).
"""
import json
from pathlib import Path
import sys

# Ensure the repo root is on path for imports
REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from extract_metrics import parse_eplustbl_csv, read_eio_file

OUTPUTS_DIR = REPO_ROOT / "outputs"
REPORTS_DIR = REPO_ROOT / "reports"
OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

def main():
    print("🔎 Generating baseline metrics...")
    metrics = parse_eplustbl_csv()
    eio_summary = read_eio_file()
    combined = {
        "metrics": metrics or {},
        "eio_summary": eio_summary or {},
        "generated_by": "scripts/generate_baseline_metrics.py"
    }

    out_path = OUTPUTS_DIR / "baseline_metrics.json"
    rpt_path = REPORTS_DIR / "baseline_metrics.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(combined, f, indent=2)
    with open(rpt_path, "w", encoding="utf-8") as f:
        json.dump(combined, f, indent=2)

    print(f"✅ Written: {out_path}")
    print(f"✅ Written: {rpt_path}")

    # Print quick summary
    m = combined["metrics"]
    if m:
        print("\nSUMMARY:")
        print(f"  Simulation Type : {m.get('simulation_type')}")
        print(f"  Total Energy (MWh): {m.get('total_energy_mwh')}")
        print(f"  Total Energy (kWh): {m.get('total_energy_kwh')}")
        print(f"  HVAC Electricity (MWh): {m.get('hvac_electricity_mwh')}")
        print(f"  HVAC % of total: {m.get('hvac_percent_of_total')}")
    else:
        print("⚠️ No metrics extracted. Check simulations/baseline/eplustbl.csv or eplustbl.htm")

if __name__ == "__main__":
    main()
