import base64
import io
import qrcode
from ..database import get_db


def already_registered(username: str, event_id: int) -> bool:
    db = get_db()
    row = db.execute(
        "SELECT 1 FROM registrations WHERE username = ? AND event_id = ?",
        (username, event_id),
    ).fetchone()
    db.close()
    return bool(row)


def register_for_event(username: str, event_id: int):
    db = get_db()
    ticket_code = f"{username}-{event_id}-{int(__import__('time').time())}"
    try:
        cursor = db.execute(
            "INSERT INTO registrations (username, event_id, ticket_code) VALUES (?, ?, ?)",
            (username, event_id, ticket_code),
        )
        db.commit()
        registration_id = cursor.lastrowid
        return registration_id
    except Exception:
        return None
    finally:
        db.close()


def get_user_registrations(username: str):
    db = get_db()
    rows = db.execute(
        "SELECT r.id, r.event_id, e.name, e.fee, e.capacity, r.registered_at, r.ticket_code "
        "FROM registrations r "
        "JOIN events e ON e.id = r.event_id "
        "WHERE r.username = ? ORDER BY r.registered_at DESC",
        (username,),
    ).fetchall()
    db.close()
    return rows


def calculate_checkout_total(username: str):
    db = get_db()
    row = db.execute(
        "SELECT SUM(e.fee) AS total FROM registrations r JOIN events e ON e.id = r.event_id WHERE r.username = ?",
        (username,),
    ).fetchone()
    db.close()
    return row["total"] or 0


def get_registration(registration_id: int, username: str):
    db = get_db()
    row = db.execute(
        "SELECT r.id, r.ticket_code, r.registered_at, e.name, e.description, e.fee "
        "FROM registrations r "
        "JOIN events e ON e.id = r.event_id "
        "WHERE r.id = ? AND r.username = ?",
        (registration_id, username),
    ).fetchone()
    db.close()
    return row


def create_ticket_qr(ticket_data: str) -> str:
    qr = qrcode.QRCode(box_size=4, border=1)
    qr.add_data(ticket_data)
    qr.make(fit=True)
    image = qr.make_image(fill_color="#111827", back_color="white")
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    encoded = base64.b64encode(buffer.getvalue()).decode("utf-8")
    return f"data:image/png;base64,{encoded}"
