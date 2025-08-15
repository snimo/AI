from fastmcp import FastMCP
mcp = FastMCP("My MCP Server")

@mcp.tool
def greet(name : str) -> str:
    return f"Hello, {name}"

@mcp.tool
def age() -> int:
    return 52

@mcp.resource("data://config")
def get_config() -> dict:
    """Provides the application configuration."""
    return {"theme": "dark", "version": "1.0"}

if __name__ == "__main__":
    mcp.run(transport="http", port=8000)