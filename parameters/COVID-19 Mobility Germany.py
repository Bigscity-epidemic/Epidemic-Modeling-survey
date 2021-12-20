import datetime
import os
import wget
from parameters.GraphData import GraphData
import ssl
ssl._create_default_https_context = ssl._create_unverified_context


def get_germany_mobility(graph_en: str):
    out = 'Germany/mobility_counties_2019_baseline.csv'
    url = 'https://files.de-1.osf.io/v1/resources/n53cz/providers/osfstorage/5f2d5f5c021ce20041f429f4?action=download&direct&version=1'
    if not os.path.exists(out) or not os.path.exists('log/' + datetime.date.today().strftime('%Y-%m-%d') + '.germany'):
        if os.path.exists(out):
            os.remove(out)
        wget.download(url, out)
        log = open('log/' + datetime.date.today().strftime('%Y-%m-%d') + '.germany', 'w')
    file = open(out)
    file.readline()
    data = {}
    for line in file.readlines():
        line_data = line[:-1].split(',')
        time = line_data[0]
        if time not in data:
            data[time] = []
        dict_temp = {
            'properties': {},
            'geometry': {
                "type": "Point",
                "coordinates": [],
            }
        }
        dict_temp['properties']['mobility'] = line_data[3]
        dict_temp['geometry']['coordinates'] = [line_data[1], line_data[2]]
        data[time].append(dict_temp)
    return GraphData(data, graph_en=graph_en)


def clear_germany_log():
    files = []
    for file in os.walk('log/'):
        files = file[2]
    for filename in files:
        if filename.split('.')[-1] == 'germany':
            os.remove('log/' + filename)
