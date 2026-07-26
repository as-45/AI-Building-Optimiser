"""
context_builder.py

Collects all information required by the LLM.
"""

from context.context_schema import Context


class ContextBuilder:

    def __init__(

        self,

        trend_analyzer,

        memory_retriever

    ):

        self.trend_analyzer = trend_analyzer

        self.memory_retriever = memory_retriever

    # ------------------------------------------------

    def build(

        self,

        building_state,

        history,

        current_episode,

        trigger

    ):

        trend = self.trend_analyzer.analyze(

            history

        )

        memories = self.memory_retriever.retrieve(

            current_episode

        )

        weather = {

            "temperature": building_state.outdoor_temperature,

            "humidity": building_state.outdoor_humidity

        }

        objectives = {

            "comfort": True,

            "energy": True,

            "carbon": True

        }

        return Context(

            current_state=building_state,

            trend_report=trend,

            retrieved_memories=memories,

            trigger=trigger,

            weather=weather,

            objectives=objectives

        )