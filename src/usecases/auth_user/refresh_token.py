from infra.external_api.interface.Iauth import IAuthService
from repo.interface.Iauth import IAuthRepo
from domain.schemas.auth.auth_credentials import AuthCredentials
from infra.exception.exceptions import TokenExpiredException, OperationFailureException
from datetime import datetime, timezone, timedelta

class RefreshToken:
    
    def __init__(self, auth_service: IAuthService, auth_repo: IAuthRepo):
        self.auth_service = auth_service
        self.auth_repo = auth_repo
        
    def execute(self, auth_credentials: AuthCredentials) -> AuthCredentials:
        
        if not auth_credentials.is_refresh_valid():
            raise TokenExpiredException(401, "Refresh token expired. Please login again")

        response = self.auth_service.refresh_token(auth_credentials)
        
        access_token, refresh_token = response["access_token"], response["refresh_token"]
        
        now = datetime.now(timezone.utc)
        access_expiry = now + timedelta(minutes=2)
        refresh_expiry = now + timedelta(minutes=4)
        
        auth_credentials.access_token = access_token
        auth_credentials.access_expiry = access_expiry
        
        auth_credentials.refresh_token = refresh_token
        auth_credentials.refresh_expiry = refresh_expiry
        
        try:
            return self.auth_repo.save_user_auth_credentials(auth_credentials)
        except Exception:
            raise OperationFailureException(500, "Internal server error")



