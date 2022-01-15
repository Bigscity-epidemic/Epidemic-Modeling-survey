import datetime


class ArrayData:
    length = 0
    start_date = None
    area_zh = None
    area_en = None
    area_iso3=None
    data = []

    def __init__(self, data: list, start_date: datetime.date = None, area_zh: str = None, area_en: str = None,area_iso3:str=None):
        self.data = data
        if start_date is not None:
            self.start_date = start_date
        if area_zh is not None:
            self.area_zh = area_zh
        if area_en is not None:
            self.area_en = area_en
        if area_iso3 is not None:
            self.area_iso3 = area_iso3
        self.length = len(data)
