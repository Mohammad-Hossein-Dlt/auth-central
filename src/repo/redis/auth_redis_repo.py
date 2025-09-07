from repo.interface.Iauth import IAuthRepo
from fastapi import Request, Response
from redis import Redis
from domain.schemas.auth.auth_credentials import AuthCredentials
import uuid

class AuthRedisRepo(IAuthRepo):
    
    def __init__(self, request: Request, response: Response, redis_client: Redis):
        self.request = request
        self.response = response   
        self.redis_client = redis_client
        
    def save_user_auth_credentials(self, credentials: AuthCredentials) -> AuthCredentials:
                
        device_id = None
        
        existing_credentials = self.get_user_auth_credentials()   
        
        if existing_credentials:
            device_id = existing_credentials.device_id
        else:
            device_id = credentials.device_id or uuid.uuid4().hex        
        
        credentials.device_id = device_id
        
        self.redis_client.hset(
            name=device_id,
            mapping={
                "email": credentials.email,
                "access_token": credentials.access_token,
                "access_expiry": str(credentials.access_expiry),
                "refresh_token": credentials.refresh_token,
                "refresh_expiry": str(credentials.refresh_expiry),
                "token_type": credentials.token_type,
            },
        )
        
        self.redis_client.expire(device_id, credentials.refresh_lifetime * 60)
        
        self.request.session["device_id"] = device_id
                                
        return credentials

    def get_user_auth_credentials(self) -> AuthCredentials | None:
        
        device_id = self.request.session.get("device_id")
                
        existing_credentials = self.redis_client.hgetall(device_id) if device_id else None
        
        if not existing_credentials:
            return None
        
        existing_credentials = {k.decode(): v.decode() for k, v in existing_credentials.items()}
                
        auth_credentials = AuthCredentials.model_validate(existing_credentials)
        
        auth_credentials.device_id = device_id
                
        return auth_credentials
    