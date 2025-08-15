from langchain_openai import OpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
import os

# Crear el LLM
llm = OpenAI(model_name="llama3-8b-8192",
             api_key=os.environ["GROQ_API_KEY"],
             base_url="https://api.groq.com/openai/v1")  # o "llama3-8b-8192" si usás Groq

# Crear el prompt
prompt = PromptTemplate(
    input_variables=["question"],
    template="Responde en español: {question}"
)

# Crear el chain
chain = LLMChain(llm=llm, prompt=prompt)

# Ejecutar
respuesta = chain.run("¿Cuál es la capital de Francia?")
print("🧠 Respuesta:", respuesta)
