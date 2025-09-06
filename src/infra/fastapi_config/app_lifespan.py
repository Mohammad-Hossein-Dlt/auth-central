from fastapi import FastAPI
from infra.settings.settings import settings
from contextlib import asynccontextmanager
from .app_state import AppStates, set_app_state
from infra.db.redis.client import init_redis_client
from infra.db.sql.database import init_sqlite_client, create_sqlite_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    
    sql_client, engine = init_sqlite_client(sqlite_url="sqlite:///./database.db")
    
    redis_client = init_redis_client(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        password=settings.REDIS_PASSWORD,
    )
    
    if settings.AUTH_DB_STACK == "sqlite":
        create_sqlite_db(engine)
        set_app_state(app, AppStates.AUTH_DB_CLIENT.value, sql_client)
        
    if settings.AUTH_DB_STACK == "redis":
        set_app_state(app, AppStates.AUTH_DB_CLIENT.value, redis_client)
    
    set_app_state(app, AppStates.AUTH_BASE_URL.value, settings.BASE_URL)
        
    yield
    
    sql_client.close()
    redis_client.close()
    
