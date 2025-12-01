from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from app.routes import auth, analyze
import os
from contextlib import asynccontextmanager
from app.services.redis_client import connect_redis, close_redis 

@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_redis()
    yield
    await close_redis()

# Pass the lifespan function to the FastAPI app
app = FastAPI(title="Smart Medical Assistant", lifespan=lifespan)

@app.get("/")
def read_root():
    return {"message" : "Welcome to Smart Medical Assistant"}

app.add_middleware(
    SessionMiddleware,
    secret_key = os.getenv("SECRET_KEY" , "supersecret")
)

app.include_router(auth.router)
app.include_router(analyze.router)