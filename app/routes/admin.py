from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse
from ..core.config import ADMIN_USERNAME, ADMIN_PASSWORD
from ..services.event_service import add_event, delete_event, event_summary
from ..services.admin_service import get_admin_overview

router = APIRouter()


def require_admin(request: Request):
    if request.session.get("admin"):
        return True
    return False


@router.get("/admin/login")
def admin_login_page(request: Request, error: str = ""):
    return request.app.state.templates.TemplateResponse(
        request,
        "admin_login.html",
        {"request": request, "error": error, "title": "Admin Login"},
    )


@router.post("/admin/login")
def admin_login(request: Request, username: str = Form(...), password: str = Form(...)):
    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        request.session["admin"] = True
        request.session.pop("user", None)
        return RedirectResponse("/admin/dashboard", status_code=302)
    return request.app.state.templates.TemplateResponse(
        request,
        "admin_login.html",
        {"request": request, "error": "Invalid admin credentials."},
    )


@router.get("/admin/dashboard")
def admin_dashboard(request: Request, message: str = ""):
    if not require_admin(request):
        return RedirectResponse("/admin/login?error=Sign+in+as+admin")
    overview = get_admin_overview()
    return request.app.state.templates.TemplateResponse(
        request,
        "admin_dashboard.html",
        {
            "request": request,
            "title": "Admin Dashboard",
            "overview": overview,
            "message": message,
        },
    )


@router.post("/admin/events/add")
def admin_add_event(
    request: Request,
    name: str = Form(...),
    description: str = Form(...),
    fee: int = Form(...),
    capacity: int = Form(...),
):
    if not require_admin(request):
        return RedirectResponse("/admin/login?error=Sign+in+as+admin")
    if add_event(name, description, fee, capacity):
        return RedirectResponse("/admin/dashboard?message=Event+added+successfully", status_code=302)
    return request.app.state.templates.TemplateResponse(
        request,
        "admin_dashboard.html",
        {
            "request": request,
            "error": "Unable to add event. Name may already exist.",
            "overview": get_admin_overview(),
        },
    )


@router.post("/admin/events/{event_id}/delete")
def admin_delete_event(request: Request, event_id: int):
    if not require_admin(request):
        return RedirectResponse("/admin/login?error=Sign+in+as+admin")
    delete_event(event_id)
    return RedirectResponse("/admin/dashboard?message=Event+deleted", status_code=302)


@router.get("/admin/logout")
def admin_logout(request: Request):
    request.session.pop("admin", None)
    return RedirectResponse("/admin/login?success=Logged+out", status_code=302)
