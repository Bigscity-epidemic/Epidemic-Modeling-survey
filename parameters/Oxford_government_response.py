import datetime
import os
import wget
from parameters.ArrayData import ArrayData


def get_oxford_government_response(start_date: datetime.date, length: int, area_en: str):
    out = 'oxford/oxford_government_response.csv'
    url = 'https://raw.githubusercontent.com/OxCGRT/covid-policy-tracker/master/data/timeseries/government_response_index.csv'
    if not os.path.exists(out) or not os.path.exists('log/' + datetime.date.today().strftime('%Y-%m-%d') + '.oxford'):
        if os.path.exists(out):
            os.remove(out)
        wget.download(url, out)
        log = open('log/' + datetime.date.today().strftime('%Y-%m-%d') + '.oxford', 'w')
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


def clear_oxford_log():
    files = []
    for file in os.walk('log/'):
        files = file[2]
    for filename in files:
        if filename.split('.')[-1] == 'oxford':
            os.remove('log/' + filename)
