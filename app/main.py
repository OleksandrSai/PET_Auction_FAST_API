from fastapi import FastAPI
from api_v1 import router as router_v1
from core.config import settings

app = FastAPI(name=settings.PROJECT_NAME, docs_url=settings.api_v1_prefix + "/docs")
app.include_router(router=router_v1, prefix=settings.api_v1_prefix)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
