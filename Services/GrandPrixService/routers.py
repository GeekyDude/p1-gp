from fastapi import APIRouter
from endpoints import upload_controller

router = APIRouter()

router.include_router(upload_controller.router, tags=["redirect"])