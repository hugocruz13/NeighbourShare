from fastapi import FastAPI
from controllers import *
from utils.tokens_record import clean_expired_tokens
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from services.votacao_service import check_votacoes_expiradas

app = FastAPI()
scheduler = AsyncIOScheduler()

clean_expired_tokens()

@app.on_event('startup')
async def start_scheduler():
    scheduler.add_job(check_votacoes_expiradas, "interval", hours=24)
    scheduler.start()

for router in routers:
    app.include_router(router, prefix="/api")