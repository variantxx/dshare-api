from fastapi import Depends, FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from .api.v1.routes import auth, me, health, users
from .database import engine
from .config import settings
from . import models
from .utils import api_key_auth


# Initialize the database
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
	title=settings.APP_NAME,
	description=settings.APP_DESCRIPTION,
	docs_url="/docs/swagger",
	redoc_url="/docs/redoc",
)

# Middleware for CORS
app.add_middleware(
	CORSMiddleware,
	allow_origins=[
      "http://localhost:8000",
   ],
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)

# API version 1
app.include_router(health.router, prefix="/v1", tags=["Health"], dependencies=[Depends(api_key_auth)])
app.include_router(auth.router, prefix="/v1/auth", tags=["Authentication"])
app.include_router(me.router, prefix="/v1/me", tags=["Logged User"], dependencies=[Depends(api_key_auth)])
app.include_router(users.router, prefix="/v1/users", tags=["Users"], dependencies=[Depends(api_key_auth)])
