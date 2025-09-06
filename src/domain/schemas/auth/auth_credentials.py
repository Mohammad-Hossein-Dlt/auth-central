from pydantic import BaseModel, ConfigDict
from datetime import datetime, timezone, timedelta

class AuthCredentials(BaseModel):
    id: int | None = None
    device_id: str | None = None
    email: str | None = None
    access_token: str | None = None
    access_expiry: datetime | None = None
    refresh_token: str | None = None
    refresh_expiry: datetime | None = None
    token_type: str | None = None
    
    model_config = ConfigDict(
        extra='ignore',
    )
    
    def is_access_valid(self) -> bool:
        now = datetime.now(timezone.utc)
        return now.time() < self.access_expiry.time()
    
    def is_refresh_valid(self) -> bool:
        now = datetime.now(timezone.utc)
        return now.time() < self.refresh_expiry.time()