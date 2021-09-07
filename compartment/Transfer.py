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


def set_path_exp(model: Model, pre_name: str, next_name: str, exp: str):
    return model.set_path_exp(pre_name, next_name, exp)


def set_path_parameters(model: Model, pre_name: str, next_name: str, parameter_name: str, parameter: float = None,
                        embedding: list = None):
    return model.set_path_parameters(pre_name, next_name, parameter_name, parameter, embedding)
