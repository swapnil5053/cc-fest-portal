from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
from .core.config import SECRET_KEY
from .database.setup import initialize_database
from .routes.auth import router as auth_router
from .routes.events import router as events_router
from .routes.admin import router as admin_router

app = FastAPI(title="CC Fest Portal", description="Modern event management for college fest organizers.")
app.add_middleware(SessionMiddleware, secret_key=SECRET_KEY, max_age=86400, session_cookie="fest_session")
app.mount("/static", StaticFiles(directory="static"), name="static")
app.state.templates = Jinja2Templates(directory="templates")
app.include_router(auth_router)
app.include_router(events_router)
app.include_router(admin_router)


@app.on_event("startup")
def startup_event():
    initialize_database()


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return app.state.templates.TemplateResponse(
        request,
        "error.html",
        {
            "request": request,
            "detail": str(exc),
            "status_code": 500,
            "user": request.session.get("user", ""),
        },
        status_code=500,
    )
