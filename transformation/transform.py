import xml.etree.ElementTree as ET 

def transform_raw_data ( data: str,) -> list[dict]:
    root = ET.fromstring(data)
    new_list = []
    for s in root:
        if s.find("dp") is not None:
            dp = s.find("dp")
            new_list.append({"zug": dp.get("fb"),
                             "geplante_zeit": dp.get("pt"),
                             "tatsaechliche_zeit": dp.get("ct"),
                             "gleis": dp.get("pp"),
                             "linie": dp.get("l"),
                             "richtung": dp.get("ppth")
                             })
    return new_list   
