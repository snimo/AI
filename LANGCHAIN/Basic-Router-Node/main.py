from typing import TypedDict, Annotated

from langchain_core.runnables import RunnableLambda
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, BaseMessage
import os

from langgraph.graph import add_messages, StateGraph

# Asegúrate de tener tu API key de Groq exportada o seteada
groq_api_key = os.environ.get("GROQ_API_KEY")

# Configura el modelo correctamente
llm = ChatOpenAI(
    model="llama3-8b-8192",  # También puedes usar mixtral-8x7b o gemma-7b-it
    openai_api_key=groq_api_key,
    openai_api_base="https://api.groq.com/openai/v1",
    temperature=0.7
)

class State(TypedDict):
    messages : Annotated[list[BaseMessage] , add_messages]

def nodoPrincipal(state : State) -> State:
    print("Principal")
    return state

def nodo1(state : State) -> State:
    print("Soy el nodo 1")
    return state

def nodo2(state : State) -> State:
    print("Soy el nodo 2")
    return state

def node_router(state : State) -> str:
    print("ejecuto")
    if (False):
        return "nodo1"
    else:
        return "nodo2"


graph = StateGraph(State)
graph.add_node("principal" , nodoPrincipal)
graph.add_node("nodo1" , nodo1)
graph.add_node("nodo2" , nodo2)
graph.add_node("router" , node_router)


graph.set_entry_point("principal")
graph.add_conditional_edges("principal" , node_router )
graph.set_finish_point("nodo1")
graph.set_finish_point("nodo2")
resp = graph.compile()
resp.invoke({"messages":[]})

