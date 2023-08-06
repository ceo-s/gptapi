from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def home():
    print("HOME SWEET HOME")
    return {"a": "b"}
