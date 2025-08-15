
from groq import Groq
from fastmcp import Client
import asyncio


clientGroq = Groq(
    api_key="",
)

def transform_fastmcp_tools_for_groq(fastmcp_tools: any) -> any:
    """
    Transforma una lista de objetos Tool de FastMCP al formato requerido por Groq para 'tools'.
    """
    groq_formatted_tools = []
    for tool_obj in fastmcp_tools:
        # Asegúrate de que la descripción no sea None, ya que es importante para el LLM
        description = tool_obj.description if tool_obj.description else f"Una función para '{tool_obj.name}'."

        groq_tool = {
            "type": "function",
            "function": {
                "name": tool_obj.name,
                "description": description,
                "parameters": tool_obj.inputSchema  # ¡Aquí es donde mapeamos el inputSchema!
            }
        }
        groq_formatted_tools.append(groq_tool)
    return groq_formatted_tools


# Crear el cliente de FastMCP (conectado al servidor local)
client = Client("http://127.0.0.1:8000/mcp")

async def inicializar():
    async with client:
        groq_format_tools = transform_fastmcp_tools_for_groq(await client.list_tools())
        print(groq_format_tools)
        valor = await client.list_tools()
        # print(valor)
        # Prompt para el modelo
        prompt = "¿Cuál es el promedio de los siguientes números: 10, 20 y 30 , usa la tool get_average?"

        # Enviar al modelo llamando a FastMCP
        response = clientGroq.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "system", "content": "Actúa como un asistente de datos conectado a herramientas."},
                {"role": "user", "content": prompt}
            ],
            tools=groq_format_tools,  # Esto le permite al modelo usar las herramientas FastMCP
            tool_choice="auto"  # O forzá con {"type": "function", "function": {"name": "get_average"}}
        )

        print("**********************")
        print(response.choices[0])


asyncio.run(inicializar())

