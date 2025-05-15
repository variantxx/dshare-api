from fastapi import APIRouter, Depends, Request, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from slowapi import Limiter
from slowapi.util import get_remote_address
from .... import schemas, models, utils, oauth2
from ....database import get_db


router = APIRouter()
limiter = Limiter(key_func=get_remote_address)

@router.post("/signin", response_model=schemas.Token)
@limiter.limit("5/minute")
def login(request: Request, user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
	user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
	if not user or not utils.verify(user_credentials.password, user.password):
		raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
	access_token = oauth2.create_access_token(data={"user_id": user.id})
	return {"access_token": access_token, "token_type": "bearer"}

@router.post("/confirm-email", status_code=status.HTTP_200_OK)
@limiter.limit("5/minute")
async def confirm_email(request: Request, body: schemas.EmailVerification, db: Session = Depends(get_db)):
	user = db.query(models.User).filter(models.User.email == body.email).first()
	if not user:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
	user.confirmed = True
	db.commit()
	return {"message": "Email confirmed successfully"}

