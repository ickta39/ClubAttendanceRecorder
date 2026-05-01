import os

import dotenv
from fastapi import FastAPI
from sqlalchemy import Select, create_engine, func
from sqlmodel import SQLModel, Session
from starlette.middleware.cors import CORSMiddleware
import uvicorn

from auth.password import *
from db.model import Profile, User
import db
import endpoint

dotenv.load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(endpoint.router)

def init_env():
    import secrets
    if (os.getenv("TOKEN_SECRET") is None or os.getenv("TOKEN_SECRET") == ""):
        dotenv.set_key(".env", "TOKEN_SECRET", secrets.token_hex())
    
    with Session(db.engine) as sess:
        result = sess.exec(Select(func.count()).select_from(User)).one()[0]

        if result == 0:
            password = secrets.token_hex(8)
            hashed = encode_password(password)

            dotenv.set_key(".env", "ADMIN_PASSWORD", password)

            admin_user = User(email=os.getenv("ADMIN_EMAIL"), password=hashed, admin=True)
            sess.add(admin_user)
            sess.commit()
            sess.refresh(admin_user)
            sess.add(Profile(id=admin_user.id, name=os.getenv("ADMIN_NAME")))
            sess.commit()


if __name__ == "__main__":
    sqlite_url = f"sqlite:///{os.getenv('DATABASE_FILE')}"

    connect_args = {"check_same_thread": False}
    db.engine = create_engine(sqlite_url, connect_args=connect_args)
    SQLModel.metadata.create_all(db.engine)

    init_env()

    uvicorn.run(app)