from fastapi import FastAPI, status, Response
from .config import settings
from .api.v1.routes import auth, health, users


app = FastAPI(
	title=settings.APP_NAME,
	description=settings.APP_DESCRIPTION,
	docs_url="/docs/swagger",
	redoc_url="/docs/redoc",
)

@app.get("/", status_code=status.HTTP_200_OK)
async def root():
	return {
		"app_name": "DShare API",
		"description": "DShare is a platform that allows users to share PDF, PPT, and DOC files.",
		"status": "ok",
	}

# API version 1
app.include_router(health.router, prefix="/v1", tags=["Health"])
app.include_router(auth.router, prefix="/v1/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/v1/users", tags=["Users"])
