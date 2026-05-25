import xml.etree.ElementTree as ET
from datetime import datetime


def parse_time (time: str | None) -> str | None:
    if time is None:
        return None 
    dt = datetime.strptime(time, "%d%m%y%H%M")
    return dt.strftime("%Y-%m-%d %H:%M")

def calculate_delay (pt: str | None, ct: str | None) -> int | None:
    if pt is None or ct is None:
        return None
    pt = datetime.strptime(pt, "%d%m%y%H%M")
    ct = datetime.strptime(ct, "%d%m%y%H%M")
    verspaetung = (ct - pt).seconds // 60
    return verspaetung 

def transform_raw_data ( data: str,) -> list[dict]:
    root = ET.fromstring(data)
    new_list = []
    for s in root:
        if s.find("dp") is not None:
            dp = s.find("dp")
            if dp.get("fb") is not None or dp.get("l") is not None:
                new_list.append({"zug": dp.get("fb"),
                             "geplante_zeit": parse_time(dp.get("pt")),
                             "tatsaechliche_zeit": parse_time(dp.get("ct")),
                             "gleis": dp.get("pp"),
                             "linie": dp.get("l"),
                             "richtung": dp.get("ppth"),
                             "verspaetung_min" : calculate_delay(dp.get("pt"), dp.get("ct"))
                             })
    return new_list   
