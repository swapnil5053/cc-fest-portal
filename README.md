# Event Management System

A simple web app for managing college fest events built with FastAPI.

## What it does

- User registration and login
- Browse available events
- Register for events
- View your registered events
- Checkout with total fee calculation

## Setup

Install dependencies:
```bash
pip install -r requirements.txt
```

Initialize the database with some events:
```bash
python insert_events.py
```

Run the server:
```bash
uvicorn main:app --reload
```

Visit `http://localhost:8000/register` to get started.

## Load Testing

Used Locust for performance testing. Run it with:
```bash
locust -f locust/events_locustfile.py
```

Then open `http://localhost:8089` and configure your test parameters.

## Project Structure

- `main.py` - FastAPI routes and app setup
- `database.py` - SQLite database connection
- `checkout/` - Checkout logic module
- `templates/` - HTML templates
- `locust/` - Load testing scripts

## Notes

The app uses SQLite for simplicity. In production you'd want something more robust.
