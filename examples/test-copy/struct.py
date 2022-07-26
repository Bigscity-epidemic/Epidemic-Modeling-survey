from compartment.Graph import Graph
from compartment.Model import Model
from compartment.Descriptor import vertical_divide
from visual.visual_graph import visual_model

graph = Graph('basic_SEIR','S')
vertical_divide(graph,'S',['E','I','R'])
model = Model('basic_SEIR',graph)
visual_model(model)