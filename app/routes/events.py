from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from ..services.auth_service import get_current_user
from ..services.event_service import list_events, get_event, available_seats
from ..services.registration_service import (
    already_registered,
    register_for_event,
    get_user_registrations,
    calculate_checkout_total,
    get_registration,
    create_ticket_qr,
)

router = APIRouter()


def require_user(request: Request):
    user = get_current_user(request)
    if not user:
        return None
    return user


@router.get("/", response_class=None)
def home(request: Request):
    if get_current_user(request):
        return RedirectResponse("/events")
    return RedirectResponse("/login")


@router.get("/events")
def events(request: Request, q: str = "", success: str = "", error: str = ""):
    user = require_user(request)
    if not user:
        return RedirectResponse("/login?error=Please+login+first")
    rows = list_events(q)
    registration_rows = get_user_registrations(user)
    registered_event_ids = {row["event_id"] for row in registration_rows}
    return request.app.state.templates.TemplateResponse(
        request,
        "events.html",
        {
            "request": request,
            "events": rows,
            "user": user,
            "query": q,
            "registered_ids": registered_event_ids,
            "success": success,
            "error": error,
        },
    )


@router.get("/events/{event_id}/register")
def register_event(request: Request, event_id: int):
    user = require_user(request)
    if not user:
        return RedirectResponse("/login?error=Please+login+first")
    event = get_event(event_id)
    if not event:
        return RedirectResponse("/events?error=Event+not+found")
    if already_registered(user, event_id):
        return RedirectResponse("/events?error=Already+registered+for+this+event")
    if available_seats(event_id) <= 0:
        return RedirectResponse("/events?error=This+event+is+sold+out")
    registration_id = register_for_event(user, event_id)
    if not registration_id:
        return RedirectResponse("/events?error=Could+not+register+for+this+event")
    return RedirectResponse(f"/tickets/{registration_id}", status_code=302)


@router.get("/my-events")
def my_events(request: Request, success: str = "", error: str = ""):
    user = require_user(request)
    if not user:
        return RedirectResponse("/login?error=Please+login+first")
    rows = get_user_registrations(user)
    total = calculate_checkout_total(user)
    return request.app.state.templates.TemplateResponse(
        request,
        "my_events.html",
        {
            "request": request,
            "events": rows,
            "user": user,
            "total": total,
            "success": success,
            "error": error,
        },
    )


@router.get("/checkout")
def checkout(request: Request):
    user = require_user(request)
    if not user:
        return RedirectResponse("/login?error=Please+login+first")
    total = calculate_checkout_total(user)
    return request.app.state.templates.TemplateResponse(
        request,
        "checkout.html",
        {"request": request, "user": user, "total": total},
    )


@router.get("/tickets/{registration_id}")
def ticket_page(request: Request, registration_id: int):
    user = require_user(request)
    if not user:
        return RedirectResponse("/login?error=Please+login+first")
    registration = get_registration(registration_id, user)
    if not registration:
        return RedirectResponse("/my-events?error=Ticket+not+found")
    qr_image = create_ticket_qr(registration["ticket_code"])
    return request.app.state.templates.TemplateResponse(
        request,
        "ticket.html",
        {
            "request": request,
            "user": user,
            "ticket": registration,
            "qr_image": qr_image,
        },
    )
