"""
Optimization goals.
"""


class ObjectivesSection:

    def build(self, context):

        return """
==========================
OBJECTIVES
==========================

1. Minimize total building energy.

2. Maintain occupant thermal comfort.

3. Reduce HVAC energy.

4. Reduce operational carbon emissions.

5. Avoid unnecessary actuator changes.

6. Prefer actions with previously successful outcomes.
"""