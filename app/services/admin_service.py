from ..database import get_db


def get_admin_overview():
    db = get_db()
    total_registrations = db.execute("SELECT COUNT(*) AS total FROM registrations").fetchone()["total"]
    revenue = db.execute(
        "SELECT COALESCE(SUM(e.fee), 0) AS total FROM registrations r JOIN events e ON e.id = r.event_id"
    ).fetchone()["total"]
    active_users = db.execute(
        "SELECT COUNT(DISTINCT username) AS total FROM registrations"
    ).fetchone()["total"]
    popular_events = db.execute(
        "SELECT e.name, e.fee, e.capacity, COUNT(r.id) AS registrations "
        "FROM events e "
        "LEFT JOIN registrations r ON r.event_id = e.id "
        "GROUP BY e.id ORDER BY registrations DESC, e.name ASC LIMIT 5"
    ).fetchall()
    pending_events = db.execute("SELECT * FROM events ORDER BY created_at DESC").fetchall()
    db.close()
    return {
        "total_registrations": total_registrations,
        "revenue": revenue,
        "active_users": active_users,
        "popular_events": popular_events,
        "events": pending_events,
    }
