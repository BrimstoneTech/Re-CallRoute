from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime
from .models import UserRole, PersonnelStatus

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

class UserBase(BaseModel):
    username: str
    role: UserRole

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool
    model_config = ConfigDict(from_attributes=True)

class RoleBase(BaseModel):
    name: str
    description: Optional[str] = None

class RoleCreate(RoleBase):
    pass

class Role(RoleBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class PersonnelBase(BaseModel):
    name: str
    extension: str
    role_id: int
    status: PersonnelStatus = PersonnelStatus.AVAILABLE

class PersonnelCreate(PersonnelBase):
    pass

class Personnel(PersonnelBase):
    id: int
    ip_address: Optional[str] = None
    last_seen: datetime
    model_config = ConfigDict(from_attributes=True)

class CallLogBase(BaseModel):
    caller_id: str
    recipient_id: int
    status: str
    redirection_details: Optional[str] = None

class CallLog(CallLogBase):
    id: int
    timestamp: datetime
    duration_seconds: Optional[int] = None
    model_config = ConfigDict(from_attributes=True)
