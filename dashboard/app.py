from flask import Flask, render_template, jsonify, send_from_directory
from pathlib import Path
import json

app = Flask(__name__, template_folder="templates", static_folder="static")

REPO_ROOT = Path(__file__).resolve().parent.parent
REPORTS_DIR = REPO_ROOT / "reports"
BASELINE_PATH = REPORTS_DIR / "baseline_metrics.json"
OPTIMIZED_PATH = REPORTS_DIR / "optimized_metrics.json"


def read_json(path: Path):
    if not path.exists():
        return {"error": f"File not found: {path}", "missing": True}
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        return {"error": str(e)}


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/api/baseline')
def api_baseline():
    return jsonify(read_json(BASELINE_PATH))


@app.route('/api/optimized')
def api_optimized():
    return jsonify(read_json(OPTIMIZED_PATH))


@app.route('/api/compare')
def api_compare():
    baseline = read_json(BASELINE_PATH).get('metrics', {})
    optimized = read_json(OPTIMIZED_PATH).get('metrics', {})

    try:
        b = float(baseline.get('total_energy_mwh', 0) or 0)
        o = float(optimized.get('total_energy_mwh', 0) or 0)
        percent_savings = None
        if b > 0:
            percent_savings = round(((b - o) / b) * 100, 2)
    except Exception:
        percent_savings = None

    return jsonify({
        'baseline': baseline,
        'optimized': optimized,
        'percent_savings_total_energy_mwh': percent_savings
    })


if __name__ == '__main__':
    # Run dev server directly
    app.run(host='0.0.0.0', port=5000, debug=True)
