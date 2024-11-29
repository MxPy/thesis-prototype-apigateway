from fastapi import status, Request, Response, APIRouter, Header
from conf import settings
from core import route
from schemas.users import *
from pydantic import BaseModel
class User(BaseModel):
    userId: str
    nickName: str

router = APIRouter(
    prefix='/forum',
    tags=['forum'])

@route(
    request_method=router.post,
    path='/create',
    status_code=status.HTTP_200_OK,
    payload_key='data',
    service_url=settings.MOCK_SERVICE_URL,
    authentication_required=True,
    privileges_level=0,
)
async def get_all(data:User, request: Request, response: Response, session_id: str = Header(...)):
    pass

@route(
    request_method=router.get,
    path='/whoami',
    status_code=status.HTTP_200_OK,
    payload_key='',
    service_url=settings.MOCK_SERVICE_URL,
    authentication_required=True,
    privileges_level=0,
)
async def get_all(userId:str, request: Request, response: Response, session_id: str = Header(...)):
    pass