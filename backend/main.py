from fastapi import FastAPI
from backend.controllers import *

app = FastAPI()

for router in routers:
    app.include_router(router, prefix="/api")