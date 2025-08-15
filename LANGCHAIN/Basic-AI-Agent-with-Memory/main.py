from typing import TypedDict, List
from langchain_core.messages import HumanMessage, BaseMessage
from langchain.chat_models import init_chat_model
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import create_react_agent
from langchain_google_community import GmailToolkit

# Creation of the state using a Typed Dictionary
class AgentState(TypedDict):
    messages: List[BaseMessage] # We are going to be storing Human Messages (the user input) as a list of messages

llm = init_chat_model("llama3-8b-8192", model_provider="groq", temperature=0.1)

tools = [GmailToolkit()] # We are using the Inbuilt Gmail tool


print("Inicializar")

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

agent_state = {"messages" : []}
user_input = input("Enter: ")
while user_input != "exit":
    agent_state["messages"].append(HumanMessage(content=user_input))
    agent_state = agent.invoke(agent_state)
    user_input = input("Enter: ")


