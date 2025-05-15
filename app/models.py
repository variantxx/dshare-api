import uuid
import random
import string
from sqlalchemy import Column, String, Boolean, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql.expression import text
from app.database import Base


class User(Base):
	__tablename__  = "users"
	id             = Column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4)
	email          = Column(String, nullable=False, unique=True)
	username       = Column(String, nullable=False)
	role           = Column(String, nullable=False, server_default=text("'user'"))
	password       = Column(String, nullable=False)
	gender         = Column(String, nullable=True, default=None)
	birth_date     = Column(TIMESTAMP(timezone=True), nullable=True, default=None)
	confirmed      = Column(Boolean, nullable=False, server_default=text("false"))
	verif_code     = Column(String, nullable=False)
	pending        = Column(Boolean, nullable=False, server_default=text("false"))
	deleted        = Column(Boolean, nullable=False, server_default=text("false"))
	created_at     = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))

class Upload(Base):
	__tablename__	= "uploads"
	id             = Column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4)
	user_id        = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
	thumbnail_url	= Column(String, nullable=False)
	file_url			= Column(String, nullable=False)
	title				= Column(String, nullable=False)
	hash				= Column(String, nullable=False)
	created_at     = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))

class Bookmark(Base):
	__tablename__  = "bookmarks"
	id             = Column(UUID(as_uuid=True), primary_key=True, nullable=False, default=uuid.uuid4)
	user_id        = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
	upload_id      = Column(UUID(as_uuid=True), ForeignKey("uploads.id"), nullable=False)
	created_at     = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
