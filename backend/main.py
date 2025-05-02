from fastapi import FastAPI
from controllers import *
from utils.tokens_record import clean_expired_tokens
from fastapi.middleware.cors import CORSMiddleware
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from services.votacao_service import check_votacoes_expiradas
from services.recurso_service import checkar_estado_recurso

scheduler = AsyncIOScheduler()
app = FastAPI()

allow_origins=[
    "http://localhost",
    "http://localhost:3000",
    "http://127.0.0.1:3000"
]


@app.on_event('startup')
async def start_scheduler():
    scheduler.add_job(check_votacoes_expiradas, "interval", hours=24)
    scheduler.add_job(checkar_estado_recurso, 'cron', hour=0)
    scheduler.start()


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