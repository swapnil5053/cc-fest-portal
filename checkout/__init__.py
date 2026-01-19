from database import get_db

def checkout_logic():
    db = get_db()
    # Query all event fees from the database
    events = db.execute("SELECT fee FROM events").fetchall()
    total = 0
    # Sum up the fees correctly
    for e in events:
        total += e['fee']
    return total
