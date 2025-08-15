from typing import TypedDict, List, Sequence, Annotated
from langchain_core.messages import HumanMessage, BaseMessage, AIMessage
from langchain.chat_models import init_chat_model
from langgraph.graph import StateGraph, START, END, add_messages
from langgraph.prebuilt import create_react_agent
from langchain_google_community import GmailToolkit
from langchain_core.tools import tool
from langgraph.checkpoint.memory import InMemorySaver

checkpointer = InMemorySaver()

llm = init_chat_model("llama3-8b-8192", model_provider="groq", temperature=0.1)

@tool
def create_gmail_draft(to: List[str], subject: str, message: str) -> str:
    """Crea un borrador de correo en Gmail.

    Args:
        to: Lista de direcciones de email a las que enviar el correo.
        subject: Asunto del correo.
        message: Cuerpo del mensaje.
    """
    # Acá invocarías la API real de Gmail
    print("LA LLAMO")
    print(to)
    print(subject)
    print(message)

    # Llamar directamente al primer tool (por ejemplo, buscar mails no leídos)

    input_data = {
        "to": to,
        "subject": subject,
        "message": message,
    }

    func_to_generate_draft_mail = GmailToolkit().get_tools()[0]

    response = func_to_generate_draft_mail.invoke(input_data)


    print("FIN CALL")

    return response


agent = create_react_agent(
    model = llm, # Choice of the LLM
    tools = [create_gmail_draft] , # Tools we want our LLM to have
    name = "email_agent", # Name of our agent
    prompt = """
        Las tools disponibles son create_gmail_draft. 
        La respuesta final deberia ser algo ai:
        
        Se genero exitosame el correo draft dirigo al siguiente correo: snimo@mas.com.ar 

    """, # System Prompt
)




# 4. Definir el estado del agente
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    quantity : 0


# Definimos un nuevo nodo
def update_quantity(state: AgentState) -> AgentState:
    state["quantity"] = state.get("quantity", 0) + 1
    
    return state

# 5. Crear el grafo
graph = StateGraph(AgentState)
graph.add_node("upd_quantity" , update_quantity)
graph.add_node("agent", agent)

graph.set_entry_point("agent")
graph.add_edge("agent","upd_quantity")
graph.set_finish_point("upd_quantity")

# 6. Compilar el grafo
email_app = graph.compile(checkpointer=checkpointer)

result = email_app.invoke({
    "messages": [HumanMessage(content="Quiero crear un borrador de correo para LUCAS@ejemplo.com con asunto 'Cobranza' y el cuerpo que diga 'Toda la deuda'")]},
     config={"configurable": {"thread_id": "user_1"},
})

result = email_app.invoke(
    {"messages": [HumanMessage(content="Quiero crear un borrador de correo para LUCAS@ejemplo.com con asunto 'Cobranza' y el cuerpo que diga 'Toda la deuda'")]},
     config={"configurable": {"thread_id": "user_1"},
})

for msg in result["messages"]:
    print(type(msg) , msg)

print("La cantidad es ",result.get("quantity"))

result = email_app.invoke({
    "messages": [HumanMessage(content="Quiero crear un borrador de correo para LUCAS@ejemplo.com con asunto 'Cobranza' y el cuerpo que diga 'Toda la deuda'")]},
     config={"configurable": {"thread_id": "user_2"},
})

for msg in result["messages"]:
    print(type(msg) , msg)

print("La cantidad es ",result.get("quantity"))

