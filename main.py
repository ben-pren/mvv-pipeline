from ingestion.extract import get_station 
from ingestion.extract import get_changes
from ingestion.load import save_raw_changes
from transformation.transform import transform_raw_data

result = get_station("München Hbf")

result_new = get_changes("8000261")

save_raw_changes(result_new)
print ("Daten Bronze erfolgreich gespeichert")

transformed_data = transform_raw_data(result_new)
print ("Daten erfolgreich transformiert")
print (transformed_data)

