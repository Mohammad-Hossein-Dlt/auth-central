from repo.interface.Iauth import IAuthRepo
from routes.api_v1.protected._router import router
from fastapi import Depends, HTTPException
from models.schemas.simple.simple_output import SimpleOutput
from routes.depends.user_repo_depend import get_auth_repo
from usecases.protected.get_protected import GetProtectedResource
from routes.http_response.responses import ResponseMessage
from infra.exception.exceptions import AppBaseException
from infra.external_api.interface.Iauth import IAuthService 
from infra.external_api.interface.Iprotected_resource import IProtectedResourceService 
from routes.depends.external_api_services_depend import get_auth_service, get_protected_resource_service

@router.get(
    "",
    response_model=SimpleOutput,
    status_code=200,
    responses={
        **ResponseMessage.HTTP_401_UNAUTHORIZED("Authentication failed"),
        **ResponseMessage.HTTP_500_INTERNAL_SERVER_ERROR("Internal server error"),
    }
)
async def get_protected_resource(
    protected_resource_service: IProtectedResourceService = Depends(get_protected_resource_service),
    auth_service: IAuthService = Depends(get_auth_service),
    auth_repo: IAuthRepo = Depends(get_auth_repo),
) -> SimpleOutput:
    
    try:
        get_protected_resource_usecase = GetProtectedResource(protected_resource_service, auth_service, auth_repo)    
        return get_protected_resource_usecase.execute()
    except AppBaseException as ex:
        raise HTTPException(status_code=ex.status_code, detail=ex.message)

    