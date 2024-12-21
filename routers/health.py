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


# TODO: fix this, should be with param:
# PUT /health/users?userId=qwe 
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

# WORKOUTS

#TODO: create new for user
#	POST http://localhost:8000/health/workouts

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

from fastapi import Header, Request, Response, status, Query
from schemas.health import Workout, WorkoutsResponse, WorkoutIdQuery
from typing import Optional

@route(
    request_method=router.get,
    path='/workouts/all',
    status_code=status.HTTP_200_OK,
    payload_key='',
    service_url=settings.HEALTH_SERVICE_URL,
    authentication_required=True,
    privileges_level=1,
)
async def get_workouts(
    request: Request, 
    response: Response, 
    session_id: str = Header(...),
    id: Optional[int] = Query(None, description="Optional workout ID")
):
    """
    If id is provided, returns a specific workout.
    If id is not provided, returns all workouts.
    """
    pass

@route(
    request_method=router.delete,
    path='/workouts/all',
    status_code=status.HTTP_200_OK,
    payload_key='',
    service_url=settings.HEALTH_SERVICE_URL,
    authentication_required=True,
    privileges_level=1,
)
async def delete_workouts(
    request: Request, 
    response: Response, 
    session_id: str = Header(...),
    id: Optional[int] = Query(None, description="Optional workout ID")
):
    """
    If id is provided, deletes a specific workout.
    If id is not provided, deletes all workouts.
    """
    pass

from fastapi import Header, Request, Response, status
from schemas.health import User, UsersResponse, CountResponse

@route(
    request_method=router.get,
    path='/users/all',
    status_code=status.HTTP_200_OK,
    payload_key='',
    service_url=settings.HEALTH_SERVICE_URL,
    authentication_required=True,
    privileges_level=1,
)
async def get_all_users(request: Request, response: Response, session_id: str = Header(...)):
    pass


@route(
    request_method=router.delete,
    path='/users',
    status_code=status.HTTP_200_OK,
    payload_key='',
    service_url=settings.HEALTH_SERVICE_URL,
    authentication_required=True,
    privileges_level=1,
) # TODO: debug, remove comment, 500
async def delete_user(
    request: Request, 
    response: Response, 
    session_id: str = Header(...),
    userId: str = Query(..., description="User ID")
):
    pass


@route(
    request_method=router.delete,
    path='/users/all',
    status_code=status.HTTP_200_OK,
    payload_key='',
    service_url=settings.HEALTH_SERVICE_URL,
    authentication_required=True,
    privileges_level=1,
) # TODO: debug, remove comment, 500
async def delete_all_users(request: Request, response: Response, session_id: str = Header(...)):
    pass

@route(
    request_method=router.get,
    path='/users/count',
    status_code=status.HTTP_200_OK,
    payload_key='',
    service_url=settings.HEALTH_SERVICE_URL,
    authentication_required=True,
    privileges_level=1,
)
async def count_all_users(request: Request, response: Response, session_id: str = Header(...)):
    pass