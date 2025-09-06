from fastapi import Request, Response
from redis import Redis
from sqlalchemy.orm import Session
from repo.interface.Iauth import IAuthRepo
from repo.redis.auth_redis_repo import AuthRedisRepo
from repo.sql.auth_sql_repo import AuthSQLRepo

from infra.fastapi_config.app import app
from infra.fastapi_config.app_state import AppStates, get_app_state

def get_auth_repo(
    request: Request,
    response: Response,
) -> IAuthRepo:
    
    auth_db_client: Redis | Session = get_app_state(app, AppStates.AUTH_DB_CLIENT.value)
    
    if isinstance(auth_db_client, Session):
        return AuthSQLRepo(request, response, auth_db_client)
    
    if isinstance(auth_db_client, Redis):
        return AuthRedisRepo(request, response, auth_db_client)