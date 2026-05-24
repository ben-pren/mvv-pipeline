from ingestion.extract import get_station 
from ingestion.extract import get_changes

result = get_station("München Hbf")
print(result)

result_new = get_changes("8000261")
print(result_new)