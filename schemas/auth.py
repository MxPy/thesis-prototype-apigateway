from pydantic import BaseModel, ConfigDict

class Token(BaseModel):
    session_id: str = ConfigDict(coerce_numbers_to_str=True)