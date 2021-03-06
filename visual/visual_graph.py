import networkx as nx
import matplotlib.pyplot as plt
from compartment.Graph import Graph
from compartment.Model import Model


def visual_graph(graph: Graph):
    G = nx.MultiDiGraph()
    edge_list = []
    for node_name in graph.name2node.keys():
        node = graph.name2node[node_name]
        for next_name in node.next_name_list:
            edge_list.append((node_name, next_name))
    G.add_edges_from(edge_list)

    plt.figure(figsize=(8, 8))
    nx.draw(G, with_labels=True)
    plt.show()


def visual_model(model: Model):
    G = nx.MultiDiGraph()
    edge_list = []
    for node_name in model.name2compartments.keys():
        node = model.name2compartments[node_name].node
        for next_name in node.next_name_list:
            edge_list.append((node_name, next_name))
    G.add_edges_from(edge_list)

    plt.figure(figsize=(8, 8))
    pos = nx.planar_layout(G, scale=2)
    nx.draw(G, pos,
            cmap=plt.cm.tab10,
            font_color="#FFFFFF",
            node_color=range(10, len(G.nodes) + 10),
            font_size=15, node_size=2000, with_labels=True)
    plt.show()
