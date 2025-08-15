from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
import os

# Asegúrate de tener tu API key de Groq exportada o seteada
groq_api_key = os.environ.get("GROQ_API_KEY")

# Configura el modelo correctamente
llm = ChatOpenAI(
    model="llama3-8b-8192",  # También puedes usar mixtral-8x7b o gemma-7b-it
    openai_api_key=groq_api_key,
    openai_api_base="https://api.groq.com/openai/v1",
    temperature=0.7
)

# Mensaje para el modelo
respuesta = llm.invoke([HumanMessage(content="La capital de francia es")])
print(respuesta.content)

