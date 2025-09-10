from infra.external_api.interface.Iauth import IAuthService
from models.schemas.user.user_register_input import UserRegisterInput
from models.schemas.simple.simple_output import SimpleOutput

class RegisterUser:
    
    def __init__(
        self,
        auth_service: IAuthService,
    ):
        
        self.auth_service = auth_service
            
    def execute(
        self,
        user_data: UserRegisterInput,
    ) -> SimpleOutput:
        
        response = self.auth_service.register_user(user_data)
        
        return SimpleOutput.model_validate(response)