import os
import requests

# Load your API key from an environment variable
api_key = os.environ.get("GROQ_API_KEY")

# Define the endpoint and headers
url = "https://api.groq.com/openai/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

# Define the JSON payload
payload = {
    "model": "deepseek-r1-distill-llama-70b",
    "messages": [
        {
            "role": "user",
            "content": "What is the weather like in Paris today?"
        }
    ],
    "tools": [
        {
            "type": "function",
            "function": {
                "name": "get_weather",
                "description": "Get current temperature for a given location.",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "City and country e.g. Bogotá, Colombia"
                        }
                    },
                    "required": ["location"],
                    "additionalProperties": False
                },
                "strict": True
            }
        }
    ]
}

# Send the POST request
response = requests.post(url, headers=headers, json=payload)

# Print the result
print(response.status_code)
print(response.json())
