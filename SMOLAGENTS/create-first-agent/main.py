#Example about how to create an agent using croq
import os
from smolagents import CodeAgent, InferenceClientModel , LiteLLMModel

# Initialize a model (using Hugging Face Inference API)
api_key = os.environ.get("GROQ_API_KEY")

model = LiteLLMModel(
    "llama-3.3-70b-versatile",
    api_base="https://api.groq.com/openai/v1",
    api_key=api_key
)

# Create an agent with no tools
agent = CodeAgent(tools=[], model=model)

# Run the agent with a task
#result = agent.run("Calculate the sum of numbers from 1 to 10")
result = agent.run("Funcion que suma dos numeros en este caso el 5 y el 10")
print(result)

print("\n📜 Agent Steps:")
for step in agent.memory.steps:
    print(f"\n--- Step: {type(step).__name__} ---")

    if hasattr(step, "input"):  # LLMStep or ToolStep
        print("Input:", step.input)

    if hasattr(step, "output"):
        print("Output:", step.output)

    if hasattr(step, "tool_name"):
        print("Tool Used:", step.tool_name)

# 💬 View summarized messages
print("\n💬 Agent Memory as Chat Messages:")
messages = agent.write_memory_to_messages()
for message in messages:
    print(f"{message.role.upper()}: {message.content}")