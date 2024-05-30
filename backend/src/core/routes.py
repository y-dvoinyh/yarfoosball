from fastapi import APIRouter
from src.api.routers import all_routers


def get_apps_router():
    router = APIRouter()
    # router.include_router(admin_controller.router)
    for r in all_routers:
        router.include_router(r)
    return router
