import os
from groq import Groq

groq_api_key = os.environ.get("GROQ_API_KEY")

client = Groq(
    api_key=groq_api_key,
)

def moderar_con_llama_guard(texto):
    # Enviar el texto al modelo Llama Guard
    response = client.chat.completions.create(
        model="meta-llama/Llama-Guard-4-12B",
        messages=[
            {
                "role": "user",
                "content": texto
            }
        ]
    )

    # Mostrar resultado
    result = response.choices[0].message.content
    return result

# 📌 Texto de prueba (modificá este input como quieras)
entrada = "Odio a todos los que piensan diferente a mí. Deberían ser castigados."

moderacion = moderar_con_llama_guard(entrada)

print("🛡️ Resultado de la moderación:")
print(moderacion)


