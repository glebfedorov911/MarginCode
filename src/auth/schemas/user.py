import uuid

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    login: str
    email: EmailStr
    is_staff: bool
    is_active: bool

class UserCreate(UserBase):
    password_for_create_user: str
    password: str

class UserRead(UserBase):
    id: uuid.UUID

class UserAuth(BaseModel):
    login: str
    password: str