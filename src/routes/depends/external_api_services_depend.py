from infra.fastapi_config.app import app
from infra.fastapi_config.app_state import AppStates, get_app_state

from infra.external_api.interface.Iauth import IAuthService
from infra.external_api.service.auth import AuthService

from infra.external_api.interface.Iprotected_resource import IProtectedResourceService
from infra.external_api.service.protected_resource import ProtectedResourceService

def get_auth_service() -> IAuthService:
    base_url = get_app_state(app, AppStates.AUTH_BASE_URL.value)
    return AuthService(base_url)

def get_protected_resource_service() -> IProtectedResourceService:
    base_url = get_app_state(app, AppStates.AUTH_BASE_URL.value)
    return ProtectedResourceService(base_url)