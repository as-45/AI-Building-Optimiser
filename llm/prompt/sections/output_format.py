"""
Required LLM response format.
"""


class OutputFormatSection:

    def build(self, context):

        return """
==========================
OUTPUT FORMAT
==========================

Respond ONLY with valid JSON.

{
    "reasoning": "...",

    "actions":[

        {
            "tool":"",

            "zone":"",

            "value":"",

            "priority":""
        }

    ],

    "expected_outcome":{

        "comfort":"",

        "energy":"",

        "carbon":""

    }
}
"""