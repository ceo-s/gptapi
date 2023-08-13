from fastapi import APIRouter

from services.drive import GDrive
from services.db import get_user, register_user, update_user, update_user_settings
from services.db import User
from db import interfaces as I

router = APIRouter()


@router.post("/auth-user/")
async def authenticate_user(user_data: I.User):
    # user = await get_user(user_data.id)
    user = await User(user_data)
    user
    if user:
        await register_user(user_data)

        await GDrive().mkdir(user_data.username)
        return {"authenticated": False}

    return {"authenticated": True}


@router.post("/get-user-data/")
async def get_user_data(user: I.OUser):
    user = await get_user(user.id)

    if not user:
        raise Exception("User was not found!")

    return user.__dict__


@router.post("/update-user-data/")
async def update_user_data(user: I.OUser):
    print(user.__dict__)
    await update_user(user)
    await update_user_settings(user.id, user.settings)
    return {"Succsess": "200"}
