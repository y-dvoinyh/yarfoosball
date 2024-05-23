from fastapi import FastAPI
from src.config.project_config import settings


app = FastAPI(
    title=settings.PROJECT_NAME,
    debug=settings.DEBUG,
    version=settings.VERSION
)


@app.get("/")
def read_root():
    return {"Hello": "World"}
