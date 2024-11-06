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
    
class UserID(BaseModel):
    userId: str

class UpdateUserRequest(BaseModel):
    userId: str = Field(alias="userId")
    user: User
