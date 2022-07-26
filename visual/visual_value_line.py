from matplotlib import pyplot as plt


def plot_line(values,log=False,linestyle=None):
    plt.figure()
    if log:
        plt.yscale('log')
    for name in values:
        plt.plot(values[name], label=name, linestyle = linestyle)
    plt.legend()
    plt.show()
