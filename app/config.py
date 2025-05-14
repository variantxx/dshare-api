from pydantic_settings import BaseSettings


class Settings(BaseSettings):
	APP_NAME: str
	APP_DESCRIPTION: str
	APP_AUTHOR: str

	# Database settings
	DATABASE_URL: str
	
	# JWT
	SECRET_KEY: str
	ALGORITHM: str
	ACCESS_TOKEN_EXPIRY: int    # In seconds

	# SMTP
	SMTP_SERVER: str
	SMTP_PORT: int
	SMTP_USERNAME: str
	SMTP_PASSWORD: str

	class Config:
		env_file = ".env"

settings = Settings()
