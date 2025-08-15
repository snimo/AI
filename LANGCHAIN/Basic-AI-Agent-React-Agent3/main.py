from typing import TypedDict, List, Sequence, Annotated, Optional

from duckduckgo_search import DDGS
from langchain_core.messages import HumanMessage, BaseMessage, AIMessage
from langchain.chat_models import init_chat_model
from langgraph.graph import StateGraph, START, END, add_messages
from langgraph.prebuilt import create_react_agent
from langchain_core.tools import tool
from langchain.tools import Tool


llm = init_chat_model("llama3-8b-8192", model_provider="groq", temperature=0.1)


def dolar_blue_search(_):
    with DDGS() as ddgs:
        results = ddgs.text("valor del dólar blue hoy Argentina", max_results=1)
        for r in results:
            return r['body']
    return "No encontré información."

dolar_blue_tool = Tool(
    name="dolar_blue_search",
    func=dolar_blue_search,
    description="Busca en la web el valor actual del dólar blue."
)



tools = [dolar_blue_tool]


agent = create_react_agent(
    model = llm, # Choice of the LLM
    tools = tools , # Tools we want our LLM to have
    name = "agent_product", # Name of our agent
    prompt = """
            
       EL objetivo es que cuando necesites acceder a información muy reciente realices uns busqueda en la web a traves de la herramienta search_duckduckgo 

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

