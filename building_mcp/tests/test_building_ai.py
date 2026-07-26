"""
Tests the complete AI reasoning pipeline.
"""

from building_mcp.services.building_ai_service import BuildingAIService


building_context = {

    "building": {

        "outdoor_temperature": 35,

        "indoor_temperature": 27,

        "building_power": 18500,

        "hvac_power": 9200

    },

    "zones": [

        {

            "name": "Open Office",

            "temperature": 27.3,

            "humidity": 53,

            "pmv": 1.2,

            "ppd": 34,

            "occupancy": 18

        },

        {

            "name": "Meeting Room",

            "temperature": 28.1,

            "humidity": 58,

            "pmv": 1.6,

            "ppd": 48,

            "occupancy": 8

        }

    ],

    "metrics": {

        "comfort_score": 74,

        "energy_score": 61,

        "carbon_score": 65

    }

}


service = BuildingAIService()

result = service.analyze(

    building_context

)

print()

print("=" * 60)

print("AI RESULT")

print("=" * 60)

print()

print(result)