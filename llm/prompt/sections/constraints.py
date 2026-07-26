"""
Safety constraints.
"""


class ConstraintsSection:

    def build(self, context):

        return """
==========================
CONSTRAINTS
==========================

• Do not violate occupant comfort.

• Avoid large HVAC setpoint changes.

• Recommend only safe actions.

• Respect current building operation.
"""