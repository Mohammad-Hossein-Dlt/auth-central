from app.src.infra.external_api.interface.Iauth import IAuthService
from app.src.repo.interface.Iauth import IAuthRepo
from app.src.models.schemas.user.user_login_input import UserLoginInput
from app.src.models.schemas.simple.simple_output import SimpleOutput
from app.src.domain.schemas.auth.auth_credentials import AuthCredentials
from app.src.infra.exception.exceptions import OperationFailureException

class LoginUser:
    
    def __init__(
        self,
        auth_service: IAuthService,
        auth_repo: IAuthRepo,
    ):
        
        self.auth_service = auth_service
        self.auth_repo = auth_repo
        
    def execute(
        self,
        user_data: UserLoginInput,
    ) -> SimpleOutput:        
        
        response = self.auth_service.login_user(user_data)
        
        access_token, refresh_token, token_type = response["access_token"], response["refresh_token"], response["token_type"]

        user_auth_credentials = AuthCredentials(
            email=user_data.username,
            access_token=access_token,
            refresh_token=refresh_token,
            token_type=token_type,
        )
                    
        try:
            self.auth_repo.save_user_auth_credentials(user_auth_credentials)
            return SimpleOutput(message="User login was successful")
        except Exception:
            raise OperationFailureException(500, "Internal server error")

