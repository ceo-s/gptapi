from typing import Literal

BASE_PROMPT_TEMPLATE = """

Дополнительные сведения по вопросу (если они есть) находятся ниже, в тэге "справочный материал":
    <справочный материал>
        {}
    </справочный материал>
"""


def generate_prompt(prompt: str, context: str) -> str:
    return prompt + BASE_PROMPT_TEMPLATE.format(context)


def history_add_message(role: Literal["user", "assistant"], message: str, history: list[dict[str, str]], max_history_size: int, name: str = None) -> None:

    new_message = {
        "role": role,
        "content": message,
    }
    if name:
        new_message["name"] = name

    history.append(new_message)

    if len(history) > max_history_size:
        history.pop(0)
