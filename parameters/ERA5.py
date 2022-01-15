import datetime
import os
from parameters.ArrayData import ArrayData


def get_ERA_2019(kind: str, start_date: datetime.date, length: int, area_en: str = None, area_iso3: str = None):
    out = 'datasets/' + kind + '.csv'
    if not os.path.exists(out):
        return None
    if area_en is None and area_iso3 is None:
        return None
    file = open(out)
    file.readline()
    for line in file.readlines():
        en = line.split(',')[1].replace('\"', '')
        iso3 = line.split(',')[0].replace('\"', '')
        if en == area_en or iso3 == area_iso3:
            data = line.split(',')[2:]
            delta = start_date - datetime.date(2019, 1, 1)
            data = data[delta.days:delta.days + length]
            data_float = []
            for item in data:
                data_float.append(float(item.replace('\"', '')))
            return ArrayData(data_float, start_date, area_en=area_en, area_iso3=area_iso3)
    return None
