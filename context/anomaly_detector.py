"""
Detect abnormal behaviour.
"""


class AnomalyDetector:

    def detect(self, history):

        anomalies = []

        if len(history) < 5:
            return anomalies

        latest = history[-1]

        if latest.building_power > 30000:

            anomalies.append(
                "Building power unusually high."
            )

        if latest.hvac_power > 20000:

            anomalies.append(
                "HVAC power unusually high."
            )

        return anomalies