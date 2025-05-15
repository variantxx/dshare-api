from fastapi import APIRouter, Depends, status, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy.orm import Session
from .... import schemas, models, utils
from ....database import get_db


router = APIRouter()

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
async def save_user(body: schemas.UserCreate, db: Session = Depends(get_db)):
	plain_password = body.password
	hashed_password = utils.hash(body.password)
	# Convert to lowercase.
	body.role = body.role.lower()
	body.gender = body.gender.lower()
	body.password = hashed_password
	new_user = models.User(**body.model_dump())
	db.add(new_user)
	db.commit()
	db.refresh(new_user)
	if body.role.lower() == "stylist":
		utils.send_email(body.username, plain_password, body.email)
	return new_user

@router.get("/", response_model=list[schemas.UserOut])
def get_users(db: Session=Depends(get_db), filter: str=Query("all", enum=schemas.roles)):
    try:
        query = db.query(models.User)
        if filter != "all":
            query = query.filter(models.User.role == filter).order_by(models.User.username)
        users = query.order_by(models.User.username).all()
        return users
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
