from fastapi import APIRouter
from endpoints import upload_controller
from endpoints import user_controller

router = APIRouter()

router.include_router(upload_controller.router, tags=["upload"])
router.include_router(user_controller.router, tags=["user"])