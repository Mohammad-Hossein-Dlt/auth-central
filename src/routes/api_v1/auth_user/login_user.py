from ._router import router
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from models.schemas.simple.simple_output import SimpleOutput
from models.schemas.user.user_login_input import UserLoginInput
from routes.depends.user_repo_depend import get_auth_repo
from repo.interface.Iauth import IAuthRepo
from usecases.auth_user.login_user import LoginUser
from routes.http_response.responses import ResponseMessage
from infra.exception.exceptions import AppBaseException
from infra.external_api.interface.Iauth import IAuthService
from routes.depends.external_api_services_depend import get_auth_service

@router.post(
    "/login",
    response_model=SimpleOutput,
    status_code=200,
    responses={
        **ResponseMessage.HTTP_401_UNAUTHORIZED("Authentication failed"),
        **ResponseMessage.HTTP_500_INTERNAL_SERVER_ERROR("Internal server error"),
    }
)
async def login_user(
    user_data: OAuth2PasswordRequestForm = Depends(),
    auth_service: IAuthService = Depends(get_auth_service),
    auth_repo: IAuthRepo = Depends(get_auth_repo)
) -> SimpleOutput:
    
    try:
        login_user_usecase = LoginUser(auth_service, auth_repo)    
        return login_user_usecase.execute(UserLoginInput.model_validate(user_data, from_attributes=True))
    except AppBaseException as ex:
        raise HTTPException(status_code=ex.status_code, detail=ex.message)
    