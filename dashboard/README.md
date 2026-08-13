# Flask Comparison Dashboard

This dashboard provides a side-by-side comparison of baseline vs optimized simulation metrics.

## Run locally

From repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install Flask
python3 dashboard/app.py
```

Open: http://localhost:5000

## Data files

The app reads:

- `reports/baseline_metrics.json`
- `reports/optimized_metrics.json`

Both files must contain a top-level `metrics` object with:

- `total_energy_mwh`
- `total_energy_kwh`
- `hvac_electricity_mwh`
- `hvac_percent_of_total`

`reports/optimized_metrics.json` in this repository is simulated so the UI works immediately. If `reports/baseline_metrics.json` is also simulated in your local branch, replace both files with real simulation outputs before final submission.
