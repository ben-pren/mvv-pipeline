import os
import requests

from dotenv import load_dotenv 
load_dotenv()

client = os.getenv("DB_CLIENT_ID")
key = os.getenv("DB_API_KEY")

if client is None or key is None:
    raise ValueError("DB_CLIENT_ID oder DB_API_KEY fehlt in .env")

def get_station(station: str) -> str:
    url= f"https://apis.deutschebahn.com/db-api-marketplace/apis/timetables/v1/station/{station}"
    headers = {
        "DB-Client-ID": client,
        "DB-Api-Key": key,
        "accept": "application/xml"
    }
    
    response = requests.get(url, headers=headers)
    return response.text 