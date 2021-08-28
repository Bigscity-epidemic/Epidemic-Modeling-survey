from compartment.Graph import Graph

# descriptor依次描述了3条指令：纵向细分，横向细分，增加转移路径
# 纵向细分，需要指明待细分的仓室和细分后额外n个仓室的依次名称，只支持1个仓室细分为长度为n+1的链。出现查不到、重名等将报错。会自动建立边
# 横向细分，需要指明待细分的仓室和细分后额外n个仓室的依次名称。只支持1个仓室细分为n+1个并列的仓室，不能横向细分初始仓室，出现查不到、重名等将报错。会自动建立边
# 增加转移路径，需要指明源仓室和目的仓室
ERRCODE = {
    'SUCCEED': 0,
    'NODE_NAME_NOT_FOUND': 1,
    'BLANK_LIST': 5
}


def vertical_divide(graph: Graph, target_node_name: str, divide_name_list: list):
    if len(divide_name_list) == 0:
        return ERRCODE['BLANK_LIST']
    if target_node_name not in graph.name2node.keys():
        return ERRCODE['NODE_NAME_NOT_FOUND']
    target_next_list = graph.name2node[target_node_name].next_name_list.copy()
    last_name = target_node_name
    for divide_name in divide_name_list:
        r = graph.add_next(last_name, divide_name)
        if r != ERRCODE['SUCCEED']:
            return r
        last_name = divide_name
    for next_name in target_next_list.keys():
        r = graph.add_edge(last_name, next_name)
        if r != ERRCODE['SUCCEED']:
            return r
    graph.name2node[target_node_name].next_name_list = {divide_name_list[0]: 0}
    return ERRCODE['SUCCEED']


def horizontal_divide(graph: Graph, target_node_name: str, divide_name_list: list):
    if len(divide_name_list) == 0:
        return ERRCODE['BLANK_LIST']
    if target_node_name not in graph.name2node.keys():
        return ERRCODE['NODE_NAME_NOT_FOUND']
    target_next_list = graph.name2node[target_node_name].next_name_list.copy()
    pre_list = []
    for node_name in graph.name2node.keys():
        node = graph.name2node[node_name]
        if target_node_name in node.next_name_list.keys():
            pre_list.append(node_name)
    for divide_name in divide_name_list:
        r = graph.add_single_node(divide_name)
        if r != ERRCODE['SUCCEED']:
            return r
        for pre in pre_list:
            r = graph.add_edge(pre, divide_name)
            if r != ERRCODE['SUCCEED']:
                return r
        for next_name in target_next_list:
            r = graph.add_edge(divide_name, next_name)
            if r != ERRCODE['SUCCEED']:
                return r
    return ERRCODE['SUCCEED']


def add_path(graph: Graph, from_name: str, to_name: str):
    return graph.add_edge(from_name, to_name)
