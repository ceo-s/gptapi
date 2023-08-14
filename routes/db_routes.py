from fastapi import APIRouter

from services.drive import GDrive
from services.db import User2
from db import interfaces as I

router = APIRouter()


@router.post("/auth-user/")
async def authenticate_user(user_data: I.User):
    # user = await get_user(user_data.id)
    user = await User2.from_pydantic(user_data)

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
    # user = await get_user(user.id)
    user = await User2.from_id(user_data.id)
    print("AAA", user.settings.prompt)
    if not user:
        raise Exception("User was not found!")

    return user.__dict__


# @router.post("/update-user-data/")
# async def update_user_data(user: I.OUser):
#     print(user.__dict__)
#     user_ = User()
#     await user_.ainit(user.id)

#     async with user_.update() as updated_user:
#         ...

#     return {"Succsess": "200"}
