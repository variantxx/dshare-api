from fastapi import APIRouter, Request
from slowapi import Limiter
from slowapi.util import get_remote_address
from ....config import settings


router = APIRouter()
limiter = Limiter(key_func=get_remote_address)

@router.get("/")
@limiter.limit("10/minute")
async def health_check(request: Request):
	return {
		"app_name": settings.APP_NAME,
		"description": settings.APP_DESCRIPTION,
		"version": "1.0.0",
		"status": "ok",
	}
