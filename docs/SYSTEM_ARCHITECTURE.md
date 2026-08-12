# System Architecture — AI Building Optimiser (Short)

## Overview
This project implements a closed-loop Physical AI PoC that uses EnergyPlus as the digital building sandbox and an LLM agent (MCP/LLM) to read simulation telemetry, decide optimal set-points, and forward-inject supervisory overrides into EnergyPlus.

## Components
- EnergyPlus (simulation engine)
  - Inputs: .idf baseline models in `simulations/baseline/`
  - Output: `eplusout.eio`, `eplustbl.*` files, `eplusout.err`
- Parser & Metrics (extract_metrics.py + scripts/generate_baseline_metrics.py)
  - Extracts annual energy (MWh/kWh), HVAC breakdown, floor area and key summaries
  - Writes `reports/baseline_metrics.json` / `outputs/baseline_metrics.json`
- LLM Agent (llm/)
  - Responsible for reasoning about comfort vs. savings and producing ECMs (energy conservation measures)
  - Communicates with a MCP Server (local or hosted) to call tools and persist state
- MCP Server (building_mcp/ or agents/)
  - Receives telemetry (Feedback), forwards to LLM, sends actions back to EnergyPlus (Forward Injection)
- Runtime Controller (simulation/runtime_controller.py)
  - Orchestrates running EnergyPlus, streaming telemetry, and applying overrides

## Closed-loop Flow (mapping to evaluation criteria)
1. Feedback (EnergyPlus -> Agent)
   - Runtime controller polls simulation outputs and sends zone temps, energy usage, PMV estimates to the agent.
2. Reasoning (Agent)
   - LLM evaluates against constraints (occupancy, target comfort range) and proposes set-points or schedules.
3. Control Actions (Agent -> EnergyPlus)
   - Agent returns ECMs and dynamic set-points which the runtime_controller injects via actuation interface (e.g., BCVTB/EMS, or IDF override).
4. Forward Injection
   - The runtime must write inputs (e.g., override `.epJSON` or EMS code) and trigger the next simulation window.

## Deliverable mapping
- System Integration (30%): runtime_controller and MCP links must be robust; logs and error-handling required.
- Energy Efficiency (25%): baseline_metrics.json and post-run comparisons show realized % savings.
- Thermal Comfort (20%): include PMV or zone temperature time-series comparisons in final report.
- Agentic Autonomy & Code Elegance (15%): show LLM tool-calls, MCP interactions, and self-correction loops.
- Presentation & Documentation (10%): this docs file, dashboard, and the final PPT / video.

## How to run baseline extraction (quick)
1. Ensure baseline simulation outputs are in `simulations/baseline/` (eplustbl.csv or eplustbl.htm, eplusout.eio)
2. Run:
   ```bash
   python3 scripts/generate_baseline_metrics.py
   ```
3. Open `reports/dashboard.html` via a small HTTP server:
   ```bash
   cd reports
   python3 -m http.server 8000
   # Then open http://localhost:8000/dashboard.html
   ```
