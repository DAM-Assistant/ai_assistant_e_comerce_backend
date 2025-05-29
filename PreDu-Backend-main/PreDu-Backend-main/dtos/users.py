from models import User
from pydantic import BaseModel, EmailStr, constr, Field
from typing import Optional

class UserOutput:
    id: int
    username: str
    firstname: str
    lastname: str
    phone: str
    email: str
    location: str
    role: str
    is_email_verified: bool

    def __init__(self, user: User):
        self.id = user.id
        self.username = user.username
        self.firstname = user.firstname
        self.lastname = user.lastname
        self.phone = user.phone
        self.email = user.email
        self.location = user.location
        self.role = user.role
        self.is_email_verified = user.is_email_verified

class UserSignupInput(BaseModel):
    firstname: constr(min_length=2, max_length=50)
    lastname: constr(min_length=2, max_length=50)
    username: constr(min_length=3, max_length=30)
    password: constr(min_length=8)
    confirm_password: constr(min_length=8)
    phone: constr(pattern=r'^\+?\d{10,15}$')  # Пример: +79991234567
    email: EmailStr
    location: str = Field(..., min_length=2, max_length=100)
        
class UpdateUserInput(BaseModel):
    firstname: Optional[str]
    lastname: Optional[str]
    phone: Optional[str]
    email: Optional[str]
    location: Optional[str]

class UpdateAdminInput(BaseModel):
    firstname: Optional[str]
    lastname: Optional[str]
    phone: Optional[str]
    email: Optional[str]