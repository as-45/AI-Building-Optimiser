"""
Registers every MCP tool.
"""

from building_mcp.tools.building_context import register_building_context


def register_tools(server):

    print("Registering MCP Tools...")

    register_building_context(server)

    print("Registration Complete.")