from fastapi import FastAPI
from controllers import routers  # <- Certifica-te que importas a lista 'routers' aqui
from utils.tokens_record import clean_expired_tokens
from fastapi.middleware.cors import CORSMiddleware
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from services.votacao_service import check_votacoes_expiradas
from services.recurso_service import checkar_estado_recurso
import os
from fastapi.staticfiles import StaticFiles



scheduler = AsyncIOScheduler()
app = FastAPI()

app.mount("/uploadFiles", StaticFiles(directory="uploadFiles"), name="uploadFiles")

allow_origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://127.0.0.1:3000"
]

@app.on_event("startup")
async def startup_event():
    clean_expired_tokens()
    if not os.getenv("TESTING"):
        scheduler.add_job(check_votacoes_expiradas, "interval", hours=24)
        scheduler.add_job(checkar_estado_recurso, "cron", hour=0)
        scheduler.start()

@app.on_event("shutdown")
async def shutdown_event():
    if scheduler.running:
        scheduler.shutdown(wait=False)  # <- Aqui para evitar problemas no shutdown dos testes

app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

for router in routers:
    app.include_router(router, prefix="/api")