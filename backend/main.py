from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from controllers import *
from utils.tokens_record import clean_expired_tokens
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from services.votacao_service import check_votacoes_expiradas
from services.recurso_service import checkar_estado_recurso

app = FastAPI()
scheduler = AsyncIOScheduler()

# CORS setup
origins = [
    "http://localhost:3000",  # React em desenvolvimento
]

@app.on_event('startup')
async def start_scheduler():
    scheduler.add_job(check_votacoes_expiradas, "interval", hours=24)
    scheduler.add_job(checkar_estado_recurso, 'cron', hour=0)
    scheduler.start()

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
