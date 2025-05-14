from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from uuid import UUID
from . import schemas, database, models
from .config import settings


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="v1/auth/signin")

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRY

def create_access_token(data: dict):
	to_encode = data.copy()
	if "user_id" in to_encode and isinstance(to_encode["user_id"], UUID):
		to_encode["user_id"] = str(to_encode["user_id"])
	expire = datetime.now(datetime.timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
	to_encode.update({"exp": expire})
	encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
	return encoded_jwt

def verify_access_token(token: str, credentials_exception):
	try:
		payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
		id: str = payload.get("user_id")
		if id is None:
			raise credentials_exception
		token_data = schemas.TokenData(id=id)
	except JWTError:
		raise credentials_exception
	return token_data

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
	try:
		credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
		token = verify_access_token(token, credentials_exception)
		user = db.query(models.User).filter(models.User.id == token.id).first()
		return user
	except Exception as e:
		print(e)
