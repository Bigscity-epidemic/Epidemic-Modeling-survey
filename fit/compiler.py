from compartment.Model import Model
from compartment.Compartment import Compartment
from compartment.Path import Path


def compile_main(model: Model):
    name2compartments = model.name2compartments
    name2paths = model.name2paths
    compartments = name2compartments.keys()
    paths = name2paths.keys()
    parameters = {}
    for path_name in paths:
        for parameter in name2paths[path_name].name2parameters.keys():
            if parameter not in parameters.keys():
                parameters[parameter] = 0
    parameters = parameters.keys()

    python = open('formula.py', 'w', encoding='utf8')

    head = 'import numpy as np\n\n\n'
    python.write(head)

    line1 = r'def formula(INPUT, t'
    for parameter in parameters:
        line1 += ', ' + parameter
    line1 += '):\n'
    python.write(line1)

    line2 = r'    Y = np.zeros(' + str(len(compartments)) + ')\n'
    python.write(line2)

    index = 0
    for compartment in compartments:
        line3 = '    ' + compartment + ' = INPUT[' + str(index) + ']\n'
        python.write(line3)
        index += 1
    
