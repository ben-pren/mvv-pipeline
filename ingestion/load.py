from datetime import datetime 

def save_raw_data (data: str, prefix: str) -> None:
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    file_path = f"data/raw/{prefix}/{timestamp}.xml"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(data)
