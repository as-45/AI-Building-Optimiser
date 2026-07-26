"""
Main MCP Server
"""

from mcp.server.fastmcp import FastMCP

from building_mcp.tool_registry import register_tools


mcp = FastMCP(
    "AI Building Optimizer"
)

register_tools(mcp)


if __name__ == "__main__":

    print("=" * 60)
    print(" AI Building Optimizer MCP Server ")
    print("=" * 60)

    mcp.run()