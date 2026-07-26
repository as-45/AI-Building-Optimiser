"""
Building Context Tool
"""

def register_building_context(server):

    @server.tool()

    def get_building_context():

        """
        Returns current building information.
        """

        return {
            "building": "Medium Office",
            "status": "Running",
            "message": "MCP Server Working"
        }