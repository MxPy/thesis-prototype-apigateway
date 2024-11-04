from fastapi import status, Request, Response, APIRouter, Header, Query
from conf import settings
from core import route
from schemas.health import (
    Workout, CreateWorkoutRequest, UpdateWorkoutRequest,
    GetWorkoutValueByStringRequest, GetWorkoutByUserIdRequest,
    GetWorkoutByUserIdTrainingIdRequest
)
from typing import Optional

router = APIRouter(
    prefix='/health',
    tags=['health']
)

@route(
    request_method=router.post,
    path='/workouts',
    status_code=status.HTTP_200_OK,
    payload_key='data',
    service_url=settings.HEALTH_SERVICE_URL,
    authentication_required=True,
    privileges_level=0,
)
async def create_workout(
    data: Workout,
    request: Request,
    response: Response,
    session_id: str = Header(...)
):
    pass

@route(
    request_method=router.delete,
    path='/delete_all',
    status_code=status.HTTP_200_OK,
    payload_key='',
    service_url=settings.HEALTH_SERVICE_URL,
    authentication_required=True,
    privileges_level=0,
)
async def delete_all_workouts(
    request: Request,
    response: Response,
    session_id: str = Header(...)
):
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
async def get_all_workouts(
    request: Request,
    response: Response,
    session_id: str = Header(...)
):
    pass

@route(
    request_method=router.get,
    path='/{workoutId}',
    status_code=status.HTTP_200_OK,
    payload_key='',
    service_url=settings.HEALTH_SERVICE_URL,
    authentication_required=True,
    privileges_level=0,
)
async def get_workout(
    workoutId: int,
    request: Request,
    response: Response,
    session_id: str = Header(...)
):
    pass

@route(
    request_method=router.put,
    path='/workouts',
    status_code=status.HTTP_200_OK,
    payload_key='data',
    service_url=settings.HEALTH_SERVICE_URL,
    authentication_required=True,
    privileges_level=0,
)
async def update_workout(
    data: UpdateWorkoutRequest,
    request: Request,
    response: Response,
    session_id: str = Header(...)
):
    pass

@route(
    request_method=router.delete,
    path='/{workoutId}',
    status_code=status.HTTP_200_OK,
    payload_key='',
    service_url=settings.HEALTH_SERVICE_URL,
    authentication_required=True,
    privileges_level=0,
)
async def delete_workout(
    workoutId: int,
    request: Request,
    response: Response,
    session_id: str = Header(...)
):
    pass

@route(
    request_method=router.get,
    path='/workouts/search',
    status_code=status.HTTP_200_OK,
    payload_key='data',
    service_url=settings.HEALTH_SERVICE_URL,
    authentication_required=True,
    privileges_level=0,
)
async def get_workout_value_by_string(
    data: GetWorkoutValueByStringRequest,
    request: Request,
    response: Response,
    session_id: str = Header(...)
):
    pass

@route(
    request_method=router.get,
    path='/workouts/user',
    status_code=status.HTTP_200_OK,
    payload_key='data',
    service_url=settings.HEALTH_SERVICE_URL,
    authentication_required=True,
    privileges_level=0,
)
async def get_workout_by_user_id(
    data: GetWorkoutByUserIdRequest,
    request: Request,
    response: Response,
    session_id: str = Header(...)
):
    pass

@route(
    request_method=router.get,
    path='/workouts/user/training',
    status_code=status.HTTP_200_OK,
    payload_key='data',
    service_url=settings.HEALTH_SERVICE_URL,
    authentication_required=True,
    privileges_level=0,
)
async def get_workout_by_user_id_training_id(
    data: GetWorkoutByUserIdTrainingIdRequest,
    request: Request,
    response: Response,
    session_id: str = Header(...)
):
    pass