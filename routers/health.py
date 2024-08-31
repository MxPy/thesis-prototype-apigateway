from fastapi import status, Request, Response, APIRouter, Header
from conf import settings
from core import route
from schemas.users import *



router = APIRouter(
    prefix='/health',
    tags=['health'])

@route(
    request_method=router.get,
    path='/workouts',
    status_code=status.HTTP_200_OK,
    payload_key='',
    service_url=settings.HEALTH_SERVICE_URL,
    authentication_required=True,
    privileges_level=0,
)
async def get_all(request: Request, response: Response, session_id: str = Header(...)):
    pass