from fastapi import APIRouter

router = APIRouter(
    prefix="/protected",
    tags=["Protected resources"]
)