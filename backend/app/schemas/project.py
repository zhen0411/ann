from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None

class ProjectCreate(ProjectBase):
    pass

class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None

class ProjectList(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class ProjectResponse(ProjectList):
    owner_id: int
    updated_at: Optional[datetime] = None

class ProjectUserBase(BaseModel):
    project_id: int
    user_id: int
    role: str

class ProjectUserCreate(ProjectUserBase):
    pass

class ProjectUserResponse(ProjectUserBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True