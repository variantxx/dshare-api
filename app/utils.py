import uuid
import random
import string
from fastapi import UploadFile
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

async def send_email_verification(username: str, email: str):
	verification_code = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
	template = f"""
	<p>Hello {username},</p>
	<p>Thank you for signing up on our platform!</p>
	<p>Your email verification code is: <strong>{verification_code}</strong></p>
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
	return verification_code
