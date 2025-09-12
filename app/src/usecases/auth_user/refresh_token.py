from app.src.infra.external_api.interface.Iauth import IAuthService
from app.src.repo.interface.Iauth import IAuthRepo
from app.src.domain.schemas.auth.auth_credentials import AuthCredentials
from app.src.infra.exception.exceptions import TokenExpiredException, OperationFailureException

class RefreshToken:
    
    def __init__(
        self,
        auth_service: IAuthService,
        auth_repo: IAuthRepo,
    ):
        
        self.auth_service = auth_service
        self.auth_repo = auth_repo
        
    def execute(
        self,
        auth_credentials: AuthCredentials,
    ) -> AuthCredentials:
        
        if not auth_credentials.is_refresh_valid():
            raise TokenExpiredException(401, "Refresh token expired. Please login again")

        response = self.auth_service.refresh_token(auth_credentials)
        
        access_token, refresh_token = response["access_token"], response["refresh_token"]
        
        auth_credentials.access_token = access_token        
        auth_credentials.refresh_token = refresh_token
        
        auth_credentials.set_new_lifetime()
        
        try:
            return self.auth_repo.save_user_auth_credentials(auth_credentials)
        except Exception:
            raise OperationFailureException(500, "Internal server error")



