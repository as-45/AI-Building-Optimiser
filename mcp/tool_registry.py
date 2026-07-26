"""
Registers every MCP tool.
"""

from tools.building_context import register_building_context


def register_tools(server):

    print()

    print("Registering MCP Tools...")

    register_building_context(server)

    print("Done.")