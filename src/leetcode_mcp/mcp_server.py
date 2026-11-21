"""MCP tools, resources, and prompts."""
from mcp.server import MCPServer

mcp = MCPServer("Leetcode MCP Server")


@mcp.tool()
async def problem_details(slug: str) -> int:
    """
    gives context of the leetcode problem for the given slug
    """
    return -1

