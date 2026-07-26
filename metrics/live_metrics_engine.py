"""
Live Metrics Engine

Evaluates every zone separately.
"""

from metrics.comfort import ComfortEngine
from metrics.energy import evaluate_energy
from metrics.carbon import evaluate_carbon
from metrics.hvac import HVACMetric


class LiveMetricsEngine:

    def __init__(self):

        self.hvac = HVACMetric()
        self.comfort = ComfortEngine()

    # -------------------------------------------------

    def evaluate(self, building_state):

        zone_results = {}

        comfort_scores = []

        # --------------------------------------------
        # Evaluate each zone
        # --------------------------------------------

        for zone_name, zone in building_state.zones.items():

            # PMV Comfort
            comfort = self.comfort.evaluate(
                zone.temperature,
                zone.humidity
            )

            # HVAC Metric
            hvac = self.hvac.evaluate(
                current_hvac_power=building_state.hvac_power,
                current_temperature=zone.temperature,
                comfort_result=comfort
            )

            # ------------------------------------
            # Save PMV results inside ZoneState
            # ------------------------------------

            zone.pmv = comfort["pmv"]
            zone.ppd = comfort["ppd"]
            zone.thermal_sensation = comfort["thermal_sensation"]
            zone.comfort_level = comfort["comfort_level"]
            zone.comfort_score = comfort["score"]

            # ------------------------------------
            # Save metrics
            # ------------------------------------

            zone_results[zone_name] = {

                "comfort": comfort,

                "hvac": hvac

            }

            comfort_scores.append(

                comfort["score"]

            )

        # --------------------------------------------
        # Building Metrics
        # --------------------------------------------

        energy = evaluate_energy(

            building_state.building_power

        )

        carbon = evaluate_carbon(

            building_state.building_power

        )

        # --------------------------------------------
        # Building Comfort Summary
        # --------------------------------------------

        average_comfort = sum(comfort_scores) / len(comfort_scores)

        worst_zone = min(

            zone_results,

            key=lambda z: zone_results[z]["comfort"]["score"]

        )

        summary = {

            "average_comfort": round(average_comfort, 2),

            "worst_zone": worst_zone,

            "number_of_zones": len(zone_results)

        }

        return {

            "zones": zone_results,

            "energy": energy,

            "carbon": carbon,

            "summary": summary

        }