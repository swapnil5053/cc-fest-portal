from ..database import get_db


def list_events(search: str = ""):
    db = get_db()
    if search:
        search_value = f"%{search.strip().lower()}%"
        rows = db.execute(
            "SELECT e.*, COALESCE((SELECT COUNT(*) FROM registrations r WHERE r.event_id = e.id), 0) AS signed_up "
            "FROM events e "
            "WHERE LOWER(e.name) LIKE ? OR LOWER(e.description) LIKE ? "
            "ORDER BY signed_up DESC, e.capacity DESC, e.fee DESC",
            (search_value, search_value),
        ).fetchall()
    else:
        rows = db.execute(
            "SELECT e.*, COALESCE((SELECT COUNT(*) FROM registrations r WHERE r.event_id = e.id), 0) AS signed_up "
            "FROM events e ORDER BY signed_up DESC, e.created_at DESC"
        ).fetchall()
    db.close()
    return rows


def get_event(event_id: int):
    db = get_db()
    event = db.execute("SELECT * FROM events WHERE id = ?", (event_id,)).fetchone()
    db.close()
    return event


def add_event(name: str, description: str, fee: int, capacity: int) -> bool:
    db = get_db()
    try:
        db.execute(
            "INSERT INTO events (name, description, fee, capacity) VALUES (?, ?, ?, ?)",
            (name.strip(), description.strip(), fee, capacity),
        )
        db.commit()
        return True
    except Exception:
        return False
    finally:
        db.close()


def delete_event(event_id: int):
    db = get_db()
    db.execute("DELETE FROM events WHERE id = ?", (event_id,))
    db.commit()
    db.close()


def available_seats(event_id: int):
    db = get_db()
    event = db.execute("SELECT capacity FROM events WHERE id = ?", (event_id,)).fetchone()
    if not event:
        db.close()
        return 0
    count = db.execute(
        "SELECT COUNT(*) AS total FROM registrations WHERE event_id = ?",
        (event_id,),
    ).fetchone()["total"]
    db.close()
    return max(0, event["capacity"] - count)


def event_summary():
    db = get_db()
    stats = db.execute(
        "SELECT id, name, fee, capacity, "
        "(SELECT COUNT(*) FROM registrations WHERE event_id = events.id) AS signed_up "
        "FROM events ORDER BY signed_up DESC, name ASC"
    ).fetchall()
    db.close()
    return stats
