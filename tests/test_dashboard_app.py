import json
import tempfile
import unittest
from pathlib import Path

import dashboard.app as dashboard_app


def _write_report(path, total_mwh, total_kwh, hvac_mwh, hvac_pct, simulation_type):
    path.write_text(
        json.dumps(
            {
                "metrics": {
                    "simulation_type": simulation_type,
                    "total_energy_mwh": total_mwh,
                    "total_energy_kwh": total_kwh,
                    "hvac_electricity_mwh": hvac_mwh,
                    "hvac_percent_of_total": hvac_pct,
                }
            }
        ),
        encoding="utf-8",
    )


class DashboardAppTests(unittest.TestCase):
    def test_compare_endpoint_returns_expected_savings(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            baseline = tmp_path / "baseline_metrics.json"
            optimized = tmp_path / "optimized_metrics.json"

            _write_report(baseline, 400, 400000, 220, 55, "baseline")
            _write_report(optimized, 360, 360000, 198, 55, "optimized")

            original_baseline = dashboard_app.BASELINE_PATH
            original_optimized = dashboard_app.OPTIMIZED_PATH
            dashboard_app.BASELINE_PATH = baseline
            dashboard_app.OPTIMIZED_PATH = optimized

            try:
                client = dashboard_app.app.test_client()
                response = client.get("/api/compare")
            finally:
                dashboard_app.BASELINE_PATH = original_baseline
                dashboard_app.OPTIMIZED_PATH = original_optimized

            self.assertEqual(response.status_code, 200)
            payload = response.get_json()
            self.assertEqual(payload["savings"]["total_energy_mwh"]["percent_savings"], 10.0)
            self.assertEqual(payload["savings"]["hvac_electricity_mwh"]["percent_savings"], 10.0)

    def test_baseline_endpoint_returns_400_when_file_missing(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_path = Path(tmp_dir)
            missing = tmp_path / "missing_baseline.json"
            optimized = tmp_path / "optimized_metrics.json"

            _write_report(optimized, 360, 360000, 198, 55, "optimized")

            original_baseline = dashboard_app.BASELINE_PATH
            original_optimized = dashboard_app.OPTIMIZED_PATH
            dashboard_app.BASELINE_PATH = missing
            dashboard_app.OPTIMIZED_PATH = optimized

            try:
                client = dashboard_app.app.test_client()
                response = client.get("/api/baseline")
            finally:
                dashboard_app.BASELINE_PATH = original_baseline
                dashboard_app.OPTIMIZED_PATH = original_optimized

            self.assertEqual(response.status_code, 400)
            self.assertIn("Missing report file", response.get_json()["error"])


if __name__ == "__main__":
    unittest.main()
