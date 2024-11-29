from fastapi import FastAPI, status, Request, Response, Header , Depends
from conf import settings
from typing import Annotated
from core import route
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from routers import auth, sensors, feed, comment_feed, health, websockets
from fastapi.security import HTTPBearer
from q.queueManager import lifespan
from schemas.users import *
import logging
import sys
ch = logging.StreamHandler(sys.stdout)
logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(funcName)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[ch]
    )

app = FastAPI(lifespan=lifespan)
security = HTTPBearer()

origins = ["http://localhost:3000",
           "http://192.168.33.3:3000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials = True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["session_id"],
)


@app.get("/")
async def read_root():
	return {"Hello":"World"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}



app.include_router(auth.router)
app.include_router(sensors.router)
app.include_router(health.router)
app.include_router(feed.router)
app.include_router(comment_feed.router)
app.include_router(websockets.router)


if __name__ == '__main__':
    #change port to nondocker run to 8001 and in docker to 8000
    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="info", reload=True)