import requests
from app.src.infra.external_api.interface.Iprotected_resource import IProtectedResourceService
from app.src.domain.schemas.auth.auth_credentials import AuthCredentials
from app.src.infra.exception.exceptions import AuthenticationException, Error


class ProtectedResourceService(IProtectedResourceService):
    
    def __init__(
        self,
        base_url: str,
    ):
        
        self.base_url = base_url
    
    def get_protected_resource(
        self,
        auth_credentials: AuthCredentials,
    ) -> dict:
        
        target_url = self.base_url + "/protected"
                
        headers = {
            "Authorization": f"{auth_credentials.token_type.title()} {auth_credentials.access_token}"
        }
        
        response = requests.get(target_url, headers=headers)

        if response.status_code == 200:
            return response.json()

        if response.status_code == 401:
            data = response.json()
            detail = data["detail"]
            raise AuthenticationException(response.status_code, detail)
        
        raise Error(500, "An error occurred during getting protected resource")
