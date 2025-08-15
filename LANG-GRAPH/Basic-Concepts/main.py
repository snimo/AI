from typing import TypedDict, List, Sequence, Annotated
from langchain_core.messages import HumanMessage, BaseMessage, AIMessage
from langchain.chat_models import init_chat_model
from langgraph.graph import StateGraph, START, END, add_messages
from langgraph.prebuilt import create_react_agent
from langchain_google_community import GmailToolkit
from langchain_core.tools import tool
from langgraph.checkpoint.memory import InMemorySaver
from operator import add  # para sumar valores numéricos o concatenar listas

def last_value_merge(old, new):
    # Ignora el viejo, devuelve el nuevo
    return new

# 4. Definir el estado del agente
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    cantidad: Annotated[int, last_value_merge]  # suma los valores que llegan de varios nodos
    node_number : Annotated[int, last_value_merge]


def nodo1(state : AgentState) -> AgentState:
    state["cantidad"] = state.get("cantidad", 0) + 1
    state["messages"] = HumanMessage(content="Mensaje del Nodo 1")
    state["node_number"] = 1
    print("executa nodo 1")
    print("1",state)
    return state

def nodo2(state : AgentState) -> AgentState:
    state["cantidad"] = state.get("cantidad", 0) + 1
    state["node_number"] = 2
    print("executa nodo 2")
    print("2",state)
    return state

def nodo3(state : AgentState) -> AgentState:
    state["cantidad"] = state.get("cantidad", 0) + 1
    state["node_number"] = 3
    print("executa nodo 3")
    print("3",state)
    return state

def nodo4(state : AgentState) -> AgentState:
    state["cantidad"] = state.get("cantidad", 0) + 1
    state["node_number"] = 4
    print("executa nodo 4")
    print("4",state)
    return state


def decideNextStep(state : AgentState)->str:
    if (True):
        return "nodo4"
    else:
        return "nodo3"

# 5. Crear el grafo
graph = StateGraph(AgentState)
graph.add_node("nodo1" , nodo1)
graph.add_node("nodo2", nodo2)
graph.add_node("nodo3", nodo3)
graph.add_node("nodo4", nodo4)


graph.add_edge(START, "nodo1")
graph.add_edge("nodo1","nodo2")
graph.add_edge("nodo2","nodo3")
graph.add_edge("nodo3" , "nodo4")
graph.add_edge("nodo4" , END)

graph.add_conditional_edges("nodo2" , decideNextStep)


compiled = graph.compile()

compiled.invoke({
    "messages": [HumanMessage(content="Hola")],
    "quantity": 0
})


