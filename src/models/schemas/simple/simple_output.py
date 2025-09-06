from pydantic import BaseModel, ConfigDict
from typing import Any

class SimpleOutput(BaseModel):
    message: Any
    
    model_config = ConfigDict(
        from_attributes=True,
        extra='allow',
    )