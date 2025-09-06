from abc import ABC, abstractmethod
from domain.schemas.auth.auth_credentials import AuthCredentials

class IAuthRepo(ABC):
    
    @abstractmethod
    def save_user_auth_credentials(credentials: AuthCredentials) -> AuthCredentials:
        raise NotImplementedError
    
    @abstractmethod
    def get_user_auth_credentials() -> AuthCredentials | None:
        raise NotImplementedError