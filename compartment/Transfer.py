from compartment.Model import Model

ERRCODE = {
    'SUCCEED': 0
}


def init_compartment(model: Model, name2value: dict):
    for name in name2value.keys():
        r = model.set_compartment(name, name2value[name])
        if r != ERRCODE['SUCCEED']:
            return r
    return ERRCODE['SUCCEED']


def set_path_parameters(model: Model, pre_name: str, next_name: str, use_embedding: bool, parameter=None,
                        parameters=None):
    return model.set_path_parameters(pre_name, next_name, use_embedding, parameter, parameters)
