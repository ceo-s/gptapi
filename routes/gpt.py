from fastapi import APIRouter
from db import interfaces as I

from services.llm import generate_prompt, history_add_message, chat_completion
from services.db import DBUser
from services.drive import GDrive

router = APIRouter()


@router.post("/chat-compeltion/")
async def get_chat_completion(q_user: I.UserQuery):
    user = await DBUser.from_id(q_user.id)
    # context = get_context(q_user.id, q_user.query)
    context = ""
    prompt = generate_prompt(user.settings.prompt, context)
    history = user.settings.history

    history_add_message(
        role='user',
        message=q_user.query,
        history=history,
        max_history_size=user.settings.history_size,
        name=user.first_name,
    )

    model_answer = chat_completion(
        history,
        prompt,
        user.settings.model_temperature)

    print(model_answer, prompt, history)

    history_add_message(
        role='assistant',
        message=model_answer,
        history=history,
        max_history_size=user.settings.history_size,
    )

    async with user.update() as user_to_update:
        user_to_update.settings.history = history

    print(history)
    return {"answer": model_answer}
