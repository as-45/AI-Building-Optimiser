"""
Building Context MCP Tool
"""

from shared.runtime_state import RuntimeState


def register_building_context(server):

    @server.tool()
    def get_building_context():
        """
        Returns the latest runtime information.
        """

        return {

            "building_state": RuntimeState.building_state,

            "metrics": RuntimeState.metrics,

            "assessment": RuntimeState.assessment

        }