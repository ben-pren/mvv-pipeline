import duckdb 
from utils.logger import get_logger

logger = get_logger(__name__)

def init_warehouse ():
    conn = duckdb.connect("data/warehouse.duckdb")
    conn.execute("""CREATE TABLE IF NOT EXISTS departures 
                (zug VARCHAR,
                geplante_zeit VARCHAR,
                tatsaechliche_zeit VARCHAR,
                gleis VARCHAR,
                linie VARCHAR,
                richtung VARCHAR,
                verspaetung_min INTEGER,
                id VARCHAR)""")
    logger.info("Datenbank Verbindung hergestellt")
    return conn
    

def insert_departures (conn, data: list[dict]):
    conn.executemany("""INSERT INTO departures VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                     [[e["zug"], e["geplante_zeit"],
                       e["tatsaechliche_zeit"],
                       e["gleis"],
                       e["linie"], e["richtung"], 
                       e["verspaetung_min"], e["id"]] for e in data])
    logger.info(" Tabelle befüllt")
    return conn