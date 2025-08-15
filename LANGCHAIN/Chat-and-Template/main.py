import getpass
import os

if not os.environ.get("GROQ_API_KEY"):
  os.environ["GROQ_API_KEY"] = getpass.getpass("Enter API key for Groq: ")

from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, SystemMessage , AIMessage

messages = [
  SystemMessage(content="Sos un asistente muy útil."),
  HumanMessage(content="¿Quién fue Albert Einstein?"),
  AIMessage(content="Einstein fue un físico teórico que desarrolló la teoría de la relatividad."),
  HumanMessage(content="¿Y cuándo nació?"),
]

model = init_chat_model("llama3-8b-8192", model_provider="groq"  )

resp = model.invoke(messages)

messages.append(AIMessage(content=resp.content))
messages.append(HumanMessage(content="Que edad tendria hoy en el año 2025?"))


resp = (model.invoke(messages))


print(resp)