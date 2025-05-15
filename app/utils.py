import random
import string
import uuid
from fastapi import HTTPException, Header, Security, UploadFile, status
from fastapi.security import APIKeyHeader
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema
from passlib.context import CryptContext
from .config import settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

conf = ConnectionConfig(
	MAIL_USERNAME = settings.SMTP_USERNAME,
	MAIL_PASSWORD = settings.SMTP_PASSWORD,
	MAIL_FROM = settings.SMTP_USERNAME,
	MAIL_PORT = settings.SMTP_PORT,
	MAIL_SERVER = settings.SMTP_SERVER,
	MAIL_STARTTLS = True,
	MAIL_SSL_TLS = False
)

def hash(password: str):
	return pwd_context.hash(password)

def verify(plain_password, hashed_password):
	return pwd_context.verify(plain_password, hashed_password)

async def randomized_filename(file: UploadFile):
	file_ext = file.filename.split(".")[-1]
	new_filename = f"{uuid.uuid4()}.{file_ext}"
	return new_filename

async def send_email_verification(username: str, email: str, verif_code: str):
	template = f"""
	<p>Hello {username},</p>
	<p>Thank you for signing up on our platform!</p>
	<p>Your email verification code is: <strong>{verif_code}</strong></p>
	<p>Please use this code to verify your email address.</p>
	"""
	message = MessageSchema(
		subject="DShare Verification Code",
		recipients=[email],
		body=template,
		subtype="html"
	)
	fm = FastMail(conf)
	await fm.send_message(message)
	return

def validate_api_key(api_key: str):
	if api_key != settings.SERVER_API_KEY:
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail="Invalid API Key"
		)

def gen_verif_code():
	verif_code = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
	return verif_code

async def api_key_auth(api_key: str = Security(APIKeyHeader(name="X-API-Key", auto_error=False))):
	if api_key is None:
		raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="API Key missing")
	validate_api_key(api_key)
	return api_key

