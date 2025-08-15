import os
import instructor
from pydantic import BaseModel, Field
from groq import Groq

# Define the tool schema
groq_api_key = os.environ.get("GROQ_API_KEY")
tool_schema = {
    "name": "get_weather_info",
    "description": "Get the weather information for any location.",
    "parameters": {
        "type": "object",
        "properties": {
            "location": {
                "type": "string",
                "description": "The location for which we want to get the weather information (e.g., New York)"
            }
        },
        "required": ["location"]
    }
}

# Define the Pydantic model for the tool call
class ToolCall(BaseModel):
    input_text1: str = Field(description="The user's input text")
    tool_name: str = Field(description="The name of the tool to call")
    tool_parameters: str = Field(description="JSON string of tool parameters")

class ResponseModel(BaseModel):
    tool_calls: list[ToolCall]

# Patch Groq() with instructor
client = instructor.from_groq(Groq(api_key=groq_api_key,), mode=instructor.Mode.JSON)

def run_conversation(user_prompt):
    # Prepare the messages
    messages = [
        {
            "role": "system",
            "content": f"You are an assistant that can use tools. You have access to the following tool: {tool_schema}"
        },
        {
            "role": "user",
            "content": user_prompt,
        }
    ]

    # Make the Groq API call
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        response_model=ResponseModel,
        messages=messages,
        temperature=0.5,
        max_completion_tokens=1000,
    )

    print(response.tool_calls)

    return response.tool_calls

# Example usage
user_prompt = "What's the weather like in San Francisco?"
tool_calls = run_conversation(user_prompt)

for call in tool_calls:
    print(f"Input: {call.input_text1}")
    print(f"Tool: {call.tool_name}")
    print(f"Parameters: {call.tool_parameters}")
