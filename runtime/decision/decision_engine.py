import json

from runtime.decision.decision import Decision
from runtime.decision.decision import Action


class DecisionEngine:

    def build(self, llm_json: str):

        data = json.loads(llm_json)

        actions = []

        for action in data["actions"]:

            actions.append(

                Action(

                    actuator=action["actuator"],

                    current=action["current"],

                    target=action["target"],

                    delta = action["target"] - action["current"],

                    priority=action["priority"],

                    reason=action["reason"]

                )

            )

        return Decision(

            trigger=data["decision"]["trigger"],

            strategy=data["decision"]["strategy"],

            confidence=data["decision"]["confidence"],

            comfort_priority=data["reasoning"]["comfort_priority"],

            energy_priority=data["reasoning"]["energy_priority"],

            carbon_priority=data["reasoning"]["carbon_priority"],

            why=data["reasoning"]["why"],

            tradeoffs=data["reasoning"]["tradeoffs"],

            actions=actions,

            estimated_energy_saving=data["predictions"]["estimated_energy_saving_percent"],

            estimated_carbon_reduction=data["predictions"]["estimated_carbon_reduction_percent"],

            estimated_comfort_change=data["predictions"]["estimated_comfort_change"],

            assumptions=data["predictions"]["assumptions"]

        )