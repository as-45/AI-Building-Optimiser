from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Tuple

from flask import Flask, jsonify, render_template

app = Flask(__name__, template_folder="templates")

REPORTS_DIR = Path(__file__).resolve().parent.parent / "reports"
BASELINE_PATH = REPORTS_DIR / "baseline_metrics.json"
OPTIMIZED_PATH = REPORTS_DIR / "optimized_metrics.json"

REQUIRED_FIELDS = (
    "total_energy_mwh",
    "total_energy_kwh",
    "hvac_electricity_mwh",
    "hvac_percent_of_total",
)


def _load_report(path: Path) -> Tuple[Dict[str, Any], str | None]:
    if not path.exists():
        return {}, f"Missing report file: {path.name}"

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return {}, f"Invalid JSON in {path.name}: {exc.msg}"

    metrics = data.get("metrics")
    if not isinstance(metrics, dict):
        return {}, f"Missing top-level 'metrics' object in {path.name}"

    missing = [field for field in REQUIRED_FIELDS if field not in metrics]
    if missing:
        return {}, f"Missing required metric fields in {path.name}: {', '.join(missing)}"

    return data, None


def _to_float(value: Any) -> float | None:
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def _build_compare_payload(baseline: Dict[str, Any], optimized: Dict[str, Any]) -> Dict[str, Any]:
    result: Dict[str, Any] = {"metrics": {}, "savings": {}}

    baseline_metrics = baseline.get("metrics", {})
    optimized_metrics = optimized.get("metrics", {})

    for key in REQUIRED_FIELDS:
        base_value = _to_float(baseline_metrics.get(key))
        opt_value = _to_float(optimized_metrics.get(key))

        result["metrics"][key] = {
            "baseline": base_value,
            "optimized": opt_value,
        }

        if base_value is None or opt_value is None:
            result["savings"][key] = None
            continue

        absolute_delta = base_value - opt_value
        percent_savings = (absolute_delta / base_value * 100.0) if base_value else None
        result["savings"][key] = {
            "absolute_delta": absolute_delta,
            "percent_savings": percent_savings,
        }

    return result


@app.get("/")
def index() -> str:
    return render_template("index.html")


@app.get("/api/baseline")
def baseline() -> tuple[Any, int] | Any:
    payload, error = _load_report(BASELINE_PATH)
    if error:
        return jsonify({"error": error}), 400
    return jsonify(payload)


@app.get("/api/optimized")
def optimized() -> tuple[Any, int] | Any:
    payload, error = _load_report(OPTIMIZED_PATH)
    if error:
        return jsonify({"error": error}), 400
    return jsonify(payload)


@app.get("/api/compare")
def compare() -> tuple[Any, int] | Any:
    baseline_payload, baseline_error = _load_report(BASELINE_PATH)
    if baseline_error:
        return jsonify({"error": baseline_error}), 400

    optimized_payload, optimized_error = _load_report(OPTIMIZED_PATH)
    if optimized_error:
        return jsonify({"error": optimized_error}), 400

    return jsonify(_build_compare_payload(baseline_payload, optimized_payload))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
