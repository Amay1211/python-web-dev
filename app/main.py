# import psycopg2
# from psycopg2.extras import RealDictCursor

from fastapi import FastAPI
from . import models
from .database import engine, getDb
from .routers import users, post, authentication, votes
from fastapi.middleware.cors import CORSMiddleware

# Commented out to avoid creating the tables again when the app is run, now tables will be created by alembic
# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(post.router)
app.include_router(authentication.router)
app.include_router(votes.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/health")
async def root():
    return {"message": "Health check"}
