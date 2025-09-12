from ._router import router
from fastapi import Depends, HTTPException
from app.src.models.schemas.simple.simple_output import SimpleOutput
from app.src.models.schemas.user.user_register_input import UserRegisterInput
from app.src.usecases.auth_user.register_user import RegisterUser
from app.src.routes.http_response.responses import ResponseMessage
from app.src.infra.exception.exceptions import AppBaseException
from app.src.infra.external_api.interface.Iauth import IAuthService 
from app.src.routes.depends.external_api_services_depend import get_auth_service

@router.post(
    "/register",
    response_model=SimpleOutput,
    status_code=201,
    responses={
        **ResponseMessage.HTTP_400_BAD_REQUEST("Email already exists or missing fields"),
        **ResponseMessage.HTTP_500_INTERNAL_SERVER_ERROR("Internal server error"),
    }
)
async def register_user(
    user_data: UserRegisterInput,
    auth_service: IAuthService = Depends(get_auth_service),
) -> SimpleOutput:
    
    try:
        register_user_usecase = RegisterUser(auth_service)    
        return register_user_usecase.execute(user_data)
    except AppBaseException as ex:
        raise HTTPException(status_code=ex.status_code, detail=ex.message)

    