from scheduler.trigger_rules import TriggerRules
from scheduler.trigger_result import TriggerResult


class InvocationScheduler:

    def __init__(self):

        self.rules = TriggerRules()

    # ----------------------------------

    def evaluate(

        self,

        building_state,

        metrics,

        assessment

    ):

        if self.rules.comfort_trigger(

            assessment

        ):

            return TriggerResult(

                True,

                "Comfort",

                "HIGH",

                0.97,

                "One or more zones uncomfortable."

            )

        if self.rules.energy_trigger(

            metrics

        ):

            return TriggerResult(

                True,

                "Energy",

                "HIGH",

                0.92,

                "Energy consumption increased."

            )

        if self.rules.carbon_trigger(

            metrics

        ):

            return TriggerResult(

                True,

                "Carbon",

                "MEDIUM",

                0.88,

                "Carbon emission increased."

            )

        if self.rules.trend_trigger(

            metrics

        ):

            return TriggerResult(

                True,

                "Trend",

                "LOW",

                0.75,

                "Comfort trend degrading."

            )

        return TriggerResult(

            False,

            "None",

            "LOW",

            1.0,

            "No reasoning required."

        )