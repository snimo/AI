from typing import TypedDict, Annotated, Sequence, Optional
from langchain_core.messages import HumanMessage, BaseMessage, SystemMessage, AIMessage
from langchain_core.tools import tool
from langgraph.constants import END, START
from langgraph.graph import StateGraph, add_messages
from langchain.chat_models import init_chat_model
import pprint

from langgraph.prebuilt import ToolNode

llm = init_chat_model("deepseek-r1-distill-llama-70b", model_provider="groq", temperature=0.1)

@tool
def get_saldo_stock(codigo_producto : str) -> str:
    """
    Devuelve la cantidad de producto que hay en Stock.
    """
    if (codigo_producto == "XXX"):
        return f"El producto {codigo_producto} tiene {333} unidades en stock."
    else:
        return f"El producto {codigo_producto} tiene {1000} unidades en stock."

@tool
def no_information(motivo: Optional[str] = None) -> str:
    """Informa que no hay información disponible. Se puede especificar el motivo."""
    if motivo:
        return f"No se encontró información porque: {motivo}"
    return "No se encontró información."

@tool
def get_costo_del_producto(codigo_producto : str ) -> str:
    """
    Función que devuelve el costo del producto en pesos
    """

    if (not codigo_producto) or (codigo_producto.strip()):
        return "No se pudo obtener información del costo. Código de producto inexistente."

    return f"El costo del producto {codigo_producto} es $ 1900"

tools = [get_saldo_stock,get_costo_del_producto,no_information]

llm = llm.bind_tools(tools)

node_tool_execution = ToolNode(tools)

class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

def node_no_information(state : AgentState) -> AgentState:
    return {"messages" : [AIMessage(content="No hay informacion")]}

def call_model(state : AgentState) -> AgentState:
    """
    El objetivo del Nodo es ejecutar una consulta contra el LLM con un System predefinido
    """

    system_prompt = """
    Eres un responsable de deposito.

    Solamente invocar a la función  get_saldo_stock si se quiere consultar el saldo de un producto
    1. 🛠️ `get_saldo_stock(codigo_producto: str)`  
       → Devuelve la cantidad de unidades disponibles en stock de un producto.

    Solamente invocar a la función  get_costo_del_producto si se quiere consultar el costo de un producto
    2. 🛠️ `get_costo_del_producto(codigo_producto: str)`  
       → Devuelve el costo del producto en pesos.

    Responder sobre el costo del producto si solamente pregunte por el mismo. Idem saldo.
    


    """


    new_prompt_messages = [SystemMessage(content=system_prompt)] + state["messages"]

    resp = llm.invoke(new_prompt_messages)

    return {"messages" : [resp]}

# Definimos un conditional Edge
def should_continue(state : AgentState) -> str:
    #Get the last message
    last_message = state["messages"][-1]
    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        if (last_message.tool_calls[0]['name']=="no_information"):
            return "node_no_information"
        else:
            return "node_tool_execution"
    else:
        return END

graph = StateGraph(AgentState)
graph.add_node("call_model" , call_model)
graph.add_node("node_tool_execution" , node_tool_execution)
graph.add_node("node_no_information" , node_no_information)
graph.add_edge(START,"call_model")
graph.add_conditional_edges("call_model" , should_continue)
graph.add_edge("node_tool_execution" , "call_model")
graph.add_edge("node_no_information" , END)
agent = graph.compile()

# Charlar con el LLM hasta obtener el saldo y costo del producto

final_state = agent.invoke({"messages" : [HumanMessage(content= """Saldo de stock y costo del producto XXX3?""")]})
last_message = final_state["messages"][-1]
print(last_message)





