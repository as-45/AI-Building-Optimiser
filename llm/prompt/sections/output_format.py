"""
Required LLM response format.
"""


class OutputFormatSection:

    def build(self, context):

        return """
========================
OUTPUT FORMAT
========================

Return ONLY valid JSON.

Do NOT explain.

Do NOT use markdown.

Do NOT wrap inside ```.

Return EXACTLY this schema:

{
  "decision": {
    "trigger": "",
    "strategy": "",
    "confidence": 0.0
  },

  "reasoning": {
    "comfort_priority": 0.0,
    "energy_priority": 0.0,
    "carbon_priority": 0.0,
    "why": "",
    "tradeoffs": []
  },

  "actions": [
    {
      "actuator": "",
      "current": 0,
      "target": 0,
      "priority": "HIGH",
      "reason": ""
    }
  ],

  "predictions": {
    "estimated_energy_saving_percent": 0,
    "estimated_carbon_reduction_percent": 0,
    "estimated_comfort_change": "",
    "assumptions": []
  }
}
"""