from datetime import datetime, time
from sqlmodel import Field, SQLModel

class User(SQLModel, table=True):
    id: int = Field(primary_key=True, default=None)
    email: str = Field(unique=True, nullable=False)
    password: str = Field(nullable=False)
    admin: bool = Field(default=False)

class Profile(SQLModel, table=True):
    id: int = Field(primary_key=True)
    name: str

class AttendanceRecord(SQLModel, table=True):
    row: int = Field(primary_key=True)
    id: int
    date: datetime = Field(nullable=False)
    executor: int
    executed_time: datetime