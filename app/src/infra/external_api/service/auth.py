import requests
from app.src.infra.exception.exceptions import AuthenticationException, InvalidRequestException, Error
from app.src.infra.external_api.interface.Iauth import IAuthService
from app.src.models.schemas.user.user_register_input import UserRegisterInput
from app.src.models.schemas.user.user_login_input import UserLoginInput
from app.src.domain.schemas.auth.auth_credentials import AuthCredentials


class AuthService(IAuthService):
    
    def __init__(
        self,
        base_url: str,
    ):
        
        self.base_url = base_url
    
    def register_user(
        self,
        user_data: UserRegisterInput,
    ) -> dict:
        
        target_url = self.base_url + "/register"
        
        response = requests.post(target_url, json=user_data.model_dump())
        
        if response.status_code == 201:
            return response.json()
    
        if response.status_code == 400:
            data = response.json()
            detail = data["detail"]
            raise InvalidRequestException(response.status_code, detail)
        
        raise Error(500, "An error occurred during registering user")
    
    def login_user(
        self,
        user_data: UserLoginInput,
    ) -> dict:
        
        target_url = self.base_url + "/login"
        
        response = requests.post(target_url, data=user_data.model_dump())
        
        if response.status_code == 200:
            return response.json()
    
        if response.status_code == 401:
            data = response.json()
            detail = data["detail"]
            raise AuthenticationException(response.status_code, detail)
        
        raise Error(500, "An error occurred during logging in user")
    
    def refresh_token(
        self,
        auth_credentials: AuthCredentials,
    ) -> dict:
        
        target_url = self.base_url + "/refresh"
        
        payload = {
            "refresh_token": auth_credentials.refresh_token,
        }
        
        response = requests.post(target_url, json=payload)
        
        if response.status_code == 200:
            return response.json()
        
        if response.status_code == 401:
            data = response.json()
            detail = data["detail"]
            raise AuthenticationException(response.status_code, detail)
                
        raise Error(500, "An error occurred during refresh token")