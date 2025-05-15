from fastapi import APIRouter, Depends, HTTPException, status, Query
from .... import oauth2, models, schemas


router = APIRouter()

@router.get("/", response_model=schemas.UserOut)
def get_logged_user(user: models.User = Depends(oauth2.get_current_user), current_user: int = Depends(oauth2.get_current_user)):
	try:
		if not current_user.id:
			raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
		return user
	except Exception as e:
		raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
