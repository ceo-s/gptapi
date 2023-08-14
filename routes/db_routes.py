from fastapi import APIRouter

from services.drive import GDrive
from services.db import User
from db import interfaces as I

router = APIRouter()


@router.post("/auth-user/")
async def authenticate_user(user_data: I.User):
    # user = await get_user(user_data.id)
    user = await User.from_pydantic(user_data)
    print(user_data.username)
    # print(f"{user.username=}")
    # print(f"{user.is_new=}")
    print(user.is_new)
    if user.is_new:
        # await register_user(user_data)
        await GDrive().mkdir(user_data.username)
        return {"authenticated": False}

    return {"authenticated": True}


@router.post("/get-user-data/")
async def get_user_data(user_data: I.OUser):
    user = await User.from_id(user_data.id)

    if not user:
        raise Exception("User was not found!")
    print(user.to_dict())
    return user.to_dict()


@router.post("/update-user-data/")
async def update_user_data(user_data: I.OUser):
    print(user_data.__dict__)
    user = await User.from_id(user_data.id)

    async with user.update() as updated_user:
        updated_user.username = "vanu4ka"
        print("UPDATED USER", updated_user)

    return {"Succsess": "200"}
