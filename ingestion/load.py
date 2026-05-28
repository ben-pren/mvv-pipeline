from datetime import datetime
import json
from pathlib import Path
from utils.logger import get_logger

PROJECT_ROOT = Path(__file__).resolve().parent.parent
logger = get_logger(__name__)

def save_raw_data (data: str, prefix: str) -> Path:
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    file_path = PROJECT_ROOT / "data" / "raw" / prefix / f"{timestamp}.xml"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(data)
    logger.info("Daten roh gespeichert")
    return file_path


def save_transformed_data (data: list | dict, prefix: str) -> Path:
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    file_path = PROJECT_ROOT / "data" / "transformed" / prefix / f"{timestamp}.json"
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    logger.info("Daten transformiert gespeichert")
    return file_path