from fastapi import FastAPI
from app.routes.analyze import router as analyze_router
import uvicorn

app = FastAPI()
app.include_router(analyze_router, prefix="/api")

if __name__ == "__main__":
    uvicorn.run("app.main:app" , host="127.0.0.1" , port=8000, reload = True)