from fit.compiler import compile_main, compile_loss, compile_optim
from compartment.Model import Model


def fit_main(model: Model, real_value: dict):
    parameters = compile_main(model)
    compile_loss(real_value, model.name2compartments)
    compile_optim(len(model.name2compartments.keys()), len(parameters))
