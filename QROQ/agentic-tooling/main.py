from groq import Groq
import os

groq_api_key = os.environ.get("GROQ_API_KEY")

client = Groq(
    api_key=groq_api_key,
)
completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "Cual es el precio del dolar blue hoy en Argentina. Hoy es 24 de Julio de 2025?"
        ,
        }
    ],
    # Change model to compound-beta to use agentic tooling
    # model: "llama-3.3-70b-versatile",
    model="compound-beta",
    include_domains=[]
)

print(completion.choices[0].message.content)
# Print all tool calls
# print(completion.choices[0].message.executed_tools)
