import os
import json
from groq import Groq

# Initialize the Groq client
groq_api_key = os.environ.get("GROQ_API_KEY")

client = Groq(
    api_key=groq_api_key,
)

speech_file_path = "/QROQ/speech-to-audio/speech.wav"
model = "playai-tts"
voice = "Fritz-PlayAI"
text = "I love building and shipping new features for our users!"
response_format = "wav"

response = client.audio.speech.create(
    model=model,
    voice=voice,
    input=text,
    response_format=response_format
)

response.write_to_file(speech_file_path)