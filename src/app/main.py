import os

import dotenv
from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlmodel import SQLModel
from starlette.middleware.cors import CORSMiddleware
import uvicorn

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

@app.get("/profile")
async def get_profile():
    pass

if __name__ == "__main__":
    sqlite_url = f"sqlite:///{os.getenv('DATABASE_FILE')}"

    connect_args = {"check_same_thread": False}
    db.engine = create_engine(sqlite_url, connect_args=connect_args)
    SQLModel.metadata.create_all(db.engine)

    uvicorn.run(app)