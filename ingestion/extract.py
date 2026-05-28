import os
import requests
from dotenv import load_dotenv 
from utils.logger import get_logger


logger = get_logger(__name__)
load_dotenv()

client = os.getenv("DB_CLIENT_ID")
key = os.getenv("DB_API_KEY")

if client is None or key is None:
    raise ValueError("DB_CLIENT_ID oder DB_API_KEY fehlt in .env")

def get_station(station: str) -> str:
    url = f"https://apis.deutschebahn.com/db-api-marketplace/apis/timetables/v1/station/{station}"
    headers = {
        "DB-Client-ID": client,
        "DB-Api-Key": key,
        "accept": "application/xml"
    }
    
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    logger.info(f"Station Suche fuer '{station}' fertiggestellt")
    return response.text



def get_changes (eva_no: str) -> str:
    url = f"https://apis.deutschebahn.com/db-api-marketplace/apis/timetables/v1/fchg/{eva_no}"
    headers = {
        "DB-Client-ID": client,
        "DB-Api-Key": key,
        "accept": "application/xml"
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    logger.info(f"Aenderungen geholt fuer station {eva_no}")
    return response.text



def get_plan (eva_no: str, date: str, hour: str) -> str:
    url = f"https://apis.deutschebahn.com/db-api-marketplace/apis/timetables/v1/plan/{eva_no}/{date}/{hour}"
    headers = {
        "DB-Client-ID": client,
        "DB-Api-Key": key,
        "accept": "application/xml"
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    logger.info(f"Plan geholt fuer station {eva_no}, datum {date}, stunde {hour}")
    return response.text

