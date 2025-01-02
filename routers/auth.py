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
    service_url=settings.AUTH_SERVICE_URL,
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
    response_key_to_forge_into_header='session_id',
    service_url=settings.AUTH_SERVICE_URL,
    authentication_required=False
)
async def login(username_password: UserLogin,
                request: Request, response: Response):
    pass

@route(
    request_method=router.post,
    path='/logout',
    status_code=status.HTTP_204_NO_CONTENT,
    payload_key='',
    
    service_url=settings.AUTH_SERVICE_URL,
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
    service_url=settings.AUTH_SERVICE_URL,
    authentication_required=False
)
async def reset_password(username_password: ResetPassword,
                request: Request, response: Response):
    pass

@route(
    request_method=router.post,
    path='/cms/register-admin',
    status_code=status.HTTP_200_OK,
    payload_key='username_password',
    service_url=settings.AUTH_SERVICE_URL,
    authentication_required=True,
    privileges_level=2,
)
async def reset_password(username_password: User,
                request: Request, response: Response, session_id: str = Header(...)):
    pass

@route(
    request_method=router.get,
    path='/cms/get_permission_level',
    status_code=status.HTTP_200_OK,
    payload_key='',
    service_url=settings.AUTH_SERVICE_URL,
    keep_header_in_body_after_forging=True,
    authentication_required=True,
    privileges_level=1,
)
async def logout(userId: str,request: Request, response: Response, session_id: str = Header(...)):
    pass

@route(
    request_method=router.put,
    path='/cms/user/update',
    status_code=status.HTTP_200_OK,
    payload_key='username_password',
    service_url=settings.AUTH_SERVICE_URL,
    authentication_required=True,
    privileges_level=2,
)
async def reset_password(username_password: User,
                request: Request, response: Response, session_id: str = Header(...)):
    pass

@route(
    request_method=router.delete,
    path='/cms/user/delete',
    status_code=status.HTTP_200_OK,
    payload_key='',
    service_url=settings.AUTH_SERVICE_URL,
    keep_header_in_body_after_forging=True,
    authentication_required=True,
    privileges_level=1,
)
async def logout(userId: str,request: Request, response: Response, session_id: str = Header(...)):
    pass

@route(
    request_method=router.get,
    path='/cms/user/get',
    status_code=status.HTTP_200_OK,
    payload_key='',
    service_url=settings.AUTH_SERVICE_URL,
    keep_header_in_body_after_forging=True,
    authentication_required=True,
    privileges_level=1,
)
async def logout(userId: str,request: Request, response: Response, session_id: str = Header(...)):
    pass

@route(
    request_method=router.get,
    path='/cms/user/get-u',
    status_code=status.HTTP_200_OK,
    payload_key='',
    service_url=settings.AUTH_SERVICE_URL,
    keep_header_in_body_after_forging=True,
    authentication_required=True,
    privileges_level=1,
)
async def logout(username: str,request: Request, response: Response, session_id: str = Header(...)):
    pass

@route(
    request_method=router.delete,
    path='/cms/user/all',
    status_code=status.HTTP_200_OK,
    payload_key='',
    service_url=settings.AUTH_SERVICE_URL,
    keep_header_in_body_after_forging=True,
    authentication_required=True,
    privileges_level=1,
)
async def logout(request: Request, response: Response, session_id: str = Header(...)):
    pass

@route(
    request_method=router.get,
    path='/cms/user/all',
    status_code=status.HTTP_200_OK,
    payload_key='',
    service_url=settings.AUTH_SERVICE_URL,
    keep_header_in_body_after_forging=True,
    authentication_required=True,
    privileges_level=1,
)
async def logout(request: Request, response: Response, session_id: str = Header(...)):
    pass

@route(
    request_method=router.get,
    path='/cms/session/all',
    status_code=status.HTTP_200_OK,
    payload_key='',
    service_url=settings.AUTH_SERVICE_URL,
    keep_header_in_body_after_forging=True,
    authentication_required=True,
    privileges_level=1,
)
async def logout(request: Request, response: Response, session_id: str = Header(...)):
    pass

@route(
    request_method=router.delete,
    path='/cms/session/all',
    status_code=status.HTTP_200_OK,
    payload_key='',
    service_url=settings.AUTH_SERVICE_URL,
    keep_header_in_body_after_forging=True,
    authentication_required=True,
    privileges_level=1,
)
async def logout(request: Request, response: Response, session_id: str = Header(...)):
    pass