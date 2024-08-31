from fastapi import status, Request, Response, APIRouter, Header
from conf import settings
from core import route
from schemas.sensors import *



router = APIRouter(
    prefix='/sensors',
    tags=['sensors'])

@route(
    request_method=router.get,
    path='/',
    status_code=status.HTTP_200_OK,
    payload_key='',
    service_url=settings.SENSORS_SERVICE_URL,
    authentication_required=True,
    privileges_level=2,
)
async def get_all(request: Request, response: Response, session_id: str = Header(...)):
    pass