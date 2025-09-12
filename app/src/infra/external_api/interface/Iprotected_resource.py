from abc import ABC, abstractmethod
from app.src.domain.schemas.auth.auth_credentials import AuthCredentials

class IProtectedResourceService(ABC):
    
    @abstractmethod
    def get_protected_resource(
        auth_credentials: AuthCredentials,
    ) -> dict:
     
        raise NotImplementedError
    