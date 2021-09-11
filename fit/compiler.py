from compartment.Model import Model


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

    name2prepath = {}
    name2nextpath = {}
    for compartment in compartments:
        name2prepath[compartment] = []
        name2nextpath[compartment] = []
    for path in paths:
        pre_name = path.split('-')[0]
        next_name = path.split('>')[1]
        name2prepath[next_name].append(path)
        name2nextpath[pre_name].append(path)

    i = 0
    for compartment in compartments:
        line4 = '    Y[' + str(i) + '] = '
        for path in name2prepath[compartment]:
            line4 += '+ (' + name2paths[path].expression + ') '
        for path in name2nextpath[compartment]:
            line4 += '- (' + name2paths[path].expression + ') '
        line4 += '  # d' + compartment + r'/dt' + '\n'
        python.write(line4)
        i += 1

    end = '    return Y\n'
    python.write(end)
    return parameters


def compile_loss(real_value: dict, name2compartments: dict):
    python = open('loss.py', 'w', encoding='utf8')
    head = 'import numpy as np\n\n\ndef get_daily(TRUE, PRED):\n    tmpTrue = TRUE.copy()\n    tmpPred = np.array(' \
           'PRED).copy()\n    for i in range(1, len(TRUE), 1):\n        k = len(TRUE) - i\n        for j in range(' \
           'len(tmpTrue[k])):\n            tmpTrue[k][j] -= tmpTrue[k - 1][j]\n        for j in range(len(tmpPred[' \
           'k])):\n            tmpPred[k][j] -= tmpPred[k - 1][j]\n    for j in range(len(tmpTrue[0])):\n        ' \
           'tmpTrue[0][j] = 0.0\n    for j in range(len(tmpPred[0])):\n        tmpPred[0][j] = 0.0\n    return ' \
           'tmpTrue, tmpPred '
    python.write(head + '\n\n\n')

    line1 = 'def loss(TRUE, PRED):\n    tt, tp = get_daily(TRUE, PRED)\n'
    python.write(line1)

    name2index = {}
    i = 0
    for name in name2compartments.keys():
        name2index[name] = i
        i += 1
    line2 = '    return np.sum('
    i = 0
    for combine in real_value.keys():
        true = 'tt[:, ' + str(i) + ']'
        pred = ''
        for compartment in combine.split('+'):
            index = name2index[compartment]
            pred += 'tp[:, ' + str(index) + '] + '
        pred = pred[:-3]
        line2 += 'np.square((' + true + ') - (' + pred + ')) + '
        i += 1
    line2 = line2[:-3]
    line2 += ')\n'
    python.write(line2)


def compile_optim(compartment: int, parameters: int):
    head = 'from formula import formula\nfrom loss import loss\nimport scipy.integrate as ' \
           'spi\n\n\ndef optim_fun(args):\n    INPUT, t_range, TRUE, kind = args\n'
    python = open('optim.py', 'w', encoding='utf8')
    python.write(head)
    tmp1 = ''
    tmp2 = ''
    for i in range(compartment):
        tmp1 += 'INPUT[' + str(i) + '], '
    tmp1 = tmp1[:-2]
    for i in range(parameters):
        tmp2 += 'x[' + str(i) + '], '
    tmp2 = tmp2[:-2]
    line = '    v = lambda x: loss(TRUE, spi.odeint(formula, (' + tmp1 + '), t_range, args=(' + tmp2 + ')))\n    return v\n'
    python.write(line)
