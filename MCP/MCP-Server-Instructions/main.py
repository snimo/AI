# server.py
from fastmcp import FastMCP

mcp = FastMCP(
    name="DataAssistant",
    instructions="""
    You are a helpful data assistant.
    Use `get_average()` to calculate the average of a list of numbers.
    """
)

@mcp.tool
def get_average(numbers: list[float]) -> float:
    """Returns the average of a list of numbers"""
    return sum(numbers) / len(numbers)

if __name__ == "__main__":
    mcp.run(transport="http", port=8000)
