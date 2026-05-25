from datetime import datetime 
import json

def save_raw_data (data: str, prefix: str) -> None:
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    file_path = f"data/raw/{prefix}/{timestamp}.xml"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(data)


def save_transformed_data (data: list | dict, prefix: str) -> None:
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    file_path = f"data/transformed/{prefix}/{timestamp}.json"
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
