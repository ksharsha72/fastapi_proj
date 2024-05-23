import sys

sys.path.insert(0, "../")

from typing import Optional, List
from fastapi import FastAPI, Response, status, HTTPException, Body, Depends
from random import randrange
import psycopg2
import utils
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
import models
import schemas
from database import engine, get_db
from routers import post, user, auth, vote

from config import settings
from fastapi.middleware.cors import CORSMiddleware

# models.Base.metadata.create_all(bind=engine)
app = FastAPI()
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)
