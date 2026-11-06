from fastapi import FastAPI, Request, HTTPException, Query
from contextlib import asynccontextmanager
from langchain_openai import ChatOpenAI

from .config import get_settings, Settings
from .model import TicketExtractIn, TicketExtracted, TicketExtractOut
from .model import TicketConfirmIn

# Database libs
from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from .database import Base, make_session_factory
from .dependencies import get_db
from .model_db import Email, Ticket, TicketConfirmed

# Min-heap
import heapq
from .algorithm import cal_deadline, cal_priority

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

    app.state.ticket_heap = []

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

    @app.post("/tickets/confirm")
    def confirm(ticket_confirm: TicketConfirmIn, db: Session = Depends(get_db)) -> None:
        if db.get(Ticket, ident=ticket_confirm.id) is None:
            raise HTTPException(status_code=404, detail="Ticket không tồn tại")

        # Contruct ranking key before commit
        received_at = db.get(Email, ticket_confirm.id).received_at
        key = cal_priority(ticket_confirm.id, received_at, ticket_confirm.severity)
        
        try:
            confirmed_row = TicketConfirmed(**ticket_confirm.model_dump())
            db.add(confirmed_row)
            db.commit()
        except IntegrityError:
            db.rollback()
            raise

        heapq.heappush(app.state.ticket_heap, key) # heap push after commit succesfully

    @app.get("/tickets/queue")
    def queue(limit: int = Query(default=10, ge=1)):
        return heapq.nsmallest(limit, app.state.ticket_heap)
        

    return app

app = create_app(get_settings())