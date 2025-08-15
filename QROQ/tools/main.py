from groq import Groq
import json

# Initialize the Groq client
client = Groq()
# Specify the model to be used (we recommend Llama 3.3 70B)
MODEL = 'llama-3.3-70b-versatile'

def getSueldo(codigo_cliente : str , pais : str):
    """Obtiene el saldo bancario de un cliente"""
    try:
        result = 0
        # Segun el codigo de cliente obtiene el saldo bancario
        if ((codigo_cliente == "A100") and (pais == "ARG")):
            result = 1200
        elif codigo_cliente == "A200":
            result = 500
        else:
            result = 0
        return json.dumps({"resp": result})
    except:
        # Return an error message if the math expression is invalid
        return json.dumps({"error": "Invalid expression"})

# imports calculate function from step 1
def run_conversation(user_prompt):
    # Initialize the conversation with system and user messages
    messages=[
        {
            "role": "system",
            "content": "Se dispone de una función getSueldo que permite obtener el sueldo de un cliente, no utilizarla para obtener el saldo bancario de un cliente"
        },
        {
            "role": "user",
            "content": user_prompt,
        }
    ]
    # Define the available tools (i.e. functions) for our model to use
    tools = [
        {
            "type": "function",
            "function": {
                "name": "getSueldo",
                "description": "Obtiene el sueldo de un cliente",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "codigo_cliente": {
                            "type": "string",
                            "description": "Codigo de cliente",
                        },
                        "pais": {
                            "type": "string",
                            "description": "Codigo de Pais",
                        },
                    },
                    "required": ["codigo_cliente","pais"],
                },
            },
        }
    ]
    # Make the initial API call to Groq
    response = client.chat.completions.create(
        model=MODEL, # LLM to use
        messages=messages, # Conversation history
        stream=False,
        tools=tools, # Available tools (i.e. functions) for our LLM to use
        tool_choice="auto", # Let our LLM decide when to use tools
        max_completion_tokens=4096 # Maximum number of tokens to allow in our response
    )
    # Extract the response and any tool call responses
    print(response)
    response_message = response.choices[0].message
    print("**** La respuesta del modelo que detecta la funcion y contesta")
    print(response_message)
    print("****")
    print(response_message.tool_calls)
    print("*****")
    messages.append(response_message)

    tool_calls = response_message.tool_calls
    if tool_calls:
        # Define the available tools that can be called by the LLM
        available_functions = {
            "getSueldo": getSueldo,
        }
        # Add the LLM's response to the conversation
        messages.append(response_message)
        print("Este es el nuevo mensaje")
        print(messages)
        print("*****")

        # Process each tool call
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_to_call = available_functions[function_name]
            function_args = json.loads(tool_call.function.arguments)
            # Call the tool and get the response
            function_response = function_to_call(
                codigo_cliente=function_args.get("codigo_cliente"),
                pais =function_args.get("pais")
            )
            # Add the tool response to the conversation
            print(f"El contenido es {function_response}\n")
            respDeFuncConID =  {
                    "tool_call_id": tool_call.id,
                    "role": "tool", # Indicates this message is from tool use
                    "name": function_name,
                    "content": function_response,
                }
            messages.append(
                respDeFuncConID
            )
            print("*** Este es el mensaje finall con respuesta de la funcion")
            print(messages)
        # Make a second API call with the updated conversation
        second_response = client.chat.completions.create(
            model=MODEL,
            messages=messages
        )
        # Return the final response
        print(second_response)
        return second_response.choices[0].message.content
# Example usage
user_prompt = ("Cual es el sueldo del cliente A100 para el pais ARG?")
print(run_conversation(user_prompt))