from fastapi import FastAPI, Request
from contextlib import asynccontextmanager
from langchain_openai import ChatOpenAI

from .config import get_settings, Settings
from .model import TicketExtractIn, TicketExtracted, TicketExtractOut

@asynccontextmanager
async def lifespan(app: FastAPI):
    pass

def create_app(settings: Settings):
    settings = settings
    app = FastAPI()

    model = ChatOpenAI(model=settings.openai_model, api_key=settings.openai_api_key)
    extractor = model.with_structured_output(TicketExtracted)

    @app.get("/api/health")
    def health():
        return {"status": "ok"}

    @app.post("/tickets/extract")
    def extract(email: TicketExtractIn) -> TicketExtractOut:
        result = extractor.invoke([
            ("system", "Trích xuất thông tin ticket. Không thêm thông tin ngoài tin nhắn."),
            ("human", email.message)
        ])
      
        # return TicketExtractOut(
        #     id=email.id,
        #     received_at=email.received_at,
        #     **result.model_dump(),
        # )

        return TicketExtractOut(
            id=email.id, 
            received_at=email.received_at,
            intent=result.intent,
            severity=result.severity,
            product=result.product,
            summary=result.summary,
            needs_human_review=result.needs_human_review
        )
    
    return app

app = create_app(get_settings())