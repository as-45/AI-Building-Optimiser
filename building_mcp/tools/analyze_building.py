"""
AI Analysis MCP Tool
"""

from building_mcp.services.building_ai_service import BuildingAIService

service = BuildingAIService()


def register_analyze_building(server):

    @server.tool()
    def analyze_building(context: dict):
        """
        Analyze the current building state using the AI.
        """

        result = service.analyze(context)

        return result