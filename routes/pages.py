from fastapi import APIRouter
from fastapi.responses import HTMLResponse

from static import get_page

from services.db import DBUser
from db import interfaces as I


router = APIRouter()


@router.get("/history-menu/{user_id}", response_class=HTMLResponse)
async def get_history_menu(user_id: int):

    user = await DBUser.from_id(user_id)

    return get_page('bot_webapps', 'history_menu', user_id=user_id,
                    cur_len=len(user.settings.history),
                    max_len=user.settings.history_size,
                    )


@router.get("/history/{user_id}", response_class=HTMLResponse)
async def get_history(user_id: int):

    user = await DBUser.from_id(user_id)

    item_template = '<div class="history-item"><h4 class="history-itemRole">{role}:</h4><p class="history-itemContent">{content}</p></div>\n'
    history = ""
    for item in user.settings.history:
        history += item_template.format(role=item.get("name", item["role"]).capitalize(),
                                        content=item["content"])
    print(get_page('bot_webapps', 'history', user_id=user_id, history=history).body)
    return get_page('bot_webapps', 'history', user_id=user_id, history=history)


@router.get("/change-history-limit/{user_id}", response_class=HTMLResponse)
async def get_change_history_webapp(user_id: int):

    user = await DBUser.from_id(user_id)

    return get_page('bot_webapps', 'change_history_limit', user_id=user_id, cur_len=len(user.settings.history), max_len=user.settings.history_size)


@router.post("/post-change-history-limit/")
async def post_change_history(user_data: I.OUser):
    print(user_data)
    user = await DBUser.from_id(user_data.id)
    async with user.update() as user_to_update:
        user_to_update.settings.history_size = user_data.settings.history_size
        if user_data.settings.history_size < len(user_to_update.settings.history):
            history = user_to_update.settings.history[-(user_data.settings.history_size):]  # nopep8
            user_to_update.settings.history = history

    return {}


@router.get("/creativity/{user_id}", response_class=HTMLResponse)
async def get_temperature_webapp(user_id: int):
    user = await DBUser.from_id(user_id)

    return get_page('bot_webapps', 'temperature', user_id=user_id, value=int(user.settings.model_temperature * 100))
