from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from controllers import *

app = FastAPI()

# CORS setup
origins = [
    "http://localhost:3000",  # React em desenvolvimento
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
for router in routers:
    app.include_router(router, prefix="/api")
