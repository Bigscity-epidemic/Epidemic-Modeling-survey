from compartment.Model import Model


def visual_compartment_values(model: Model):
    for compartment_name in model.name2compartments.keys():
        compartment = model.name2compartments[compartment_name]
        print(compartment.node.name + ' : ' + str(compartment.value))
