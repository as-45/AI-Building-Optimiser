import json

from runtime.decision.decision_engine import DecisionEngine
from runtime.validator.response_validator import ResponseValidator
from runtime.executor.action_executor import ActionExecutor


sample = {

    "decision": {

        "trigger": "Comfort",

        "strategy": "Balanced",

        "confidence": 0.91

    },

    "reasoning": {

        "comfort_priority": 0.9,

        "energy_priority": 0.8,

        "carbon_priority": 0.7,

        "why": "Maintain comfort.",

        "tradeoffs": []

    },

    "actions": [

        {

            "actuator": "Cooling Setpoint",

            "current": 24,

            "target": 25,

            "priority": "HIGH",

            "reason": "High occupancy"

        }

    ],

    "predictions": {

        "estimated_energy_saving_percent": 6,

        "estimated_carbon_reduction_percent": 5,

        "estimated_comfort_change": "Minimal",

        "assumptions": []

    }

}


decision = DecisionEngine().build(

    json.dumps(sample)

)

validator = ResponseValidator()

result = validator.validate(decision)

if result.valid:

    executor = ActionExecutor()

    execution = executor.execute(decision)

    print()

    print("Success :", execution.success)

    print()

    print("Applied Actions")

    for a in execution.applied_actions:

        print(a)

else:

    print(result.errors)