from infra.external_api.interface.Iprotected_resource import IProtectedResourceService
from infra.external_api.interface.Iauth import IAuthService
from repo.interface.Iauth import IAuthRepo
from models.schemas.simple.simple_output import SimpleOutput
from domain.schemas.auth.auth_credentials import AuthCredentials
from usecases.auth_user.refresh_token import RefreshToken
from infra.exception.exceptions import AuthenticationException, EntityNotFoundError, OperationFailureException

class GetProtectedResource:
    
    def __init__(
        self,
        protected_service: IProtectedResourceService,
        auth_service: IAuthService,
        auth_repo: IAuthRepo,
    ):
        
        self.protected_resource_service = protected_service
        self.refresh_token_usecase = RefreshToken(auth_service, auth_repo)
        self.auth_repo = auth_repo
        
    def execute(
        self,
    ) -> SimpleOutput:
        
        is_token_refreshed = False
        
        try:
            auth_credentials: AuthCredentials = self.auth_repo.get_user_auth_credentials()
        except Exception:
            raise OperationFailureException(500, "Internal server error")    
        
        if not auth_credentials:
            raise EntityNotFoundError(401, "User is not logged in")
        
        if not auth_credentials.is_access_valid():
            auth_credentials = self.refresh_token_usecase.execute(auth_credentials)
            is_token_refreshed = True
            
        try:
            response = self.protected_resource_service.get_protected_resource(auth_credentials)
        except AuthenticationException:
            auth_credentials = self.refresh_token_usecase.execute(auth_credentials)
            response = self.protected_resource_service.get_protected_resource(auth_credentials)
            
            is_token_refreshed = True
        
        response["token_status"] = "Token refreshed using refresh_token" if is_token_refreshed else "Current access token is valid"
        
        return SimpleOutput.model_validate(response)
        


