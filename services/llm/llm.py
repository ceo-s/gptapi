import dotenv
import os
import aiohttp
import openai
from openai.openai_object import OpenAIObject

dotenv.load_dotenv(".env")

openai.api_key = os.getenv("OPENAI_API_KEY")


async def chat_completion(history: list[dict[str, str]], prompt: str, temperature: int) -> str:
    messages = [{
                "role": "system",
                "content": prompt
                }]
    messages += history

    response = await openai.ChatCompletion.acreate(
        model="gpt-3.5-turbo-0613",
        messages=messages,
        temperature=temperature,
    )

    return response.get("choices")[0].message["content"].strip()
