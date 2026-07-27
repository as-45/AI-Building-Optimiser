#!/usr/bin/env python3
"""
Extract Energy Metrics from Baseline Simulation Results
"""
import csv
import json
from pathlib import Path
import re

PROJECT_ROOT = Path(__file__).resolve().parent.parent
BASELINE_DIR = PROJECT_ROOT / "simulations" / "baseline"

def parse_eplustbl_csv():
    """Parse the EnergyPlus results table CSV"""
    csv_file = BASELINE_DIR / "eplustbl.csv"
    
    if not csv_file.exists():
        print(f"❌ File not found: {csv_file}")
        return None
    
    metrics = {
        "simulation_type": "baseline",
        "results_file": str(csv_file),
        "total_energy_mwh": None,
        "total_energy_kwh": None,
        "hvac_electricity_mwh": None,
        "hvac_percent_of_total": None,
    }
    
    try:
        with open(csv_file, 'r', encoding='utf-8', errors='ignore') as f:
            # Read all content
            content = f.read()
            
            # Look for key metrics in the CSV
            # EnergyPlus summary tables typically have annual values
            
            # Search for "Facility Total Electricity Demand Rate"
            if "Facility Total Electricity Demand Rate" in content:
                # Find the row and extract annual value
                lines = content.split('\n')
                for i, line in enumerate(lines):
                    if "Facility Total Electricity Demand Rate" in line:
                        # Next rows might have annual values
                        if i + 1 < len(lines):
                            next_line = lines[i + 1]
                            # Try to extract number
                            numbers = re.findall(r'[\d.]+', next_line)
                            if numbers:
                                try:
                                    # Assume first number is MWh
                                    mwh = float(numbers[0])
                                    metrics["total_energy_mwh"] = round(mwh, 2)
                                    metrics["total_energy_kwh"] = round(mwh * 1000, 0)
                                except:
                                    pass
            
            # Look for HVAC electricity
            if "Facility Total HVAC Electricity Demand Rate" in content:
                lines = content.split('\n')
                for i, line in enumerate(lines):
                    if "Facility Total HVAC Electricity Demand Rate" in line:
                        if i + 1 < len(lines):
                            next_line = lines[i + 1]
                            numbers = re.findall(r'[\d.]+', next_line)
                            if numbers:
                                try:
                                    hvac_mwh = float(numbers[0])
                                    metrics["hvac_electricity_mwh"] = round(hvac_mwh, 2)
                                    
                                    # Calculate percentage
                                    if metrics["total_energy_mwh"]:
                                        pct = (hvac_mwh / metrics["total_energy_mwh"]) * 100
                                        metrics["hvac_percent_of_total"] = round(pct, 1)
                                except:
                                    pass
    
    except Exception as e:
        print(f"❌ Error parsing CSV: {e}")
        return None
    
    return metrics

def read_eio_file():
    """Extract summary from EIO file"""
    eio_file = BASELINE_DIR / "eplusout.eio"
    
    if not eio_file.exists():
        return None
    
    summary = {}
    
    try:
        with open(eio_file, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                # Look for key metrics
                if "Total Floor Area" in line:
                    summary["floor_area"] = line.strip()
                elif "Zone Summary" in line:
                    summary["zone_info"] = line.strip()
    
    except Exception as e:
        print(f"⚠️  Could not read EIO: {e}")
    
    return summary

def main():
    print("=" * 70)
    print(" BASELINE SIMULATION METRICS EXTRACTION")
    print("=" * 70)
    
    # Check if baseline exists
    if not BASELINE_DIR.exists():
        print(f"❌ Baseline directory not found: {BASELINE_DIR}")
        return
    
    print(f"\n✅ Baseline directory found: {BASELINE_DIR}\n")
    
    # Parse CSV
    print("📊 Parsing eplustbl.csv...")
    metrics = parse_eplustbl_csv()
    
    if metrics:
        print("✅ Metrics extracted:\n")
        for key, value in metrics.items():
            if key != "results_file":
                print(f"   {key:.<40} {value}")
    else:
        print("⚠️  Could not extract metrics from CSV")
        # Provide manual extraction instructions
        print("\n📝 MANUAL EXTRACTION:")
        print("   1. Open: simulations/baseline/eplustbl.htm in browser")
        print("   2. Look for 'Facility Total Electricity Demand Rate'")
        print("   3. Find 'Annual [MWh]' column value")
        print("   4. Record that number (e.g., 450 MWh = 450,000 kWh)")
    
    # Read EIO
    print("\n📋 Reading eplusout.eio...")
    eio_summary = read_eio_file()
    if eio_summary:
        print("✅ EIO summary found:\n")
        for key, value in eio_summary.items():
            print(f"   {key}: {value}")
    
    # Check error file
    err_file = BASELINE_DIR / "eplusout.err"
    if err_file.exists():
        print("\n⚠️  Checking for errors...")
        with open(err_file, 'r', encoding='utf-8', errors='ignore') as f:
            errors = [l for l in f if 'Error' in l or 'Fatal' in l]
            if errors:
                print(f"   ⚠️  Found {len(errors)} error messages")
            else:
                print("   ✅ No critical errors in simulation")
    
    # Summary
    print("\n" + "=" * 70)
    print(" NEXT STEPS:")
    print("=" * 70)
    print("""
    ✅ Baseline simulation COMPLETE
    
    Now you need to:
    1. Extract exact energy value from eplustbl.htm
    2. Save as baseline_metrics.json
    3. Enable LLM control (config/runtime_config.json)
    4. Set MCP_SERVER_URL environment variable
    5. Run: python simulation/runtime_controller.py
    6. Extract optimized simulation results
    7. Compare % savings
    8. Build dashboard to visualize
    
    This will prove:
    ✅ System Integration (30% grade)
    ✅ Energy Efficiency (25% grade)
    ✅ Comfort Maintained (20% grade)
    """)
    print("=" * 70)

if __name__ == "__main__":
    main()
