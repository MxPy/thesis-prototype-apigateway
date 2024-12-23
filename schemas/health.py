from pydantic import BaseModel, Field
from typing import List
from datetime import datetime
from typing import Optional

class User(BaseModel):
    userId: str
    gender: str
    age: int
    weight: float
    height: int
    bmr: Optional[int] = None
    tdee: Optional[int] = None
    
class BMRTDEE(BaseModel):
    bmr: int
    tdee: int

class UpdateUserRequest(BaseModel):
    gender: str
    age: int
    weight: float
    height: int
    bmr: Optional[int] = None
    tdee: Optional[int] = None

#TODO MOVE TO ADMIN BELOW SCHEMAS
    
# Request Models
class CreateSensorDataRequest(BaseModel):
    userId: str
    ir: List[int]
    red: List[int]
    ax: List[int]
    ay: List[int]
    az: List[int]
    recordedAt: str

# Query Parameter Models
class UserIdQuery(BaseModel):
    userId: str

class UserIdSensorIdQuery(BaseModel):
    userId: str
    id: int

# Response Models
class SensorDataResponse(BaseModel):
    data: List[dict]

class CountResponse(BaseModel):
    count: int

# Base Schema Model (as defined in components)
class SensorData(BaseModel):
    userId: str
    ir: List[int]
    red: List[int]
    ax: List[int]
    ay: List[int]
    az: List[int]
    recordedAt: str


from pydantic import BaseModel
from typing import List, Optional

# Base User Model (as defined in components)
class User(BaseModel):
    userId: str
    gender: str
    age: int
    weight: float
    height: int
    bmr: Optional[int] = None
    tdee: Optional[int] = None

# Response Models
class UsersResponse(BaseModel):
    data: List[User]

class CountResponse(BaseModel):
    count: int
    
# WORKOUT SCHEMAS

class WorkoutBase(BaseModel):
    # workoutId: Optional[int] = None
    userId: str
    workoutType: str
    duration: int  
    distance: float
    caloriesBurned: float
    avgSteps: int 
    avgHeartrate: float
    date: str

class Workout(BaseModel):
    workout: WorkoutBase

class WorkoutIdQuery(BaseModel):
    id: Optional[int] = None

class WorkoutsResponse(BaseModel):
    data: List[Workout]