from fastapi import APIRouter, Response
from db import interfaces as I

from services.llm import generate_prompt, history_add_message, chat_completion
from services.db import DBUser
from services.llm_db import get_context
from openai.error import InvalidRequestError

from log import logger

router = APIRouter()


@router.post("/chat-compeltion/")
async def get_chat_completion(q_user: I.UserQuery, responce: Response):
    user = await DBUser.from_id(q_user.id)
    context_documents = await get_context(q_user.id, q_user.query)
    context = "\n".join(context_documents)
    prompt = generate_prompt(user.settings.prompt, context)
    history = user.settings.history

    history_add_message(
        role='user',
        message=q_user.query,
        history=history,
        max_history_size=user.settings.history_size,
        name=user.first_name,
    )
    try:
        model_answer = await chat_completion(
            history,
            prompt,
            user.settings.model_temperature)
    except InvalidRequestError as ex:
        responce.status_code = 400
        logger.warning(f"У {user} сработало ограничение по вводу токенов.")
        return {"answer": "Текст, отправленный на обработку (документы + промпт + история + запрос) оказался слишком большим. Возможные причины:\n\n1.История хранит слишкиом много сообщений.\n2.Введённый запрос слишком большой.\n3.Промпт слишком большой."}

    history_add_message(
        role='assistant',
        message=model_answer,
        history=history,
        max_history_size=user.settings.history_size,
    )

    async with user.update() as user_to_update:
        user_to_update.settings.history = history

    return {"answer": model_answer}
