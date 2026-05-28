import sqlite3
from passlib.context import CryptContext
from passlib.exc import UnknownHashError
from fastapi import Request
from ..database import get_db

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    try:
        return pwd_context.verify(password, hashed_password)
    except (ValueError, UnknownHashError):
        return False


def register_user(username: str, password: str) -> bool:
    db = get_db()
    try:
        db.execute(
            "INSERT INTO users (username, password, is_admin) VALUES (?, ?, 0)",
            (username, hash_password(password)),
        )
        db.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        db.close()


def authenticate_user(username: str, password: str):
    db = get_db()
    user = db.execute(
        "SELECT username, password FROM users WHERE username = ?",
        (username,),
    ).fetchone()
    db.close()
    if not user:
        return None
    if verify_password(password, user["password"]):
        return user["username"]
    return None


def get_current_user(request: Request):
    return request.session.get("user")


def login_user(request: Request, username: str):
    request.session["user"] = username
    request.session.pop("admin", None)


def logout_user(request: Request):
    request.session.clear()
