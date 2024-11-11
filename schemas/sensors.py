from pydantic import BaseModel

class CreateSensorDataRequestModel(BaseModel):
    userId: str
    ir: list[int]
    red: list[int]
    ax: list[int]
    ay: list[int]
    az: list[int]
    recordedAt: str
    
    