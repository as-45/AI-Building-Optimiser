"""
Contains all wake-up conditions.
"""


class TriggerRules:

    def comfort_trigger(self, assessment):

        return assessment["uncomfortable_zones"] > 0

    # ----------------------------------

    def energy_trigger(self, metrics):

        return metrics["energy"]["score"] < 80

    # ----------------------------------

    def carbon_trigger(self, metrics):

        return metrics["carbon"]["score"] < 80

    # ----------------------------------

    def trend_trigger(self, metrics):

        return metrics["summary"]["average_comfort"] < 90