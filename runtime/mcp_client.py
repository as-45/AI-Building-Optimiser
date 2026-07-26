"""
mcp_client.py

Communicates with the MCP Server running on RunPod.
"""

import requests


class MCPClient:

    def __init__(self, base_url):

        self.base_url = base_url.rstrip("/")

    # ----------------------------------------------------

    def analyze_building(self, context):

        """
        Sends the current building context
        to the MCP server.

        Returns the validated AI decision.
        """

        response = requests.post(

            f"{self.base_url}/analyze_building",

            json=context,

            timeout=180

        )

        response.raise_for_status()

        return response.json()