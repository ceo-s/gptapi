from fastapi import APIRouter

from services.drive import GDrive
from services.db import get_user, register_user, update_user, update_user_settings
from services.db.embedding import UserCollection
from db import interfaces as I

router = APIRouter()


@router.post("/auth-user/")
async def authenticate_user(user_data: I.User):
    # user = await get_user(user_data.id)
    # user = await User.from_pydantic(user_data)
    user = await get_user(user_data.id)
    print(user_data.username)
    # print(f"{user.username=}")
    # print(f"{user.is_new=}")

    if user is None:
        await register_user(user_data)
        await GDrive().mkdir(user_data.username)
        return {"authenticated": False}

    return {"authenticated": True}


@router.post("/get-user-data/")
async def get_user_data(user_data: I.OUser):
    # user = await User.from_id(user_data.id)
    user = await get_user(user_data.id)

    if not user:
        raise Exception("User was not found!")

    return user.__dict__


@router.post("/update-user-data/")
async def update_user_data(user_data: I.OUser):
    print(user_data)

    await update_user(user_data)
    if user_data.settings:
        print("UPDATING THIS SHIT")
        await update_user_settings(user_data.id, user_data.settings)

    return {"Succsess": "200"}


@router.get("/update-documents/")
async def update_documents(user_id: int, username: str, document_text: str):
    print("IN UPDATE DOCS", user_id, username, document_text)
    collection = await UserCollection.from_user(user_id)

    await collection.add_document(document_text, file_id="1",
                                  name="govno", description="AAA", token_cost=10)
    await collection.add_document(document_text+"aaa", file_id="2",
                                  name="govno2", description="AAA2", token_cost=10)
    # await collection.add_document(document_text, metadata=I.DocumentMetadata(
    #     file_id="1", name="govno", description="AAA", token_cost=10
    # ))
    await collection.commit()
    print(f"{collection.__dict__}")
    return {"succ": "ass"}
