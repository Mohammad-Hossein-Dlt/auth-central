from pydantic import BaseModel, ConfigDict, model_validator
from typing import ClassVar
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
    
    access_lifetime: ClassVar[int] = 2  # in minutes
    refresh_lifetime: ClassVar[int] = 4  # in minutes
    
    
    model_config = ConfigDict(
        extra='ignore',
    )
    
    @model_validator(mode='before')
    def __set_default_expiry(
        cls,
        values: dict,
    ) -> dict:
        
        now: datetime = datetime.now(timezone.utc)
        
        if values.get('access_expiry') is None:
            values['access_expiry'] = now + timedelta(minutes=cls.access_lifetime)
            
        if values.get('refresh_expiry') is None:
            values['refresh_expiry'] = now + timedelta(minutes=cls.refresh_lifetime)
            
        return values
    
    def set_new_expiries(
        self,
    ) -> bool:        
        
        now: datetime = datetime.now(timezone.utc)
        
        self.access_expiry = now + timedelta(minutes=self.access_lifetime)
        self.refresh_expiry = now + timedelta(minutes=self.refresh_lifetime)
    
    def is_access_valid(
        self,
    ) -> bool:
        
        now = datetime.now(timezone.utc)
        return now < self.access_expiry.astimezone(timezone.utc)
    
    def is_refresh_valid(
        self,
    ) -> bool:
    
        now = datetime.now(timezone.utc)
        return now < self.refresh_expiry.astimezone(timezone.utc)