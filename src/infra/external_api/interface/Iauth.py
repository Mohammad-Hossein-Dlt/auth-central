from abc import ABC, abstractmethod
from models.schemas.user.user_register_input import UserRegisterInput
from models.schemas.user.user_login_input import UserLoginInput
from domain.schemas.auth.auth_credentials import AuthCredentials

class IAuthService(ABC):
    
    @abstractmethod
    def register_user(
        user_data: UserRegisterInput,
    ) -> dict:
    
        raise NotImplementedError
    
    @abstractmethod
    def login_user(
        user_data: UserLoginInput,
    ) -> dict:
    
        raise NotImplementedError
    
    @abstractmethod
    def refresh_token(
        user: AuthCredentials,
    ) -> dict:
        
        raise NotImplementedError