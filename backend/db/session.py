import os
from dotenv import load_dotenv
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine

load_dotenv()

DATABASE_URL = str(os.getenv("DATABASE_URL"))
engine = create_engine(str(DATABASE_URL), connect_args={"check_same_thread": False})
connection = engine.connect()
if connection:
    print("Conexão estabelecida com a Base de Dados")
else:
    print("Erro ao conectar com a Base de Dados")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()