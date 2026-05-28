import xml.etree.ElementTree as ET
from datetime import datetime
from utils.logger import get_logger

logger = get_logger(__name__)


def parse_time (time: str | None) -> str | None:
    if time is None:
        return None 
    dt = datetime.strptime(time, "%y%m%d%H%M")
    return dt.strftime("%Y-%m-%d %H:%M")

def calculate_delay (pt: str | None, ct: str | None) -> int | None:
    if pt is None or ct is None:
        return None
    pt = datetime.strptime(pt, "%y%m%d%H%M")
    ct = datetime.strptime(ct, "%y%m%d%H%M")
    verspaetung = (ct - pt).seconds // 60
    return verspaetung 

def transform_raw_data ( data: str) -> list[dict]:
    root = ET.fromstring(data)
    new_list = []
    for s in root:
        if s.find("dp") is not None:
            dp = s.find("dp")
            if dp.get("fb") is not None or dp.get("l") is not None:
                if dp.get("pt") is not None or dp.get("ct") is not None:
                    new_list.append({"zug": dp.get("fb"),
                             "geplante_zeit": parse_time(dp.get("pt")),
                             "tatsaechliche_zeit": parse_time(dp.get("ct")),
                             "gleis": dp.get("pp"),
                             "linie": dp.get("l"),
                             "richtung": dp.get("ppth"),
                             "verspaetung_min" : calculate_delay(dp.get("pt"), dp.get("ct")),
                             "id": s.get("id"),
                             "ct_raw": dp.get("ct")
                             })
    return new_list   

def transform_plan (data: str) -> dict:
    root = ET.fromstring(data)
    plan_dict = {}
    for s in root:
        stop_id = s.get("id")
        dp = s.find("dp")
        if stop_id is not None and dp is not None:
            plan_dict[stop_id] = dp.get("pt")
    return plan_dict

def join_plan_and_changes (changes: list[dict], plan: dict):
    list_verspaetung = []
    for eintrag in changes:
        pt_plan = plan.get(eintrag["id"])
        if pt_plan is not None and eintrag["geplante_zeit"] is None:
            eintrag["geplante_zeit"] = parse_time(pt_plan)
            eintrag["verspaetung_min"] = calculate_delay(pt_plan, eintrag["ct_raw"])
        list_verspaetung.append(eintrag)
    list_verspaetung = [e for e in list_verspaetung if e["geplante_zeit"] is not None or e["tatsaechliche_zeit"] is not None]
    logger.info("Daten zusammengefügt")
    return list_verspaetung

