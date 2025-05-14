from pydantic import BaseModel, EmailStr
from typing import Optional
from uuid import UUID
from datetime import datetime


# AUTH RESPONSE
class Token(BaseModel):
	access_token: str
	token_type: str

# CREATE USER ACCOUNT
class UserCreate(BaseModel):
	email: EmailStr
	username: str
	password: str
	gender: Optional[str] = None
	birth_date: Optional[datetime] = None

# USER INFO RESPONSE
class UserOut(BaseModel):
	id: UUID
	email: EmailStr
	username: str
	role: str
	gender: Optional[str] = None
	birth_date: Optional[datetime] = None
	confirmed: bool
	pending: bool
	deleted: bool
	created_at: datetime
