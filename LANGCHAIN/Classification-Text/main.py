from langchain.chat_models import init_chat_model
from langchain_core.documents import Document

model = init_chat_model("llama3-8b-8192", model_provider="groq"  )

