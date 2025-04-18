from fastapi import FastAPI
from controllers import *
from utils.tokens_record import clean_expired_tokens

app = FastAPI()

clean_expired_tokens()

for router in routers:
    app.include_router(router, prefix="/api")