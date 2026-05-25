from ingestion.extract import get_station 
from ingestion.extract import get_changes
from ingestion.extract import get_plan
from ingestion.load import save_raw_data
from ingestion.load import save_transformed_data
from transformation.transform import transform_raw_data
from transformation.transform import transform_plan
from transformation.transform import join_plan_and_changes
from utils.logger import get_logger
from ingestion.warehouse import init_warehouse
from ingestion.warehouse import insert_departures


logger = get_logger("main")


station = get_station("München Hbf")
changes_plan = get_changes("8000261")
timetable_plan = get_plan("8000261","260525", "09")


save_raw_data(changes_plan, "changes")
save_raw_data(timetable_plan, "plan")

transformed_data_changes = transform_raw_data(changes_plan)
transformed_data_plan = transform_plan(timetable_plan)

save_transformed_data(transformed_data_changes, "changes")
save_transformed_data(transformed_data_plan, "plan")

joined_data = join_plan_and_changes(transformed_data_changes, transformed_data_plan)
save_transformed_data(joined_data, "joined")

conn = init_warehouse()
insert_departures(conn, joined_data)

result = conn.execute("SELECT COUNT(*) FROM departures").fetchone()
logger.info(f"Einträge in der Datenbank: {result[0]}")


