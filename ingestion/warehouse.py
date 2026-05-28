import duckdb
from pathlib import Path
from utils.logger import get_logger

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
logger = get_logger(__name__)

def init_warehouse ():
    conn = duckdb.connect(str(_PROJECT_ROOT / "data" / "warehouse.duckdb"))
    has_pk = conn.execute("""
        SELECT COUNT(*) FROM information_schema.table_constraints
        WHERE table_name = 'departures' AND constraint_type = 'PRIMARY KEY'
    """).fetchone()[0]
    if not has_pk:
        conn.execute("DROP TABLE IF EXISTS departures")
    conn.execute("""CREATE TABLE IF NOT EXISTS departures
                (zug VARCHAR,
                geplante_zeit VARCHAR,
                tatsaechliche_zeit VARCHAR,
                gleis VARCHAR,
                linie VARCHAR,
                richtung VARCHAR,
                verspaetung_min INTEGER,
                id VARCHAR PRIMARY KEY)""")
    logger.info("Datenbank Verbindung hergestellt")
    return conn


def insert_departures (conn, data: list[dict]):
    conn.executemany("""INSERT INTO departures VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                        ON CONFLICT (id) DO NOTHING""",
                     [[e["zug"], e["geplante_zeit"],
                       e["tatsaechliche_zeit"],
                       e["gleis"],
                       e["linie"], e["richtung"],
                       e["verspaetung_min"], e["id"]] for e in data])
    logger.info("Tabelle befüllt")
    return conn