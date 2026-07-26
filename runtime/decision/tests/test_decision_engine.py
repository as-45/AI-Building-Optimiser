import json

from runtime.decision.decision_engine import DecisionEngine


sample = {

    "decision": {

        "trigger": "Comfort",

        "strategy": "Balanced",

        "confidence": 0.92

    },

    "reasoning": {

        "comfort_priority": 0.85,

        "energy_priority": 0.70,

        "carbon_priority": 0.60,

        "why": "Maintain comfort while reducing HVAC energy.",

        "tradeoffs": [

            "Lighting reduced by 20%",

            "Cooling increased by 1°C"

        ]

    },

    "actions": [

        {

            "actuator": "Cooling Setpoint",

            "current": 24,

            "target": 25,

            "priority": "HIGH",

            "reason": "High electricity price"

        }

    ],

    "predictions": {

        "estimated_energy_saving_percent": 6,

        "estimated_carbon_reduction_percent": 5,

        "estimated_comfort_change": "Minimal",

        "assumptions": [

            "Normal occupancy"

        ]

    }

}


engine = DecisionEngine()

decision = engine.build(

    json.dumps(sample)

)

print()

print("Strategy :", decision.strategy)

print("Confidence :", decision.confidence)

print("Action :", decision.actions[0].actuator)

print("Target :", decision.actions[0].target)

print("Estimated Saving :", decision.estimated_energy_saving)

print()