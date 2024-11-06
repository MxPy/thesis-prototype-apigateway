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
async def get_all(data: CreateSensorDataRequestModel, request: Request, response: Response, session_id: str = Header(...)):
    pass
