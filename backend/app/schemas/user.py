from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from app.core.database import UserRole

class UserBase(BaseModel):
    username: str
    email: EmailStr
    role: UserRole

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    role: Optional[UserRole] = None
    is_active: Optional[bool] = None

class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class UserList(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: UserRole
    is_active: bool
    
    class Config:
        from_attributes = True