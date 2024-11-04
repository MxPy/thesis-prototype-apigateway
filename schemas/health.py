from pydantic import BaseModel
from typing import List, Optional, Union

class Workout(BaseModel):
    workoutId: int
    userId: str
    workoutType: str
    duration: int
    caloriesBurned: float
    avgSteps: int  # using int instead of uint32 as Python doesn't have uint32
    avgHeartrate: float
    date: str

# Create Workout
class CreateWorkoutRequest(BaseModel):
    workout: Workout

class CreateWorkoutResponse(BaseModel):
    message: str
    workout: Workout

# Get Workout
class GetWorkoutRequest(BaseModel):
    workoutId: int

class GetWorkoutResponse(BaseModel):
    workout: Workout

# Get All Workouts
class GetAllWorkoutsRequest(BaseModel):
    pass

class GetAllWorkoutsResponse(BaseModel):
    workouts: List[Workout]

# Update Workout
class UpdateWorkoutRequest(BaseModel):
    workout: Workout

class UpdateWorkoutResponse(BaseModel):
    workout: Workout

# Delete Workout
class DeleteWorkoutRequest(BaseModel):
    workoutId: int

class DeleteWorkoutResponse(BaseModel):
    success: bool

# Delete All Workouts
class DeleteAllWorkoutsRequest(BaseModel):
    pass

class DeleteAllWorkoutsResponse(BaseModel):
    success: bool

# Get Workout Value By String
class GetWorkoutValueByStringRequest(BaseModel):
    workoutId: int
    userId: str
    fieldName: str

class GetWorkoutValueByStringResponse(BaseModel):
    value: str

# Get Workout By UserId
class GetWorkoutByUserIdRequest(BaseModel):
    userId: str

class GetWorkoutByUserIdResponse(BaseModel):
    workouts: List[Workout]

# Get Workout By UserId and TrainingId
class GetWorkoutByUserIdTrainingIdRequest(BaseModel):
    userId: str
    workoutId: int

class GetWorkoutByUserIdTrainingIdResponse(BaseModel):
    workout: Workout