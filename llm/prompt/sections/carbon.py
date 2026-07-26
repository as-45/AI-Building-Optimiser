"""
Carbon metrics.
"""


class CarbonSection:

    def build(self, context):

        carbon = context.current_state.building_power * 0.0007

        return f"""
==========================
CARBON
==========================

Estimated Carbon

{carbon:.2f} kg CO₂
"""