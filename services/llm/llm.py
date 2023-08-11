import dotenv
import os
import aiohttp
import openai
from openai.openai_object import OpenAIObject

dotenv.load_dotenv(".env")

openai.api_key = os.getenv("OPENAI_API_KEY")


def chat_completion(history: list[dict[str, str]], prompt: str, temperature: int) -> str:
    messages = [{
                "role": "system",
                "content": prompt
                }]
    messages += history

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=messages,
        temperature=temperature,
    )

    return response.get("choices")[0].message["content"].strip()


# prompt = generate_prompt(
#     "Ты - Бэтмен. На все вопросы задвигай триаду о преступности в своем Стиле.".encode(),
#     "Вчера в готеме взоравлся склад игрушками. Подозреваемый, скрываясь, подстрелил нескольких полицейских.".encode()
# )

# print(prompt)

# history = generate_chat_history(
#     '[{"role": "user", "content": "Сегодня прекрасный день, не правда ли?", "name": "Joker"}, \
#     {"role": "assistant", "content": "Длятся восхитительные будни жителей Готэма, но я не могу сказать, что день сегодня прекрасный. Я занят борьбой с преступностью и нежелательными элементами. Позвольте задать вам вопрос: вы знаете что-нибудь о складе игрушек, который был ограблен вчера?"}, \
#         {"role": "user", "content": "Знаю! Это был я! АЗХАХАХАХАХАХ", "name": "Joker"}]'.encode())


# answer = ask(history, prompt)
# answer: OpenAIObject

# res = answer.get("choices")[0].message["content"].strip()

# print(res)
# # print(res.to_dict()["message"]["content"])
