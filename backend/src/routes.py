from fastapi import APIRouter


def get_apps_router():
    router = APIRouter()
    # router.include_router(admin_controller.router)
    return router
