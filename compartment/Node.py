ERRCODE = {
    'SUCCEED': 0,
    'NO_DUPLICATED_EDGE': 4
}


class Node:
    name = ''
    next_name_list = {}

    def __init__(self, name: str):
        self.name = name
        self.next_name_list = {}

    def add_next(self, name: str):
        if name in self.next_name_list.keys():
            return ERRCODE['NO_DUPLICATED_EDGE']
        self.next_name_list[name] = 0
        return ERRCODE['SUCCEED']
