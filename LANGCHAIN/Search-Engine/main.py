"""
Build a semantic search engine

This tutorial will familiarize you with LangChain's document loader, embedding, and vector store abstractions.
These abstractions are designed to support retrieval of data—from (vector) databases and other sources—
for integration with LLM workflows.

They are important for applications that fetch data to be reasoned over as part of model inference,
as in the case of retrieval-augmented generation, or RAG (see our RAG tutorial here).

Here we will build a search engine over a PDF document. This will allow us to retrieve
passages in the PDF that are similar to an input query.

Concepts
This guide focuses on retrieval of text data. We will cover the following concepts:

Documents and document loaders;
Text splitters;
Embeddings;
Vector stores and retrievers.

"""


from langchain_community.document_loaders import PyPDFLoader

file_path = "rules.pdf"
loader = PyPDFLoader(file_path = file_path , mode= 'page' )

docs = loader.load()


print(f"Cantidad de documentos {len(docs)}")

"""

Splitting
For both information retrieval and downstream question-answering purposes, a page may be too coarse a representation.
 Our goal in the end will be to retrieve Document objects that answer an input query, and further splitting our PDF will help 
 ensure that the meanings of relevant portions of the document are not "washed out" by surrounding text.

We can use text splitters for this purpose. Here we will use a simple text splitter that partitions based on characters. 
We will split our documents into chunks of 1000 characters with 200 characters of overlap between chunks.
 The overlap helps mitigate the possibility of separating a statement from important context related to it.
  We use the RecursiveCharacterTextSplitter, which will recursively split the document using common separators 
  like new lines until each chunk is the appropriate size. This is the recommended text splitter for generic text use cases.

We set add_start_index=True so that the character index where each split Document starts within the initial Document is
 preserved as metadata attribute “start_index”.

"""

from langchain_text_splitters import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000, chunk_overlap=100, add_start_index=True
)
all_splits = text_splitter.split_documents(docs)

print(f"Cantidad de chuncks {len(all_splits)}")

"""

Embeddings
Vector search is a common way to store and search over unstructured data 
(such as unstructured text). The idea is to store numeric vectors that are associated with the text. 
Given a query, we can embed it as a vector of the same dimension and use vector similarity metrics
 (such as cosine similarity) to identify related text.

LangChain supports embeddings from dozens of providers. These models specify how text should be converted into a numeric vector. 
Let's select a model:

"""

from langchain_huggingface import HuggingFaceEmbeddings
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

"""

Vector stores
LangChain VectorStore objects contain methods for adding text and Document objects to the store, 
and querying them using various similarity metrics. 
They are often initialized with embedding models, which determine how text data is translated to numeric vectors.

"""
from langchain_core.vectorstores import InMemoryVectorStore
vector_store = InMemoryVectorStore(embeddings)
ids = vector_store.add_documents(documents=all_splits)

results = vector_store.similarity_search(
    " ¿Puede haber más de un encordado en la superficie de golpe de una raqueta?"
)

results = vector_store.similarity_search_with_score(
    " ¿Puede haber más de un encordado en la superficie de golpe de una raqueta?"
)

document , score = results[0]
print(score)

print(embeddings.embed_query("Esto se pasa a un vector"))

"""
Retrievers
LangChain VectorStore objects do not subclass Runnable. LangChain Retrievers are Runnables,
 so they implement a standard set of methods (e.g., synchronous and asynchronous invoke and batch operations).
  Although we can construct retrievers from vector stores, retrievers can interface with non-vector store sources of data, 
  as well (such as external APIs).

We can create a simple version of this ourselves, without subclassing Retriever.
 If we choose what method we wish to use to retrieve documents, we can create a runnable easily.
  Below we will build one around the similarity_search method:
"""

from typing import List
from langchain_core.documents import Document
from langchain_core.runnables import chain


@chain
def retriever(query: str) -> List[Document]:
    return vector_store.similarity_search(query, k=3)


resp = retriever.batch(
    [
        "Cuando un jugador pierde un punto?",
        "Sancionar a un jugador",
    ],
)

print(resp[0][0].page_content)
print(resp[0][1].page_content)
print(resp[0][2].page_content)

retriever = vector_store.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 1},
)

question = "como es la regla 10 que detalla el CAMBIO DE LADO?. Voy 2 a 1 en tie-break corresponde cambiar de lado?"

resp = retriever.invoke(
        question
)


context_loose_point = resp[0].page_content

#Se lo paso al LLM como System
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, SystemMessage , AIMessage

messages = [
  SystemMessage(content=context_loose_point),
  HumanMessage(content=question),
]

model = init_chat_model("llama3-8b-8192", model_provider="groq"  )

resp = model.invoke(messages)

print("🤖 Respuesta:", resp)

print("hola","como","estas")