from openai import OpenAI
import os
from langchain.prompts import PromptTemplate

# Crear un prompt template
template_habitantes = PromptTemplate(
    input_variables=["pais","ciudad"],
    template=(
            "Responde en español: "
             "¿Cuál es la cantidad de habitantes de {ciudad} ubicada en {pais}?"
            )
)

prompt_final = template_habitantes.format(pais="Argentina" , ciudad = "Buenos Aires")

client = OpenAI(
    api_key=os.environ["GROQ_API_KEY"],
    base_url="https://api.groq.com/openai/v1"
)

response = client.chat.completions.create(
    model="llama3-8b-8192",
    messages=[
        {"role": "user", "content": prompt_final}
    ],
    temperature=0.7
)

print("🤖 Respuesta:", response.choices[0].message.content)