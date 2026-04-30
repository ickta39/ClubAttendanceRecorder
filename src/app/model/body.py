from pydantic import BaseModel

class IdentifyBody(BaseModel):
    email: str
    password: str