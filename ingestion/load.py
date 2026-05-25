from datetime import datetime 

def save_raw_changes (data: str) -> None:
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    file_path = f"data/raw/changes/{timestamp}.xml"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(data)
