from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session
from db.session import SessionLocal
from controllers import *


app = FastAPI()

for router in routers:
    app.include_router(router, prefix="/api")