"""
Energy metrics.
"""


class EnergySection:

    def build(self, context):

        state = context.current_state

        return f"""
==========================
ENERGY
==========================

Building Power

{state.building_power:.2f} W

HVAC Power

{state.hvac_power:.2f} W
"""