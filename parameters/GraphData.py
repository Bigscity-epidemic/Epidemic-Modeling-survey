import datetime


class GraphData:
    time_length = 0
    start_date = None
    graph_zh = None
    graph_en = None

    data = {}

    '''
    {
        time:[ 
            {
                "properties": {
                    "property_name": "property_value"
                    ...
                    },
                geometry:{
                    "type": "Point"/"MultiPoint"/"LineString...(参考geojson),
                    "coordinates":[]
                }
            },
            ...
            ],
        ...  
    }
    '''


    def __init__(self, data: dict, start_date: datetime.date = None, graph_zh: str = None, graph_en: str = None):
        self.data = data
        if start_date is not None:
            self.start_date = start_date
        if graph_zh is not None:
            self.area_zh = graph_zh
        if graph_en is not None:
            self.area_en = graph_en
        self.length = len(data)


