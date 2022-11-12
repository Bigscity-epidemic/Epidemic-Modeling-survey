from compartment.Model import Model


class Executor:
    model = None

    def __init__(self, model: Model):
        self.model = model

    def simulate_step(self, index: int, probe_compartments=None):
        probe_results = {}
        if probe_compartments is not None:
            for compartment_name in probe_compartments:
                probe_results[compartment_name] = 0.0

        path2value = {}
        for pathname in self.model.name2paths.keys():
            pre_name = pathname.split('-')[0]
            path = self.model.name2paths[pathname]
            exp = '+' + path.expression

            value = 0.0

            i = 0
            while i < len(exp):
                op = exp[i]
                j = i + 1
                while j < len(exp) and exp[j] != '+':
                    j += 1
                term = exp[i + 1:j]
                term_value = 1.0
                variables = term.split('*')
                for variable in variables:
                    if variable[0].isupper():
                        term_value *= self.model.name2compartments[variable].value
                    else:
                        if path.name2parameters[variable][0] == 'single':
                            term_value *= path.name2parameters[variable][1]
                        else:
                            term_value *= path.name2parameters[variable][1][index]

                i = j
                value += term_value

            if self.model.name2compartments[pre_name].value <= value:
                value = self.model.name2compartments[pre_name].value
            self.model.name2compartments[pre_name].value -= value
            path2value[pathname] = value
        for pathname in path2value.keys():
            next_name = pathname.split('>')[1]
            self.model.name2compartments[next_name].value += path2value[pathname]

            if next_name in probe_results.keys():
                probe_results[next_name] += path2value[pathname]

        return probe_results
