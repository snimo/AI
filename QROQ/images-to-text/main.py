import os
import json
from groq import Groq

# Initialize the Groq client
groq_api_key = os.environ.get("GROQ_API_KEY")

client = Groq(
    api_key=groq_api_key,
)

completion = client.chat.completions.create(
    model="meta-llama/llama-4-scout-17b-16e-instruct",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Poder obtener el número de la patente de este auto y devolverla en formato JSON con un solo atributo que sea patente y contenga solo el dato de la misma. Eliminar todo la resouesta menor el JSON, no quiero texto o informacion adicional que no sea el JSON solicitado."
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": "https://d343b4rj4wrvkr.cloudfront.net/static/uploads/2025/02/06/7cdb736253c0154be46d1d4c475d9aa3.webp?w=1920&q=75"
                    }
                }
            ]
        }
    ],
    temperature=1,
    max_completion_tokens=1024,
    top_p=1,
    stream=False,
    stop=None,
)

print(completion.choices[0].message)