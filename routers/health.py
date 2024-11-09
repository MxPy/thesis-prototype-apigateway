from fastapi import status, Request, Response, APIRouter, Header, Query
from conf import settings
from core import route
from schemas.health import (
    User, UpdateUserRequest, BMRTDEE
)
from typing import Optional

router = APIRouter(
    prefix='/health',
    tags=['health']
)

@route(
    request_method=router.post,
    path='/users',
    status_code=status.HTTP_200_OK,
    payload_key='data',
    service_url=settings.HEALTH_SERVICE_URL,
    authentication_required=True,
    privileges_level=0,
)
async def get_all(data:User, request: Request, response: Response, session_id: str = Header(...)):
    pass

@route(
    request_method=router.get,
    path='/users',
    status_code=status.HTTP_200_OK,
    payload_key='',
    service_url=settings.HEALTH_SERVICE_URL,
    authentication_required=True,
    privileges_level=0,
)
async def get_all(userId :str, request: Request, response: Response, session_id: str = Header(...)):
    pass

@route(
    request_method=router.put,
    path='/users',
    status_code=status.HTTP_200_OK,
    payload_key='data',
    service_url=settings.HEALTH_SERVICE_URL,
    authentication_required=True,
    privileges_level=0,
)
async def get_all(userId :str, data:UpdateUserRequest, request: Request, response: Response, session_id: str = Header(...)):
    pass

@route(
    request_method=router.put,
    path='/users/bmr-tdee',
    status_code=status.HTTP_200_OK,
    payload_key='data',
    service_url=settings.HEALTH_SERVICE_URL,
    authentication_required=True,
    privileges_level=0,
)
async def get_all(userId :str, data:BMRTDEE, request: Request, response: Response, session_id: str = Header(...)):
    pass

@route(
    request_method=router.get,
    path='/users/metrics',
    status_code=status.HTTP_200_OK,
    payload_key='',
    service_url=settings.HEALTH_SERVICE_URL,
    authentication_required=True,
    privileges_level=0,
)
async def get_all(userId :str, request: Request, response: Response, session_id: str = Header(...)):
    pass

@route(
    request_method=router.get,
    path='/workouts',
    status_code=status.HTTP_200_OK,
    payload_key='',
    service_url=settings.HEALTH_SERVICE_URL,
    authentication_required=True,
    privileges_level=0,
)
async def get_all(userId :str, request: Request, response: Response, session_id: str = Header(...)):
    pass

@route(
    request_method=router.get,
    path='/workouts/single',
    status_code=status.HTTP_200_OK,
    payload_key='',
    service_url=settings.HEALTH_SERVICE_URL,
    authentication_required=True,
    privileges_level=0,
)
async def get_all(search:str, userId :str, workoutId:str, request: Request, response: Response, session_id: str = Header(...)):
    pass