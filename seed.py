from app.database.setup import initialize_database

if __name__ == "__main__":
    initialize_database()
    print("✅ Database created and seeded with default users and events.")
