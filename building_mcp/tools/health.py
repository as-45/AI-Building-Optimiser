"""
Health Check Tool
"""


def register_health(server):

    @server.tool()
    def health():

        """
        Checks whether the MCP server is alive.
        """

        return {
            "status": "running",
            "server": "AI Building Optimizer MCP",
            "gpu": True
        }