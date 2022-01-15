import datetime
import os
import wget
from parameters.ArrayData import ArrayData


def get_oxford_government_response(start_date: datetime.date, length: int, area_en: str):
    out = 'datasets/oxford_government_response.csv'
    url = 'https://raw.githubusercontent.com/OxCGRT/covid-policy-tracker/master/data/timeseries/government_response_index.csv'
    if not os.path.exists(out):
        wget.download(url, out)
    file = open(out)
    file.readline()
    for line in file.readlines():
        en = line.split(',')[2].replace('\"', '')
        if en == area_en:
            data = line.split(',')[3:]
            delta = start_date - datetime.date(2020, 1, 20)
            data = data[delta.days:delta.days + length]
            data_float = []
            for item in data:
                data_float.append(float(item.replace('\"', '')))
            return ArrayData(data_float, start_date, area_en=area_en)
    return None

