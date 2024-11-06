from pydantic import BaseModel, Field
from uuid import uuid4

class User(BaseModel):
    user_id: str
    gender: str
    age: int
    weight: float
    height: int
    bmr: int
    tdee: int
    
class UserID(BaseModel):
    user_id: str

class UpdateUserRequest(BaseModel):
    user_id: str = Field(alias="userId")
    user: User
