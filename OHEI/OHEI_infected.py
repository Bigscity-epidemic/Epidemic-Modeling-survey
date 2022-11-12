def get_infected(results):
    infected_age = {}
    infect_whole=0.0
    for age in results.keys():
        infected_age[age] = results[age]['Ic']
        for item in infected_age[age]:
            infect_whole+=item
    return infect_whole,infected_age
