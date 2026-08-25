# import psycopg2
# from psycopg2.extras import RealDictCursor

from fastapi import FastAPI
from . import models
from .database import engine, getDb
from .routers import users, post, authentication

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users.router)
app.include_router(post.router)
app.include_router(authentication.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/health")
async def root():
    return {"message": "Health check"}
