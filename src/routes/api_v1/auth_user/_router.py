from fastapi import APIRouter

router = APIRouter(
    prefix="/auth",
    tags=["User Authentication"]
)