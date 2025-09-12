from app.src.infra.fastapi_config.app import app
from app.src.routes.api_v1.main_router import main_router_v1


app.include_router(main_router_v1)
