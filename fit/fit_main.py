from fit.compiler import compile_main
from compartment.Model import Model

def fit_main(model:Model,real_value:dict):
    compile_main(model)

