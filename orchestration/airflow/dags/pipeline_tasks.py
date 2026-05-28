from ingestion.extract import get_changes, get_plan
from ingestion.load import save_raw_data, save_transformed_data
from ingestion.warehouse import init_warehouse, insert_departures
from transformation.transform import transform_raw_data, transform_plan, join_plan_and_changes
from datetime import datetime, timedelta
from utils.logger import get_logger
import json

logger = get_logger(__name__)


def extract_and_save(ti=None):
    now = datetime.now()
    date_current = now.strftime("%y%m%d")
    hour_current = now.strftime("%H")

    prev = now.replace(minute=0, second=0, microsecond=0) - timedelta(hours=1)
    date_prev = prev.strftime("%y%m%d")
    hour_prev = prev.strftime("%H")

    changes_path = save_raw_data(get_changes("8000261"), "changes")
    plan_current_path = save_raw_data(get_plan("8000261", date_current, hour_current), "plan")

    plan_paths = [str(plan_current_path)]
    try:
        plan_prev_path = save_raw_data(get_plan("8000261", date_prev, hour_prev), "plan")
        plan_paths.append(str(plan_prev_path))
    except Exception as e:
        logger.warning(f"Vorherige Stunde ({date_prev} {hour_prev}) nicht verfügbar: {e}")

    ti.xcom_push(key="changes_path", value=str(changes_path))
    ti.xcom_push(key="plan_paths", value=plan_paths)
    logger.info(f"Daten extrahiert: {len(plan_paths)} Planstunden")


def transform_and_save(ti=None):
    changes_path = ti.xcom_pull(task_ids="extract_and_save", key="changes_path")
    plan_paths = ti.xcom_pull(task_ids="extract_and_save", key="plan_paths")

    with open(changes_path, "r", encoding="utf-8") as f:
        data_transformed_raw = transform_raw_data(f.read())
    logger.info(f"Änderungen transformiert: {len(data_transformed_raw)} Einträge")

    plan_dict = {}
    for plan_path in plan_paths:
        with open(plan_path, "r", encoding="utf-8") as f:
            plan_dict.update(transform_plan(f.read()))
    logger.info(f"Plan transformiert: {len(plan_dict)} Einträge")

    joined_data = join_plan_and_changes(data_transformed_raw, plan_dict)
    logger.info(f"Zusammengefügt: {len(joined_data)} Einträge")

    joined_path = save_transformed_data(joined_data, "joined")
    ti.xcom_push(key="joined_path", value=str(joined_path))


def load_to_warehouse(ti=None):
    joined_path = ti.xcom_pull(task_ids="transform_and_save", key="joined_path")
    conn = init_warehouse()
    with open(joined_path, "r", encoding="utf-8") as f:
        data_loaded = json.load(f)
    count_before = conn.execute("SELECT COUNT(*) FROM departures").fetchone()[0]
    insert_departures(conn, data_loaded)
    count_after = conn.execute("SELECT COUNT(*) FROM departures").fetchone()[0]
    inserted = count_after - count_before
    skipped = len(data_loaded) - inserted
    logger.info(f"Geladen: {inserted} neu, {skipped} übersprungen (Duplikate), {count_after} gesamt")
