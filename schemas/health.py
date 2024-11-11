from pydantic import BaseModel, Field
from uuid import uuid4

class User(BaseModel):
    userId: str
    gender: str
    age: int
    weight: float
    height: int
    bmr: int
    tdee: int
    
class BMRTDEE(BaseModel):
    bmr: int
    tdee: int

class UpdateUserRequest(BaseModel):
    gender: str
    age: int
    weight: float
    height: int
    bmr: int
    tdee: int
    
