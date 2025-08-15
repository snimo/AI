import asyncio
import json
from fastmcp import Client

client = Client("http://127.0.0.1:8000/mcp")

async def call_tool(name: str):
    async with client:
        result = await client.call_tool("greet", {"name": name})
        print(result)
        result = await client.call_tool("age" , {})
        print(f"La edad es {result.data}")
        config = await client.read_resource("data://config")
        print("Configuration from server:", config[0].text)
        data = json.loads(config[0].text)
        print(data["theme"])
        data["theme"]="Green"
        print(data["theme"])


asyncio.run(call_tool("Sebastian Nimo"))

