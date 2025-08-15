from openai import OpenAI
import os
from langchain.prompts import ChatPromptTemplate

def map_role(role):
    return "user" if role == "human" else role

# Crear un prompt template
prompt_template = ChatPromptTemplate.from_messages(
    [
    ("system", "Traducir a {idioma} el siguiente texo"),
    ("user", "{text}")
    ]
)

resp = prompt_template.invoke({"idioma" : "Inglés" , "text":"Cual es tu nombre?"})

openai_messages = [
    {"role": map_role(msg.type), "content": msg.content}
    for msg in resp.to_messages()
]

print(openai_messages)

client = OpenAI(
    api_key=os.environ["GROQ_API_KEY"],
    base_url="https://api.groq.com/openai/v1"
)

response = client.chat.completions.create(
    model="llama3-8b-8192",
    messages= openai_messages,
    temperature=0.7
)

print("🤖 Respuesta:", response.choices[0].message.content)