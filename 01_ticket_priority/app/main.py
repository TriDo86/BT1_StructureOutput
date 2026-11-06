from fastapi import FastAPI, Request
from contextlib import asynccontextmanager
from langchain_openai import ChatOpenAI

from .config import get_settings, Settings
from .model import TicketExtractIn, TicketExtracted, TicketExtractOut

# Database libs
from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from .database import Base, make_session_factory
from .dependencies import get_db
from .model_db import Email, Ticket

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(app.state.engine)
    yield
    app.state.engine.dispose() # Mỗi lần start app -> refresh session với DB 1 lần

def create_app(settings: Settings):
    settings = settings
    app = FastAPI(lifespan=lifespan)
    app.state.settings = settings

    engine, session_factory = make_session_factory(database_url=settings.database_url)
    app.state.engine = engine
    app.state.session_factory = session_factory

    model = ChatOpenAI(model=settings.openai_model, api_key=settings.openai_api_key)
    extractor = model.with_structured_output(TicketExtracted)

    @app.get("/api/health")
    def health():
        return {"status": "ok"}

    @app.post("/tickets/extract")
    def extract(email: TicketExtractIn, db: Session = Depends(get_db)) -> TicketExtractOut:
        result = extractor.invoke([
            ("system", "Trích xuất thông tin ticket. Không thêm thông tin ngoài tin nhắn."),
            ("human", email.message)
        ])

        ticket_extracted = TicketExtractOut(
            id=email.id, 
            received_at=email.received_at,
            intent=result.intent,
            severity=result.severity,
            product=result.product,
            summary=result.summary,
            needs_human_review=result.needs_human_review
        )

        try:
            email_row = Email(id=email.id, received_at=email.received_at, message=email.message)
            ticket_row = Ticket(id=email.id, 
                                intent=result.intent,
                                severity=result.severity,
                                product=result.product,
                                summary=result.summary,
                                needs_human_review=result.needs_human_review)

            db.add(email_row)
            db.flush() # why
            db.add(ticket_row)
            db.commit()
        except IntegrityError:
            db.rollback()
            raise

        return ticket_extracted
    
    return app

app = create_app(get_settings())