"""
sensor_reader.py

Reads all monitored zones.
"""

from models.building_state import BuildingState

from models.zone_state import ZoneState


class SensorReader:

    def __init__(self, api, handle_manager):

        self.api = api

        self.handles = handle_manager

        self.timestep = 0

    # --------------------------------------------------

    def read(self, state):

        exchange = self.api.exchange

        self.timestep += 1

        zone_states = {}

        for zone, handles in self.handles.get("zones").items():
            zone_states[zone] = ZoneState(name=zone,
            temperature=exchange.get_variable_value(
                state,
                handles["temperature"]
    ),

            humidity=exchange.get_variable_value(
                state,
                handles["humidity"]
    ),

            predicted_heating_load=exchange.get_variable_value(
                state,
                handles["predicted_heating"]
    ),

            predicted_cooling_load=exchange.get_variable_value(
                state,
                handles["predicted_cooling"]
    ),

            actual_heating_rate=exchange.get_variable_value(
                state,
                handles["actual_heating"]
    ),

            actual_cooling_rate=exchange.get_variable_value(
                state,
                handles["actual_cooling"]
    )

)
        return BuildingState(

            timestep=self.timestep,

            outdoor_temp=exchange.get_variable_value(

                state,

                self.handles.get("outdoor_temp")

            ),

            outdoor_humidity=exchange.get_variable_value(

                state,

                self.handles.get("outdoor_humidity")

            ),

            building_power=exchange.get_variable_value(

                state,

                self.handles.get("building_power")

            ),

            hvac_power=exchange.get_variable_value(

                state,

                self.handles.get("hvac_power")

            ),

            zones=zone_states

        )