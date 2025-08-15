import os
import io
import fitz  # PyMuPDF
import pytesseract
from PIL import Image
from sentence_transformers import SentenceTransformer
import chromadb
import requests
from chromadb.config import Settings

# CONFIG
PDF_PATH = "/QROQ/convert-pdf-to-text/plan.pdf"  # Ruta al PDF
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")  # Debe estar seteada como variable de entorno
GROQ_MODEL = "llama3-70b-8192"
CHUNK_SIZE = 500

# Tesseract path (si es necesario)
pytesseract.pytesseract.tesseract_cmd = "/opt/homebrew/bin/tesseract"

# 1. Extraer texto y OCR del PDF
def extraer_texto_y_ocr(pdf_path):
    contenido = []
    doc = fitz.open(pdf_path)

    for page in doc:
        # Texto directo
        texto = page.get_text()
        if texto.strip():
            contenido.append(texto)

        # Texto desde imágenes (OCR)
        for img_index, img in enumerate(page.get_images(full=True)):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image = Image.open(io.BytesIO(image_bytes))
            texto_img = pytesseract.image_to_string(image)
            if texto_img.strip():
                contenido.append(texto_img)

    doc.close()
    return "\n".join(contenido)

# 2. Chunking
def dividir_en_chunks(texto, tamaño=CHUNK_SIZE):
    return [texto[i:i+tamaño] for i in range(0, len(texto), tamaño)]

# 3. Crear base Chroma con embeddings
def crear_chroma(chunks):
    modelo_emb = SentenceTransformer("all-MiniLM-L6-v2")
    embeddings = modelo_emb.encode(chunks)

    chroma_client = chromadb.Client(Settings(anonymized_telemetry=False))
    collection = chroma_client.create_collection(name="pdf_info")
    collection.add(
        documents=chunks,
        embeddings=embeddings.tolist(),
        ids=[f"chunk_{i}" for i in range(len(chunks))]
    )
    return collection, modelo_emb

# 4. Buscar contexto relevante
def buscar_contexto(pregunta, collection, modelo_emb, top_k=3):
    pregunta_emb = modelo_emb.encode([pregunta])[0]
    resultados = collection.query(query_embeddings=[pregunta_emb], n_results=top_k)
    return resultados['documents'][0]

# 5. Preguntar a Groq
def preguntar_a_groq(pregunta, contexto):
    contexto_txt = "\n".join(contexto)
    prompt = f"""Contexto:
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

# MAIN
if __name__ == "__main__":
    print("🔍 Extrayendo información del PDF...")
    texto = extraer_texto_y_ocr(PDF_PATH)
    chunks = dividir_en_chunks(texto)
    collection, modelo_emb = crear_chroma(chunks)
    print("✅ Base lista. Preguntá lo que quieras sobre el PDF.\n")

    while True:
        pregunta = input("❓ Pregunta (o 'salir'): ")
        if pregunta.lower() == "salir":
            break
        contexto = buscar_contexto(pregunta, collection, modelo_emb)
        respuesta = preguntar_a_groq(pregunta, contexto)
        print(f"\n🧠 Respuesta:\n{respuesta}\n")

