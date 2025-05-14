from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .... import schemas, models, utils, oauth2
from ....database import get_db


router = APIRouter()

@router.post("/signin", response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
	user = db.query(models.User).filter(
		models.User.email == user_credentials.username).first()
	if not user or not utils.verify(user_credentials.password, user.password):
		try:
			db.add(models.UnauthLoginAttempts())
			db.commit()
		except Exception as e:
			raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
		raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
	try:
		access_token = oauth2.create_access_token(data={"user_id": user.id})
		log_entry = models.Logs(user_id=user.id)
		db.add(log_entry)
		db.commit()
		db.refresh(log_entry)
		return {"access_token": access_token, "token_type": "bearer"}
	except Exception as e:
		raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
