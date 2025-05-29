import os
import re
import time
import traceback
from pathlib import Path

from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

from db import models


DB_HOST = os.getenv("DB_HOST", "db")
DB_PORT = os.getenv("DB_PORT", "1433")
DB_USER = os.getenv("DB_USER", "sa")
DB_PASSWORD = os.getenv("DB_PASSWORD", "DEVesi2025")
DB_NAME = os.getenv("DB_NAME", "NeighbourShare")
DB_DRIVER = os.getenv("DB_DRIVER", "ODBC Driver 18 for SQL Server")
DB_ENCRYPT = os.getenv("DB_ENCRYPT", "no")
DB_TRUST_CERT = os.getenv("DB_TRUST_CERT", "yes")
DB_WAIT_TIMEOUT = int(os.getenv("DB_WAIT_TIMEOUT", "600"))

SEED_SQL_DIR = Path(os.getenv("SEED_SQL_DIR", "/sql-init"))


def _connection_url(database: str) -> str:
    return (
        f"mssql+pyodbc://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{database}"
        f"?driver={DB_DRIVER.replace(' ', '+')}&Encrypt={DB_ENCRYPT}"
        f"&TrustServerCertificate={DB_TRUST_CERT}"
    )


def _wait_for_sql_server(engine) -> None:
    deadline = time.time() + DB_WAIT_TIMEOUT
    attempt = 0
    while time.time() < deadline:
        attempt += 1
        try:
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            print(f"[db-init] SQL Server ready after {attempt} attempts")
            return
        except SQLAlchemyError as exc:
            print(f"[db-init] SQL Server not ready yet (attempt {attempt}): {exc}")
            time.sleep(3)

    raise TimeoutError("SQL Server did not become ready within timeout")


def _create_database_if_missing(master_engine) -> None:
    query = text(
        "SELECT 1 FROM sys.databases WHERE name = :db_name"
    )

    with master_engine.connect() as conn:
        exists = conn.execute(query, {"db_name": DB_NAME}).scalar() is not None

    if exists:
        print(f"[db-init] Database [{DB_NAME}] already exists")
        return

    # CREATE DATABASE must run in autocommit mode, outside an implicit transaction.
    with master_engine.connect().execution_options(isolation_level="AUTOCOMMIT") as conn:
        conn.execute(text(f"CREATE DATABASE [{DB_NAME}]"))
    print(f"[db-init] Database [{DB_NAME}] created")


def _split_sql_batches(sql_text: str) -> list[str]:
    chunks = re.split(r"^\s*GO\s*$", sql_text, flags=re.IGNORECASE | re.MULTILINE)
    return [chunk.strip() for chunk in chunks if chunk.strip()]


def _normalize_sql_batch(batch: str) -> str:
    # Connection is already opened against DB_NAME, so USE directives are unnecessary.
    lines = [line for line in batch.splitlines() if not re.match(r"^\s*USE\s+", line, flags=re.IGNORECASE)]
    return "\n".join(lines).strip()


def _execute_sql_file(engine, sql_file: Path) -> None:
    print(f"[db-init] Executing seed file: {sql_file.name}")
    sql_text = sql_file.read_text(encoding="utf-8")
    batches = _split_sql_batches(sql_text)

    with engine.connect().execution_options(isolation_level="AUTOCOMMIT") as conn:
        for batch in batches:
            normalized = _normalize_sql_batch(batch)
            if normalized:
                conn.execute(text(normalized))


def _run_seeds_if_needed(db_engine) -> None:
    tipos_file = SEED_SQL_DIR / "tipos&estados.sql"
    contas_file = SEED_SQL_DIR / "contas.sql"

    if tipos_file.exists():
        _execute_sql_file(db_engine, tipos_file)
    else:
        print("[db-init] Skipping tipos&estados.sql (file missing)")

    if contas_file.exists():
        _execute_sql_file(db_engine, contas_file)
    else:
        print("[db-init] Skipping contas.sql (file missing)")


def main() -> None:
    print("[db-init] Starting database bootstrap")
    master_engine = create_engine(_connection_url("master"), pool_pre_ping=True)
    _wait_for_sql_server(master_engine)
    _create_database_if_missing(master_engine)

    app_engine = create_engine(_connection_url(DB_NAME), pool_pre_ping=True)
    print("[db-init] Creating/updating schema from SQLAlchemy models")
    models.Base.metadata.create_all(bind=app_engine)
    _run_seeds_if_needed(app_engine)

    print("[db-init] Database initialization completed")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"[db-init] Fatal error: {exc}")
        traceback.print_exc()
        raise
