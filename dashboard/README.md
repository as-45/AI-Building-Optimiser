# Flask Dashboard — Setup & Run

This small Flask app serves a comparison dashboard between baseline and optimized metrics.

Prerequisites
- Python 3.8+
- Install Flask:
  pip install Flask

Run the app (from repository root):

  python3 dashboard/app.py

Then open http://localhost:5000 in your browser.

Where the app reads data
- Baseline metrics: reports/baseline_metrics.json
- Optimized metrics: reports/optimized_metrics.json

Replace these JSON files with your real outputs after running the baseline extractor and the optimization loop.
