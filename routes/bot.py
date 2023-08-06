from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from drive import GDrive
from views import get_page
from llm import generate_prompt, history_add_message, chat_completion

router = APIRouter()


class Admin(BaseModel):
    username: str


@router.post("/init-admin/")
async def init_admin(admin: Admin):
    GDrive().mkdir(admin.username)
    return {"success": "200"}


class ModelParams(BaseModel):
    name: str
    query: str
    model_temperature: float
    prompt: str
    history: list[dict[str, str]]


@router.post("/chat-compeltion/")
async def get_chat_completion(params: ModelParams):

    prompt = generate_prompt(
        params.query,
        params.prompt,
    )

    history_add_message(
        role="user",
        message=params.query,
        history=params.history,
        name=params.name,
    )

    answer = chat_completion(params.history, prompt, params.model_temperature)

    history_add_message(
        role="assistant",
        message=answer,
        history=params.history
    )

    return {"answer": answer, "history": params.history}


@router.get("/history/", response_class=HTMLResponse)
async def get_history_webapp():
    return get_page('bot_webapps', 'history')


@router.get("/creativity/", response_class=HTMLResponse)
async def get_temperature_webapp(temperature: float):
    # return get_page('bot_webapps', 'temperature', value=10)
    return get_page('bot_webapps', 'temperature', value=int(temperature * 100))
