from fastapi import APIRouter, Depends, status, Header, HTTPException
from fastapi.background import BackgroundTasks
from fastapi.responses import FileResponse
from auth import decode_access_token_backend_admin

from files.schemas import FileDownload, FileUpload
from files.services import download_file, upload_file

filesRouter = APIRouter(prefix="/files", tags=["files"])
import logging

logger = logging.getLogger()

@filesRouter.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    tags=["files"],
)
async def file_upload(file: FileUpload = Depends(), session_id: str = Header(...)):
    exc = None
    try:
        token_payload = await decode_access_token_backend_admin(session_id)
        logger.info(token_payload["valid"])
        if not token_payload["valid"]:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=token_payload["detail"],
                headers={'WWW-Authenticate': 'Bearer'},
            )
    except Exception as e:
        exc = str(e)
    finally:
        if exc:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=exc,
                headers={'WWW-Authenticate': 'Bearer'},
                        )
    logger.info("uploooooad")
    if uploaded := await upload_file(
        user_id=file.user_id, bucket_name=file.bucket_name, file=file.file
    ):
        return uploaded