from .config import get_settings, Settings

from fastapi import FastAPI, Request
from contextlib import asynccontextmanager
from langchain-

@asynccontextmanager
async def lifespan(app: FastAPI):
    pass

def create_app(settings: Settings):
    settings = settings
    app = FastAPI()

    app.state.settings = settings

    @app.get("/api/health")
    def health(request: Request):
        return {"status": "ok"}

    @app.post("/tickets/extract")
    def extract(email: json):
        #
    
    return app

app = create_app(get_settings)