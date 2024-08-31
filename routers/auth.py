from fastapi import status, Request, Response, APIRouter, Header
from conf import settings
from core import route
from schemas.users import *



router = APIRouter(
    prefix='/auth',
    tags=['auth'])


@route(
    request_method=router.post,
    path='/register',
    status_code=status.HTTP_201_CREATED,
    payload_key='username_password',
    service_url=settings.USERS_SERVICE_URL,
    authentication_required=False
)
async def register(username_password: User,
                request: Request, response: Response):
    pass

@route(
    request_method=router.post,
    path='/login',
    status_code=status.HTTP_200_OK,
    payload_key='username_password',
    service_url=settings.USERS_SERVICE_URL,
    authentication_required=False
)
async def register(username_password: UserLogin,
                request: Request, response: Response):
    pass

@route(
    request_method=router.post,
    path='/logout',
    status_code=status.HTTP_204_NO_CONTENT,
    payload_key='',
    service_url=settings.USERS_SERVICE_URL,
    authentication_required=True,
    keep_header_in_body_after_forging=True,
)
async def logout(request: Request, response: Response, session_id: str = Header(...)):
    pass

@route(
    request_method=router.put,
    path='/reset_password',
    status_code=status.HTTP_200_OK,
    payload_key='username_password',
    service_url=settings.USERS_SERVICE_URL,
    authentication_required=False
)
async def reset_password(username_password: ResetPassword,
                request: Request, response: Response):
    pass

