import datetime
import os
import wget
from parameters.GraphData import GraphData
import ssl
ssl._create_default_https_context = ssl._create_unverified_context


def get_germany_mobility(graph_en: str):
    out = 'datasets/mobility_counties_2019_baseline.csv'
    url = 'https://files.de-1.osf.io/v1/resources/n53cz/providers/osfstorage/5f2d5f5c021ce20041f429f4?action=download&direct&version=1'
    if not os.path.exists(out):
        wget.download(url, out)
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

