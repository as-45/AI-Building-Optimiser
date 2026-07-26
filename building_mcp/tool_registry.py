"""
Registers every MCP tool.
"""

from building_mcp.tools.building_context import register_building_context
from building_mcp.tools.health import register_health
from building_mcp.tools.analyze_building import register_analyze_building


def register_tools(server):

    print("Registering MCP Tools...")

    register_health(server)

    register_building_context(server)

    register_analyze_building(server)

    print("Registration Complete.")