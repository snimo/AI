from smolagents import CodeAgent, LiteLLMModel

model = LiteLLMModel(
    "ollama/codellama:13b-python",  # el nombre del modelo cargado en Ollama
    api_base="http://localhost:11434",  # API de Ollama
    api_key=None  # no se necesita clave para Ollama local,
)

agent = CodeAgent(model=model, tools=[], add_base_tools=False)

result = agent.run("Python function to calculate 5 +6")
print(result)