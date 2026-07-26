"""
Shared Runtime State

Stores the latest building state so that
the MCP server and other modules can
access live simulation data.
"""


class RuntimeState:

    building_state = None

    metrics = None

    assessment = None