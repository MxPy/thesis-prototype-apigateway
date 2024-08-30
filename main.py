from fastapi import FastAPI, status, Request, Response, Header , Depends
from conf import settings
from typing import Annotated
from core import route
import uvicorn
from routers import auth, sensors
from fastapi.security import HTTPBearer
from schemas.users import *

app = FastAPI()
security = HTTPBearer()

@app.get("/")
async def read_root():
	return {"Hello":"World"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}


app.include_router(auth.router)
app.include_router(sensors.router)


if __name__ == '__main__':
    #change port to nondocker run to 8001 and in docker to 8000
    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="info", reload=True)