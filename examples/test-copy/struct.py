from compartment.Graph import Graph
from compartment.Model import Model
from executor.Executor import Executor
from compartment.Descriptor import vertical_divide
from compartment.Transfer import init_compartment, set_path_exp, set_path_parameters
from visual.visual_graph import visual_model
from visual.visual_model_data import visual_compartment_values

graph = Graph('basic_SEIR', 'S')
vertical_divide(graph, 'S', ['E', 'I', 'R'])
model = Model('basic_SEIR', graph)
visual_model(model)