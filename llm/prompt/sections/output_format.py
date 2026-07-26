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
  "reasoning": {
    "comfort_priority": 0.0,
    "energy_priority": 0.0,
    "carbon_priority": 0.0,
    "confidence": 0.0
  },

  "actions": [
    {
      "actuator": "",
      "current": 0,
      "target": 0,
      "delta": 0,
      "reason": ""
    }
  ],

  "predictions": {
    "expected_energy_saving_percent": 0,
    "expected_carbon_reduction_percent": 0,
    "expected_pmv": 0
  }
}
"""