"""
Analyzes one hour of history.
"""

from statistics import mean

from context.trend_report import TrendReport


class TrendAnalyzer:

    def analyze(self, history):

        if len(history) < 2:

            return TrendReport(

                "Unknown",

                "Unknown",

                "Unknown",

                "Unknown",

                "Unknown",

                "Unknown",

                0,

                0,

                0

            )

        temps = [h.outdoor_temperature for h in history]

        power = [h.building_power for h in history]

        hvac = [h.hvac_power for h in history]

        comfort = []

        for h in history:

            scores = []

            for zone in h.zones.values():

                scores.append(zone.comfort_score)

            comfort.append(mean(scores))

        return TrendReport(

            temperature_trend="Increasing" if temps[-1] > temps[0] else "Decreasing",

            humidity_trend="Stable",

            hvac_trend="Increasing" if hvac[-1] > hvac[0] else "Decreasing",

            power_trend="Increasing" if power[-1] > power[0] else "Decreasing",

            comfort_trend="Improving" if comfort[-1] > comfort[0] else "Declining",

            carbon_trend="Increasing" if power[-1] > power[0] else "Decreasing",

            predicted_power=mean(power),

            predicted_hvac=mean(hvac),

            predicted_comfort=mean(comfort)

        )