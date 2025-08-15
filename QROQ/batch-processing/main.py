import os

from groq import Groq

groq_api_key = ""

print(groq_api_key)

client = Groq(
    api_key=groq_api_key,
)

file_path = "/QROQ/batch-processing/batch_file.jsonl"
response = client.files.create(file=open(file_path, "rb"), purpose="batch")

print(response)


