from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from redis import Redis
from flask import current_app

# Instantiate extensions (no app bound yet)
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

redis_client: Redis | None = None

def init_redis(app):
    global redis_client
    url = app.config.get("REDIS_URL")
    if url:
        redis_client = Redis.from_url(url, decode_responses=True)
    else:
        redis_client = Redis(host="localhost", port=6379, db=0, decode_responses=True)
    return redis_client
