from fastapi import APIRouter, Depends, HTTPException, Request, status, Query
from slowapi import Limiter
from slowapi.util import get_remote_address
from .... import oauth2, models, schemas


router = APIRouter()
limiter = Limiter(key_func=get_remote_address)

@router.get("/", response_model=schemas.UserOut)
@limiter.limit("10/minute")
def get_logged_user(request: Request, user: models.User = Depends(oauth2.get_current_user), current_user: int = Depends(oauth2.get_current_user)):
	try:
		if not current_user.id:
			raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
		return user
	except Exception as e:
		raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
