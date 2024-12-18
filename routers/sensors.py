from fastapi import status, Request, Response, APIRouter, Header
from conf import settings
from core import route
from schemas.sensors import *

router = APIRouter(
    prefix='/sensors',
    tags=['sensors'])

@route(
    request_method=router.post,
    path='/handle_sensor_data',
    status_code=status.HTTP_200_OK,
    payload_key='data',
    service_url=settings.SENSORS_SERVICE_URL,
    authentication_required=True,
    privileges_level=0,
)
async def get_all(data: CreateSensorDataRequestModel, request: Request, response: Response, workoutType: str | None = None, session_id: str = Header(...)):
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
async def get_all(userId :str, id:str, request: Request, response: Response, session_id: str = Header(...)):
    pass

@route(
    request_method=router.get,
    path='/users/all',
    status_code=status.HTTP_200_OK,
    payload_key='',
    service_url=settings.HEALTH_SERVICE_URL,
    authentication_required=True,
    privileges_level=0,
)
async def get_all(userId :str, request: Request, response: Response, session_id: str = Header(...)):
    pass


#TODO MOVE BELOW TO ADMIN

from fastapi import Header, Request, Response, status
from schemas.health import (CreateSensorDataRequest, UserIdQuery, UserIdSensorIdQuery, SensorDataResponse, CountResponse)

@route(
    request_method=router.post,
    path='/',
    status_code=status.HTTP_200_OK,
    payload_key='data',
    service_url=settings.HEALTH_SERVICE_URL,
    authentication_required=True,
    privileges_level=1,
)
async def create_sensor_data(data: CreateSensorDataRequest, request: Request, response: Response, session_id: str = Header(...)):
    pass

@route(
    request_method=router.get,
    path='/all',
    status_code=status.HTTP_200_OK,
    payload_key='',
    service_url=settings.HEALTH_SERVICE_URL,
    authentication_required=True,
    privileges_level=1,
)
async def get_all_sensor_data(request: Request, response: Response, session_id: str = Header(...)):
    pass

@route(
    request_method=router.delete,
    path='/all',
    status_code=status.HTTP_200_OK,
    payload_key='',
    service_url=settings.HEALTH_SERVICE_URL,
    authentication_required=True,
    privileges_level=1,
)
async def delete_all_sensor_data(request: Request, response: Response, session_id: str = Header(...)):
    pass

@route(
    request_method=router.get,
    path='/all/count',
    status_code=status.HTTP_200_OK,
    payload_key='',
    service_url=settings.HEALTH_SERVICE_URL,
    authentication_required=True,
    privileges_level=1,
)
async def count_all_sensor_data(request: Request, response: Response, session_id: str = Header(...)):
    pass

@route(
    request_method=router.delete,
    path='/user',
    status_code=status.HTTP_200_OK,
    payload_key='',
    service_url=settings.HEALTH_SERVICE_URL,
    authentication_required=True,
    privileges_level=1,
)
async def delete_data_by_user_id(userId: str, request: Request, response: Response, session_id: str = Header(...)):
    pass

@route(
    request_method=router.get,
    path='/user/count',
    status_code=status.HTTP_200_OK,
    payload_key='',
    service_url=settings.HEALTH_SERVICE_URL,
    authentication_required=True,
    privileges_level=1,
)
async def count_data_by_user_id(userId: str, request: Request, response: Response, session_id: str = Header(...)):
    pass

@route(
    request_method=router.get,
    path='/user',
    status_code=status.HTTP_200_OK,
    payload_key='',
    service_url=settings.HEALTH_SERVICE_URL,
    authentication_required=True,
    privileges_level=1,
)
async def get_data_by_user_id_sensor_id(userId: str, id: int, request: Request, response: Response, session_id: str = Header(...)):
    pass

@route(
    request_method=router.get,
    path='/user/all',
    status_code=status.HTTP_200_OK,
    payload_key='',
    service_url=settings.HEALTH_SERVICE_URL,
    authentication_required=True,
    privileges_level=1,
)
async def get_data_by_user_id(userId: str, request: Request, response: Response, session_id: str = Header(...)):
    pass