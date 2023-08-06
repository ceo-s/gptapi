from typing import Literal

BASE_PROMPT_TEMPLATE = """

Ниже, предоставлен справочный материал по данному вопросу. Вы можете руководствоваться им, для повышения точности ответа.

Cправочный материал:
[{}]
"""


def get_context(query: str) -> str:
    return ""


def history_add_message(role: Literal["user", "assistant"], message: str, history: list[dict[str, str]], name: str = None) -> None:
    new_message = {
        "role": role,
        "content": message,
    }
    if name:
        new_message["name"] = name

    history.append(new_message)


def generate_prompt(query: str, prompt: str, base_template: bytes = BASE_PROMPT_TEMPLATE) -> str:
    context = get_context(query)
    return prompt + base_template.format(context)
