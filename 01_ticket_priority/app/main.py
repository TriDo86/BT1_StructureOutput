from .config import get_settings, Settings

from fastapi import FastAPI, Request
from contextlib import asynccontextmanager

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
    
    return app

app = create_app(get_settings)