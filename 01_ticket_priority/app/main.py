from fastapi import FastAPI, Request
from contextlib import asynccontextmanager
from langchain_openai import ChatOpenAI

from .config import get_settings, Settings
from .model import TicketExtractIn, TicketExtracted

@asynccontextmanager
async def lifespan(app: FastAPI):
    pass

def create_app(settings: Settings):
    settings = settings
    app = FastAPI()
    app.state.settings = settings

    model = ChatOpenAI(model=settings.openai_model, api_key=settings.openai_api_key)
    extractor = model.with_structured_output(TicketExtracted)

    @app.get("/api/health")
    def health(request: Request):
        return {"status": "ok"}

    @app.post("/tickets/extract")
    def extract(email: TicketExtractIn) -> TicketExtracted:
        result = extractor.invoke(email.message)
        return result
    
    return app

app = create_app(get_settings())