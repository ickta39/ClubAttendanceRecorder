from pydantic import BaseModel

class ProfileResponse(BaseModel):
    id: int
    name: str
    admin: bool