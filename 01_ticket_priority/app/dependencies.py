from fastapi import Request

def get_db(request: Request): # Not understand yet
    with request.app.state.session_factory() as db:
        yield db