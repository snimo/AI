import os
from groq import Groq

groq_api_key = os.environ.get("GROQ_API_KEY")

client = Groq(
    api_key=groq_api_key,
)

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": 'La cpaital de francia es '
        }
    ],
    model="llama-3.3-70b-versatile",
    stop=["\n\n", "Respuesta:", "Explicación:","```"]
)

print(chat_completion.choices[0].message.content)


