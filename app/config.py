from pydantic_settings import BaseSettings


class Settings(BaseSettings):
	APP_NAME: str
	APP_DESCRIPTION: str
	APP_AUTHOR: str
	
	# Seerver API key
	SERVER_API_KEY: str

	# Database settings
	DATABASE_URL: str

	# SUPABASE
	SUPABASE_URL: str
	SUPABASE_API_KEY: str
	
	# JWT
	SECRET_KEY: str
	ALGORITHM: str
	ACCESS_TOKEN_EXPIRY: int

	# SMTP
	SMTP_SERVER: str
	SMTP_PORT: int
	SMTP_USERNAME: str
	SMTP_PASSWORD: str

	class Config:
		env_file = ".env"

settings = Settings()
