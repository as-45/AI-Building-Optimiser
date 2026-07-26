"""
Test the complete Prompt Builder.
"""

from llm.prompt_builder import PromptBuilder

from context.context_schema import Context
from context.trend_report import TrendReport


# --------------------------------------------------
# Dummy Building State
# --------------------------------------------------

class DummyZone:

    def __init__(self):

        self.temperature = 25.8
        self.humidity = 44.2

        self.pmv = 0.35
        self.ppd = 7.0

        self.comfort_score = 95
        self.comfort_level = "Comfortable"
        self.predicted_cooling_load = 4200.0
        self.predicted_heating_load = 0.0


class DummyBuilding:

    def __init__(self):

        self.outdoor_temperature = 31.2
        self.outdoor_humidity = 64.5

        self.building_power = 18500
        self.hvac_power = 5100

        self.zones = {

            "CORE_TOP": DummyZone(),

            "CORE_BOTTOM": DummyZone()

        }


# --------------------------------------------------
# Trend Report
# --------------------------------------------------

trend = TrendReport(

    temperature_trend="Increasing",

    humidity_trend="Stable",

    hvac_trend="Increasing",

    power_trend="Increasing",

    comfort_trend="Declining",

    carbon_trend="Increasing",

    predicted_power=19200,

    predicted_hvac=5300,

    predicted_comfort=91

)

# --------------------------------------------------
# Retrieved Memory
# --------------------------------------------------

memory = [

    {

        "distance":0.13,

        "document":"""

Episode

Comfort degraded.

AI reduced cooling setpoint.

Energy reduced 8%.

Comfort recovered.

"""

    }

]

# --------------------------------------------------
# Context
# --------------------------------------------------

context = Context(

    current_state=DummyBuilding(),

    trend_report=trend,

    retrieved_memories=memory,

    trigger={

        "trigger":"Comfort"

    },

    weather={

        "temperature":31.2,

        "humidity":64.5

    },

    objectives={

        "comfort":True,

        "energy":True,

        "carbon":True

    }

)

builder = PromptBuilder()

prompt = builder.build(context)

print(prompt)