from typing import Annotated

from fastapi import Depends
from sqlmodel import Session

from .model import *

engine = None

def get_session():
    with Session(engine) as session:
        yield session

session_deps = Annotated[Session, Depends(get_session)]