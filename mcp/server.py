"""
MCP Server

Main entry point.
"""

from mcp.server.fastmcp import FastMCP

from mcp.tool_registry import register_tools


mcp = FastMCP(

    "AI Building Optimizer"

)


register_tools(mcp)


if __name__ == "__main__":

    print()

    print("=" * 60)

    print(" AI Building Optimizer MCP Server ")

    print("=" * 60)

    print()

    mcp.run()