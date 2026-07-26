"""
Building Context Tool
"""


def register_building_context(server):

    @server.tool()

    def get_building_context():

        """
        Returns the current building information.
        """

        return {

            "building_name": "Medium Office",

            "status": "Running",

            "message": "MCP connection successful."

        }