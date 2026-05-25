from ingestion.extract import get_station 
from ingestion.extract import get_changes
from ingestion.load import save_raw_changes

result = get_station("München Hbf")

result_new = get_changes("8000261")

save_raw_changes(result_new)
print ("Daten Bronze erfolgreich gespeichert")