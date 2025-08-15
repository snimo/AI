from typing import TypedDict, List, Sequence, Annotated, Optional

from duckduckgo_search import DDGS
from langchain_core.messages import HumanMessage, BaseMessage, AIMessage
from langchain.chat_models import init_chat_model
from langgraph.graph import StateGraph, START, END, add_messages
from langgraph.prebuilt import create_react_agent
from langchain_core.tools import tool
from langchain.tools import Tool


llm = init_chat_model("llama3-8b-8192", model_provider="groq", temperature=0.1)

@tool
def get_saldo_stock(codigo_producto : str) -> str:
    """
    Devuelve la cantidad de producto que hay en Stock.
    """
    print("****" , codigo_producto)
    if ((not codigo_producto) or (not codigo_producto.strip())):
       return "No se ingreso codigo de producto"
    else:
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
    print("**** ", codigo_producto)
    if (not codigo_producto) or (not codigo_producto.strip()):
        return "No se pudo obtener información del costo. Código de producto inexistente."

    return f"El costo del producto {codigo_producto} es $ 1900"

def search_duckduckgo(query: str) -> str:
    """
    Funcion que permite buscar en la web
    """
    with DDGS() as ddgs:
        results = ddgs.text(query, max_results=3)
        for r in results:
            return r['body']  # Primer snippet encontrado
    return "No se encontró información."


tools = [get_saldo_stock,get_costo_del_producto,no_information]


agent = create_react_agent(
    model = llm, # Choice of the LLM
    tools = tools , # Tools we want our LLM to have
    name = "agent_product", # Name of our agent
    prompt = """
            
        El código de producto tiene 3 caracteres. Si no se puede tomar un código de producto asumir que el codigo es '' como si nfuera un string vacio.
        Primer pasos es analizar si se ingresó un código de producto, si esto no es asi entonces terminar.
        
        Si no se puede identificar el código de producto, entonces arrojar un mensaje de respuesta "No se especifico el codigo de producto".

        Solamente invocar a la función  get_saldo_stock si se quiere consultar el saldo de un producto
         1. 🛠️ `get_saldo_stock(codigo_producto: str)`  
             → Devuelve la cantidad de unidades disponibles en stock de un producto.

        Solamente invocar a la función  get_costo_del_producto si se quiere consultar el costo de un producto
        2. 🛠️ `get_costo_del_producto(codigo_producto: str)`  
            → Devuelve el costo del producto en pesos.
            
        Cuando ejecutes una función suma la respuesta al historial de mensajes para darle contexto.

        Responder sobre el costo del producto si solamente pregunte por el mismo. Idem saldo.
        
        Si ya obtuviste la información de la tool para un mismo código de producto, no vuelvas a ejecutarla nuevamente. Si necesita analiza el resulta de la respuesta de la tool para responder.

        No invoques una función si no se pidio información sobre la misma.
        
        Si se pide información del costo y saldo en stock de producto, informar ambos.
        
        La respuesta final debería informa el costo del producto, o bien informar la cantidad en stock o biem ambos segun la consulta original. Nunca dejar la respuesta en blnaco.

    """, # System Prompt
)

# 4. Definir el estado del agente
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    quantity : int

# Definimos un nuevo nodo
def update_quantity(state: AgentState) -> AgentState:
    state["quantity"] = state.get("quantity", 0) + 1
    return state

# 5. Crear el grafo
graph = StateGraph(AgentState)
graph.add_node("upd_quantity" , update_quantity)
graph.add_node("agent", agent)

graph.set_entry_point("agent")
graph.add_edge("agent","upd_quantity")
graph.set_finish_point("upd_quantity")

# 6. Compilar el grafo
agente = graph.compile()

while (True):
    prompt = input("Ingresar prompt:")
    if (prompt == "exit"):
        break
    result = agente.invoke({
        "messages": [HumanMessage(content=prompt)]})
    for msg in result["messages"]:
        print(type(msg) , msg)

