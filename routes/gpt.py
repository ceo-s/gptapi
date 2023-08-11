from fastapi import APIRouter
from db.relational import interfaces as I

from services.llm import generate_prompt, history_add_message, chat_completion
from services.llm.db import get_context, get_collection_size
from services.db import get_user, update_user_settings
from services.drive import GDrive

router = APIRouter()


@router.post("/chat-compeltion/")
async def get_chat_completion(q_user: I.UserQuery):
    user = await get_user(q_user.id)
    context = get_context(q_user.id, q_user.query)
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

    await update_user_settings(
        user_id=user.id,
        settings=I.OSettings(history=history)
    )

    print(history)
    return {"answer": model_answer}


@router.post("update-documents")
async def update_documents(user: I.OUser):
    files = GDrive().listdir(user.username)
    updates = GDrive().check_updates()

    # file_ids_map = map(lambda x: x["id"], files)
    # col_size = get_collection_size(user.id)
    # print(f"COL SIZE {col_size} & LEN FILES {len(files)}")
    # print(user.id)
    # print(user.username)
    return {"result": "succ ass"}
