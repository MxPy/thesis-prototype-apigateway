from fastapi import status, Request, Response, APIRouter, Header, Depends, HTTPException, File, Form, UploadFile
from conf import settings
from core import route
import aiohttp
import os
import re
from datetime import datetime
from schemas.users import *
from schemas import forum
from files.services import download_file, upload_file
from auth import decode_access_token
from network import make_request
import logging
from typing import Optional

logger = logging.getLogger()

routerRead = APIRouter(
    prefix='/forum-read',
    tags=['forum-read'])

routerWrite = APIRouter(
    prefix='/forum-write',
    tags=['forum-write'])

@routerWrite.post(
    "/forum-posts",
    status_code=status.HTTP_201_CREATED,
)
async def file_upload(post: forum.PostOuterRequest = Depends(), session_id: str = Header(...)):
    # Validate token
    exc = None
    try:
        token_payload = await decode_access_token(session_id)
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

    # Create the inner request
    inner_request = forum.PostInerRequest(
        userId=post.userId,
        title=post.title,
        tag=post.tag,
        imageLink=None,
        description=post.description
    )
    

    # Upload file to S3 if present
    if post.image and post.image.filename:
        try:
            safe_title = re.sub(r'[^\w\s-]', '', post.title).strip().replace(' ', '_')  # Remove special characters
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')  # Add a timestamp to ensure uniqueness
            extension = os.path.splitext(post.image.filename)[1]  # Keep the original file extension
            new_filename = f"{safe_title}_{timestamp}{extension}"  # Combine title and timestamp

            # Rename the file
            post.image.filename = new_filename
            uploaded = await upload_file(
                user_id=post.userId,
                bucket_name="images",
                file=post.image
            )
            if uploaded:
                inner_request.imageLink = uploaded.get("path")
        except Exception as e:
            logger.error(f"Failed to upload file: {str(e)}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to upload image"
            )

    # Prepare request data and headers
    service_headers = {}
    request_data = inner_request.model_dump(exclude_none=True)
    url = settings.FORUM_WRITE_API_URL+"/forum-write/forum-posts"
    print(url)
    logger.info(url)
    try:
        response_data, status_code_from_service = await make_request(
            url=url,
            method="post",
            data=request_data,
            headers=service_headers,
        )
    except aiohttp.client_exceptions.ClientConnectorError:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail='Service is unavailable.',
            headers={'WWW-Authenticate': 'Bearer'},
        )

    if status_code_from_service not in (200, 201):
        raise HTTPException(
            status_code=status_code_from_service,
            detail="Failed to process request"
        )

    return response_data

@routerWrite.post(
    "/user-avatar", 
    status_code=status.HTTP_201_CREATED
)
async def avatar_upload(
    user_id: str = Form(...), 
    avatar: Optional[UploadFile] = File(None), 
    session_id: str = Header(...)
):
    # Validate token
    exc = None
    try:
        token_payload = await decode_access_token(session_id)
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
    
    # Validate avatar presence
    if not avatar or not avatar.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Avatar image is required"
        )
    
    # Upload avatar to S3
    try:
        # Generowanie unikalnej nazwy pliku dla avatara
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        extension = os.path.splitext(avatar.filename)[1]
        new_filename = f"avatar_{user_id}_{timestamp}{extension}"
        avatar.filename = new_filename

        # Upload pliku
        uploaded = await upload_file(
            user_id=user_id,
            bucket_name="avatars",
            file=avatar
        )
        
        # if not uploaded:
        #     raise HTTPException(
        #         status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        #         detail="Failed to upload avatar"
        #     )
        
        # # Przygotowanie danych do wysłania do serwisu użytkowników
        # request_data = {
        #     "userId": user_id,
        #     "avatarLink": uploaded.get("path")
        # }
        
        # # Wysłanie linku do avatara do serwisu użytkowników
        # url = settings.AUTH_SERVICE_URL + "/update-avatar"
        # service_headers = {}
        
        # response_data, status_code_from_service = await make_request(
        #     url=url,
        #     method="post",
        #     data=request_data,
        #     headers=service_headers,
        # )
        
        # if status_code_from_service not in (200, 201):
        #     raise HTTPException(
        #         status_code=status_code_from_service,
        #         detail="Failed to update user avatar"
        #     )
        
        return {"avatarLink": uploaded.get("path")}
    
    except Exception as e:
        logger.error(f"Avatar upload failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to process avatar upload"
        )