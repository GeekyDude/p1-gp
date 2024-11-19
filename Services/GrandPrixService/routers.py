from fastapi import APIRouter
from endpoints import upload_controller
from endpoints import user_controller
from endpoints import driver_controller

router = APIRouter()

router.include_router(upload_controller.router, tags=["upload"])
router.include_router(user_controller.router, tags=["user"])
router.include_router(driver_controller.router, tags=["driver"])