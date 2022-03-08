

class ProfileData:
    area_zh = None
    area_en = None
    feature2value = None




    def __init__(self, data: dict, area_zh: str = None, area_en: str = None):
        self.feature2value = data
        if area_zh is not None:
            self.area_zh = area_zh
        if area_en is not None:
            self.area_en = area_en
        self.length = len(data)
