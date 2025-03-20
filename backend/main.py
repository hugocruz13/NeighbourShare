from fastapi import FastAPI
from controllers import *

app = FastAPI()

for router in routers:
    app.include_router(router, prefix="/api")