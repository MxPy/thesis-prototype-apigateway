from fastapi import FastAPI, status, Request, Response
from conf import settings
from core import route

from schemas.users import *

app = FastAPI()


@route(
    request_method=app.post,
    path='/user/register',
    status_code=status.HTTP_201_CREATED,
    payload_key='username_password',
    service_url=settings.USERS_SERVICE_URL,
    authentication_required=False
)
async def register(username_password: User,
                request: Request, response: Response):
    pass