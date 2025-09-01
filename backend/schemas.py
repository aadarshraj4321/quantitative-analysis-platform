from pydantic import BaseModel, ConfigDict
from uuid import UUID
from typing import Optional, Dict, Any

class JobCreate(BaseModel):
    ticker: str

class Job(BaseModel):
    id: UUID
    ticker: str
    status: str
    result: Optional[Dict[str, Any]] = None

    model_config = ConfigDict(from_attributes=True)