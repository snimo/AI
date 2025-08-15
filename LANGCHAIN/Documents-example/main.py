
from langchain.chat_models import init_chat_model
from langchain_core.documents import Document

model = init_chat_model("llama3-8b-8192", model_provider="groq"  )


documents = [
    Document(page_content="El auto es de color rojo y puede ir a una velocidad de 300 kilometros por hora"),
    Document(page_content="La cantidad de empleados en la fabrica es de 200 personas"),
    Document(page_content="El color del caballo es blanco"),
]

from langchain_huggingface import HuggingFaceEmbeddings
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

from langchain_core.vectorstores import InMemoryVectorStore
vector_store = InMemoryVectorStore(embeddings)

# Devuelve una lista de ids de los documentos
document_ids = vector_store.add_documents(documents=documents)

# Obtener un retriever desde el vector store
retriever = vector_store.as_retriever(search_kwargs={"k": 2})

#Obtener un retriever
document_answers = retriever.invoke("Que cantidad de empleados hay en la fabrica?")

context = "\n\n".join(docu_text.page_content for docu_text in document_answers)

from langchain_core.messages import HumanMessage, SystemMessage , AIMessage

resp = model.invoke([
    SystemMessage(content=context),
    HumanMessage(content="Que cantidad de empleados hay en la fabrica?")
])

print(resp)




