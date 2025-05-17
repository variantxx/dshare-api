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
	gender: Optional[str] = None
	birth_date: Optional[datetime] = None

# USER EMAIL VERIFICATION
class EmailVerification(BaseModel):
	email: EmailStr
	code: str

# USER INFO RESPONSE
class UserOut(BaseModel):
	id: UUID
	email: EmailStr
	username: str
	gender: Optional[str] = None
	birth_date: Optional[datetime] = None

# USER SIGNUP RESPONSE
class SignupOut(BaseModel):
	id: UUID
	email: EmailStr
	username: str
	gender: Optional[str] = None
	verif_code: str
	birth_date: Optional[datetime] = None

# UPLOAD FILE RESPONSE
class UploadFileResponse(BaseModel):
	thumbnail_url: str
	file_url: str
	hash: str

