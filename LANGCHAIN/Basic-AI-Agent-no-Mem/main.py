from typing import TypedDict, List
from langchain_core.messages import HumanMessage
from langchain.chat_models import init_chat_model
from langgraph.graph import StateGraph, START, END

# Creation of the state using a Typed Dictionary
class AgentState(TypedDict):
    messages: List[HumanMessage] # We are going to be storing Human Messages (the user input) as a list of messages

llm = init_chat_model("llama3-8b-8192", model_provider="groq", temperature=0.1)

# This is an action - the underlying function of our node
def process(state: AgentState) -> AgentState:
    response = llm.invoke(state["messages"])
    print(f"\nAI: {response.content}")
    return state

graph = StateGraph(AgentState) # Initialization of a Graph
graph.add_node("process_node", process) # Adding nodes
graph.add_edge(START, "process_node") # Adding edges
graph.add_edge("process_node", END)
agent = graph.compile() # Compiling the graph

resp = agent.invoke({"messages":[HumanMessage(content="Cual es la capital de Argentina?")]})
print(resp)
