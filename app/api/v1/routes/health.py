from fastapi import APIRouter


router = APIRouter()

@router.get("/")
async def health_check():
	return {
		"app_name": "DShare API",
		"description": "DShare is a platform that allows users to share PDF, PPT, and DOC files.",
		"version": "1.0.0",
		"status": "ok",
	}
