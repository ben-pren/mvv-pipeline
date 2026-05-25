from ingestion.extract import get_station 
from ingestion.extract import get_changes
from ingestion.extract import get_plan
from ingestion.load import save_raw_data
from transformation.transform import transform_raw_data

station = get_station("München Hbf")
changes_plan = get_changes("8000261")
timetable_plan = get_plan("8000261","260525", "09")


save_raw_data(changes_plan, "changes")
save_raw_data(timetable_plan, "plan")
print ("Daten Bronze erfolgreich gespeichert")

transformed_data = transform_raw_data(changes_plan)
print ("Daten erfolgreich transformiert")
print (transformed_data)

