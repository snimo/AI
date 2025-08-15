import os
from sentence_transformers import SentenceTransformer
import chromadb
import requests
from chromadb.config import Settings


# Initialize the Groq client

DOCUMENTO = "/Users/sebastiannimo/Projects/groq/train-model/plan_comercial.txt"
GROQ_MODEL = "llama3-70b-8192"
CHUNK_SIZE = 500
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")


# 1. Leer y dividir el documento
with open(DOCUMENTO, 'r', encoding='utf-8') as f:
    texto = f.read()


chunks = [texto[i:i+CHUNK_SIZE] for i in range(0, len(texto), CHUNK_SIZE)]

print(texto)

# 2. Crear embeddings
modelo_emb = SentenceTransformer("all-MiniLM-L6-v2")
embeddings = modelo_emb.encode(chunks)

# 3. Crear base Chroma local en memoria
chroma_client = chromadb.Client(Settings(anonymized_telemetry=False))
collection = chroma_client.create_collection(name="plan_comercial")

# 4. Cargar los chunks
collection.add(
    documents=chunks,
    embeddings=embeddings.tolist(),
    ids=[f"chunk_{i}" for i in range(len(chunks))]
)

# 5. Buscar contexto relevante
def buscar_contexto(pregunta, top_k=3):
    pregunta_emb = modelo_emb.encode([pregunta])[0]
    results = collection.query(query_embeddings=[pregunta_emb], n_results=top_k)
    return results['documents'][0]

# 6. Preguntar a Groq
def preguntar_a_groq(pregunta):
    contexto = buscar_contexto(pregunta)
    contexto_txt = "\n".join(contexto)
    prompt = f"""Contexto del plan comercial:
{contexto_txt}

Pregunta: {pregunta}
Respuesta:"""

    response = requests.post(
        "https://api.groq.com/openai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        },
        json={
            "model": GROQ_MODEL,
            "messages": [
                {"role": "user", "content": prompt}
            ]
        }
    )
    return response.json()["choices"][0]["message"]["content"]

# 7. Probarlo en consola
while True:
    q = input("¿Qué querés saber? (o 'salir') ")
    if q.lower() == "salir":
        break
    print(preguntar_a_groq(q))