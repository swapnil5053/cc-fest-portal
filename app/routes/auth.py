from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from ..services.auth_service import register_user, authenticate_user, login_user, logout_user
from ..models.schemas import RegisterForm, LoginForm

router = APIRouter()


@router.get("/register", response_class=HTMLResponse)
def register_page(request: Request):
    return request.app.state.templates.TemplateResponse(
        request,
        "register.html",
        {"request": request, "title": "Create Account", "toast": None},
    )


@router.post("/register")
def register(request: Request, username: str = Form(...), password: str = Form(...)):
    form = RegisterForm(username=username, password=password)
    if register_user(form.username, form.password):
        return RedirectResponse("/login?success=Account+created+successfully", status_code=302)
    return request.app.state.templates.TemplateResponse(
        request,
        "register.html",
        {"request": request, "error": "Username already exists.", "title": "Create Account"},
    )


@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return request.app.state.templates.TemplateResponse(
        request,
        "login.html",
        {"request": request, "title": "Welcome Back", "toast": None, "error": request.query_params.get("error", ""), "success": request.query_params.get("success", "")},
    )


@router.post("/login")
def login(request: Request, username: str = Form(...), password: str = Form(...)):
    form = LoginForm(username=username, password=password)
    user = authenticate_user(form.username, form.password)
    if not user:
        return request.app.state.templates.TemplateResponse(
            request,
            "login.html",
            {"request": request, "error": "Invalid credentials. Try again.", "success": "", "title": "Welcome Back"},
        )
    login_user(request, user)
    return RedirectResponse("/events?success=Logged+in+successfully", status_code=302)


@router.get("/logout")
def logout(request: Request):
    logout_user(request)
    return RedirectResponse("/login?success=Logged+out+successfully", status_code=302)
