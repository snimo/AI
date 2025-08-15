from smolagents import CodeAgent, InferenceClientModel
import os

api_key = os.environ.get("HUGGINGFACEHUB_API_TOKEN")


model_id = "meta-llama/Llama-3.3-70B-Instruct"

model = InferenceClientModel(model_id=model_id, token=api_key) # You can choose to not pass any model_id to InferenceClientModel to use a default model
# you can also specify a particular provider e.g. provider="together" or provider="sambanova"
# El parametro additional_authorized_imports indica que modulos se pueden importar
agent = CodeAgent(tools=[], model=model, add_base_tools=True , additional_authorized_imports=["requests", "pandas"])

result = agent.run(
    "Dado el precio de un producto de 1200, se le quiere agregar un 20% de descuento, cual seria el nuevo precio con dos decimales?",
)

print("resp:")
print(result)