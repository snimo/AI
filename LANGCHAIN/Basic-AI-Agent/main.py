from getpass import getpass

from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.prebuilt import create_react_agent  # Method to create ReAct agents easily
from langchain.chat_models import init_chat_model
from langchain_community.tools import DuckDuckGoSearchRun



prompt = """
You are my AI assistant that has access to certain tools. 
Use the tool DuckDuckGoSearchRun to get information from the WEB when needed.

Your main task is to extract the **current dollar exchange rate in Argentina** from reliable web search results.

Once you have it, respond with a JSON object in **this format**:

{
  "cotizacion_dolar": <only the number, no $ or other symbols>
}

For example, if the exchange rate is 1355 pesos per dollar, you must reply:

{
  "cotizacion_dolar": 1355
}

Make sure your answer is **valid JSON** and do not include any other text.
"""


tools = [DuckDuckGoSearchRun()]

llm = init_chat_model("llama3-8b-8192", model_provider="groq", temperature=0.1)

agent = create_react_agent(
    model = llm,
    tools = tools,  # Passing in the list of tools
    name = "search_agent"
)


result = agent.invoke({
    "messages": [
        SystemMessage(content=prompt),
        HumanMessage(content="¿Cual es la cotizacion del dolar hoy en Argentina? ")]
})

for msg in result["messages"]:
    if hasattr(msg, "tool_calls") and msg.tool_calls:
        print("Tool Calls:")
        for call in msg.tool_calls:
            print(f"  Tool: {call['name']}, Args: {call['args']}")

# Print the final answer
print("\nFinal Answer:")
print(result["messages"][-1].content)
