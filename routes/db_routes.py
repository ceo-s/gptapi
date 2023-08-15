from fastapi import APIRouter

from services.drive import GDrive
from services.db import DBUser
from services.db.embedding import UserCollection
from db import interfaces as I

router = APIRouter()


@router.post("/auth-user/")
async def authenticate_user(user_data: I.User):

    user = await DBUser.from_id(user_data.id)

    if not user:
        await user.create(user_data.username, user_data.first_name)
        GDrive().mkdir(user_data.username)
        return {"authenticated": False}

    return {"authenticated": True}


@router.post("/get-user-data/")
async def get_user_data(user_data: I.OUser):
    user = await DBUser.from_id(user_data.id)

    return user.dict()


@router.post("/update-user-data/")
async def update_user_data(user_data: I.OUser):
    user_dict = user_data.model_dump()
    user_dict.pop("id")
    settings_dict = user_dict.pop("settings", {})

    user = await DBUser.from_id(user_data.id)
    async with user.update() as user_to_update:
        for attr, val in user_dict.items():
            if val is not None:
                setattr(user_to_update, attr, val)

        for attr, val in settings_dict.items():
            if val is not None:
                setattr(user_to_update.settings, attr, val)

    return {"Succsess": "200"}


@router.get("/update-documents/")
async def update_documents(user_id: int, username: str, document_text: str):
    print("IM HEREE!!!")
    collection = await UserCollection.from_user(user_id)

    # await collection.add_document("1", "AAAA", metadata=I.DocumentMetadata(
    #     name="govno", description="AAA", token_cost=10
    # ))

    # document = await collection.update_document("2")
    # document.metadata_.description = "TI BARAN"
    # async with collection.update_document("2") as document:
    #     document.metadata_.description = "Hi"
    #     document.metadata_.name = "Bye"
    await collection.delete_document("1")
    # await collection.delete_document("2")
    # await collection.delete_document("3")
    await collection.commit()
    return {"succ": "ass"}
