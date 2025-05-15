import random
import string
from fastapi import APIRouter, Depends, Request, status, HTTPException, Query
from slowapi import Limiter
from slowapi.util import get_remote_address
from sqlalchemy.orm import Session
from sqlalchemy.orm import Session
from .... import schemas, models, utils
from ....database import get_db


router = APIRouter()
limiter = Limiter(key_func=get_remote_address)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.SignupOut)
@limiter.limit("5/minute")
async def save_user(request: Request, body: schemas.UserCreate, db: Session = Depends(get_db)):
	try:
		hashed_password = utils.hash(body.password)
		body.gender = body.gender.lower()
		body.password = hashed_password
		user_data = body.model_dump()
		verif_code = utils.gen_verif_code()
		user_data["verif_code"] = verif_code
		new_user = models.User(**user_data)
		db.add(new_user)
		db.commit()
		db.refresh(new_user)
		await utils.send_email_verification(body.username, body.email, verif_code)
		return new_user
	except Exception as e:
		raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@router.get("/", response_model=list[schemas.UserOut])
@limiter.limit("10/minute")
def get_users(request: Request, db: Session=Depends(get_db), filter: str=Query("all", enum=schemas.roles)):
	try:
		query = db.query(models.User)
		if filter != "all":
			query = query.filter(models.User.role == filter).order_by(models.User.username)
		users = query.order_by(models.User.username).all()
		return users
	except Exception as e:
		raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

