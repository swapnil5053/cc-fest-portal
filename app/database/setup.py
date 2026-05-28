import os
from pathlib import Path
from datetime import datetime


def initialize_database():
    from . import get_db

    db_path = Path(os.getenv("DATABASE_PATH", "fest.db"))
    if db_path.exists():
        db = get_db()
        if needs_rebuild(db):
            db.close()
            db_path.unlink()
            db = get_db()
        else:
            db.close()
            db = get_db()
    else:
        db = get_db()

    db.executescript(
        """
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL,
            is_admin INTEGER NOT NULL DEFAULT 0,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            description TEXT NOT NULL DEFAULT '',
            fee INTEGER NOT NULL DEFAULT 0,
            capacity INTEGER NOT NULL DEFAULT 30,
            created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS registrations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            event_id INTEGER NOT NULL,
            registered_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
            ticket_code TEXT NOT NULL UNIQUE,
            FOREIGN KEY(username) REFERENCES users(username) ON DELETE CASCADE,
            FOREIGN KEY(event_id) REFERENCES events(id) ON DELETE CASCADE,
            UNIQUE(username, event_id)
        );
        """
    )
    db.commit()
    seed_default_user(db)
    seed_default_events(db)
    db.close()


def needs_rebuild(db):
    try:
        user_columns = [row[1] for row in db.execute("PRAGMA table_info(users)").fetchall()]
        event_columns = [row[1] for row in db.execute("PRAGMA table_info(events)").fetchall()]
        registration_columns = [row[1] for row in db.execute("PRAGMA table_info(registrations)").fetchall()]

        user_ok = "is_admin" in user_columns and "created_at" in user_columns
        event_ok = "description" in event_columns and "capacity" in event_columns and "created_at" in event_columns
        registration_ok = "ticket_code" in registration_columns and "registered_at" in registration_columns

        return not (user_ok and event_ok and registration_ok)
    except Exception:
        return True


def seed_default_user(db):
    default_password_hash = "$pbkdf2-sha256$29000$MwaA0No7Z.ydM4bQ2lurtQ$9Ys7a8CAp.HUD2InNXXwsO5kLkXp81R6u81sY0U8.vE"
    db.execute(
        "INSERT OR IGNORE INTO users (username, password, is_admin) VALUES (?, ?, 0)",
        ("tester", default_password_hash),
    )
    db.execute(
        "UPDATE users SET password = ? WHERE username = ? AND password = ?",
        (
            default_password_hash,
            "tester",
            "$2b$12$Pb2ZZNY./PJAWD4JFdV44eAtT9QYCRk7WplGAo6t66IiI0nY7Bh3a",
        ),
    )


def seed_default_events(db):
    events = [
        ("Hackathon Sprint", "Build a campus-ready hackathon project.", 500, 40),
        ("Data Science Workshop", "Hands-on machine learning and data techniques.", 400, 25),
        ("Robo Rally", "Design, build and race robots in a timed course.", 450, 20),
        ("Campus Concert", "Live music and open mic under the stars.", 250, 120),
        ("Photography Walk", "Capture campus moments with expert feedback.", 200, 30),
        ("Gaming Tournament", "Fast-paced teams battle for the championship.", 350, 50),
    ]
    for event in events:
        db.execute(
            "INSERT OR IGNORE INTO events (name, description, fee, capacity) VALUES (?, ?, ?, ?)",
            event,
        )
    db.commit()
