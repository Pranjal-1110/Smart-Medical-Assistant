from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from app.routes import auth, analyze
import os

app = FastAPI(title="Smart Medical Assistant")

@app.get("/")
def read_root():
    return {"message" : "Welcome to Smart Medical Assistant"}

app.add_middleware(
    SessionMiddleware,
    secret_key = os.getenv("SECRET_KEY" , "supersecret")
)

app.include_router(auth.router)
app.include_router(analyze.router)
