"""
Zone report.
"""


class ZoneSection:

    def build(self, context):
        building_state = context.current_state
        report = """

==========================================================
ZONE ANALYSIS
==========================================================

"""

        for zone_name, zone in building_state.zones.items():

            report += f"""
--------------------------------------------

{zone_name}

Temperature : {zone.temperature:.2f} °C

Humidity    : {zone.humidity:.2f} %

PMV         : {zone.pmv:.2f}

PPD         : {zone.ppd:.2f} %

Comfort     : {zone.comfort_level}

Cooling Load: {zone.predicted_cooling_load:.2f} W

Heating Load: {zone.predicted_heating_load:.2f} W

"""

        return report