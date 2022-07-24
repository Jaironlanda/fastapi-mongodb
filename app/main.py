from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import PlainTextResponse


from . import v1
from .v1 import main


tags_metadata = [
    {
        "name": "FastAPI and MongoDB",
        "description": "Basic CRUD",
    }
]

app = FastAPI()

app.include_router(v1.main.router)
