from pydantic import BaseModel, EmailStr
from typing import Optional
from uuid import UUID
from datetime import datetime


roles = ["user", "admin", "super"]

# AUTH RESPONSE
class Token(BaseModel):
	access_token: str
	token_type: str

class TokenData(BaseModel):
	id: Optional[str] = None

# CREATE USER ACCOUNT
class UserCreate(BaseModel):
	email: EmailStr
	username: str
	password: str
	role: Optional[str] = "user"
	gender: Optional[str] = None
	birth_date: Optional[datetime] = None

# USER INFO RESPONSE
class UserOut(BaseModel):
	id: UUID
	email: EmailStr
	username: str
	gender: Optional[str] = None
	birth_date: Optional[datetime] = None
