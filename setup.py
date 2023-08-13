from dotenv import load_dotenv
import openai
import os
from pprint import pp

load_dotenv(".env")

openai.api_key = os.getenv("OPENAI_API_KEY")

texts = [
    "Hello my name is Gustavo, but you can call me Gus.",
    "-Say my Name! -Heisenberg... -You are god damn right."
]

embedding = openai.Embedding.create(
    input=texts, model="text-embedding-ada-002")

# for i in range(len(texts)):
pp(embedding)
pp(embedding["usage"]["total_tokens"])
