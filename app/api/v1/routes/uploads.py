import os
import mimetypes
import hashlib
from fastapi import APIRouter, Depends, File, HTTPException, Request, UploadFile, status
from sqlalchemy.orm import Session
from supabase import create_client, Client
from slowapi import Limiter
from slowapi.util import get_remote_address
from ....database import get_db
from ....config import settings
from .... import schemas, utils, models, oauth2



router = APIRouter()

limiter = Limiter(key_func=get_remote_address)
supabase: Client = create_client(settings.SUPABASE_URL, settings.SUPABASE_API_KEY)

@router.post("/doc", response_model=schemas.UploadFileResponse)
@limiter.limit("10/minute")
async def upload_doc(request: Request, file: UploadFile = File(...), db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
   if not current_user.id:
      raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
   file_bytes = await file.read()
   sha256_hash = hashlib.sha256(file_bytes).hexdigest()
   # Check if file with this hash already exists
   existing_file = db.query(models.Upload).filter(models.Upload.hash == sha256_hash).first()
   if existing_file:
      # Create a new record pointing to the same file and thumbnail
      new_upload = models.Upload(
         user_id=current_user.id,
         file_url=existing_file.file_url,
         thumbnail_url=existing_file.thumbnail_url,
         title=os.path.splitext(file.filename)[0],
         hash=sha256_hash
      )
      db.add(new_upload)
      db.commit()
      db.refresh(new_upload)
      return new_upload
   # If not exists, generate thumbnail and upload both files
   thumbnail_bytes = await utils.generate_thumbnail(file_bytes, file.filename)
   new_filename = await utils.randomized_filename(file)
   thumbnail_filename = os.path.splitext(new_filename)[0] + ".jpg"
   file_path = new_filename
   thumbnail_path = thumbnail_filename
   content_type = mimetypes.guess_type(file.filename)[0] or "application/octet-stream"
   supabase.storage.from_("documents").upload(file_path, file_bytes, file_options={"content-type": content_type})
   supabase.storage.from_("thumbnails").upload(thumbnail_path, thumbnail_bytes.getvalue(), file_options={"content-type": "image/jpeg"})
   doc_url = supabase.storage.from_("documents").get_public_url(file_path)
   image_url = supabase.storage.from_("thumbnails").get_public_url(thumbnail_path)
   new_upload = models.Upload(
      user_id=current_user.id,
      file_url=doc_url,
      thumbnail_url=image_url,
      title=os.path.splitext(file.filename)[0],
      hash=sha256_hash
   )
   db.add(new_upload)
   db.commit()
   db.refresh(new_upload)
   return new_upload


