from fastapi import FastAPI
from controllers import *
from utils.tokens_record import clean_expired_tokens
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

allow_origins=[
    "http://localhost",
    "http://localhost:3000",
    "http://127.0.0.1:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

clean_expired_tokens()

for router in routers:
    app.include_router(router, prefix="/api")