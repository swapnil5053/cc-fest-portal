import sqlite3
from .setup import initialize_database
from ..core.config import DATABASE_PATH


def get_db():
    connection = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection
