"""
Building section.
"""


class BuildingSection:

    def build(self, context):

        building_state = context.current_state

        return f"""
==========================================================
CURRENT BUILDING
==========================================================

Outdoor Temperature

{building_state.outdoor_temperature:.2f} °C

Outdoor Humidity

{building_state.outdoor_humidity:.2f} %

Building Power

{building_state.building_power:.2f} W

HVAC Power

{building_state.hvac_power:.2f} W
"""