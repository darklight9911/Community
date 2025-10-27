# Community API (Flask)

A scalable, modular community backend built with Flask, PostgreSQL, SQLAlchemy, JWT auth, and Redis.

## Features
- Application Factory pattern
- Blueprints for modular APIs: auth, posts, doubts, comments, votes, reports
- PostgreSQL via SQLAlchemy and migrations with Flask-Migrate
- JWT authentication (access/refresh)
- Redis for vote counters

## Quickstart

1. Create and activate a virtualenv (optional).
2. Install dependencies.
3. Set environment variables in `.env` or your shell.
4. Initialize the database and run the server.

### Environment
Copy `.env` and update values as needed:

- DATABASE_URL
- REDIS_URL
- JWT_SECRET_KEY

### Flask CLI

This app uses an application factory. Set `FLASK_APP=run.py`.

### Migrations

- Initialize: `flask db init`
- Generate: `flask db migrate -m "init"`
- Apply: `flask db upgrade`

### Run

- Development: `python run.py`
- Production (example): `gunicorn -b 0.0.0.0:8000 run:app`

## Notes
- Votes are tracked in Redis via HINCRBY for atomic counters.
- Consider a periodic sync job if you want to persist aggregated vote counts back to PostgreSQL.
