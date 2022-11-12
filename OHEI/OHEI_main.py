from OHEI_executor import dataloader_OHEI_model, execute_OHEI_model
from OHEI_eval import eval_OHEI
from json import dump

if __name__ == '__main__':
    vacc_out_pool = ['less', 'normal', 'more', 'most']
    area_pool = ['United Kingdom', 'France', 'Egypt', 'Belgium', 'Brazil', 'Canada', 'Denmark', 'Afghanistan']
    vacc_pri_pool = ['V+', 'V20', 'V60', 'V75']
    time_length = 30
    start_date = '20200801'

    result_exp = {}
    popu, epi1, contact, init_vacc, mobility, policy, gdp = dataloader_OHEI_model()

    for vacc_out in vacc_out_pool:
        result_exp[vacc_out] = {}
        for area in area_pool:
            print(vacc_out, area)
            result_exp[vacc_out][area] = {}
            for vacc_pri in vacc_pri_pool:
                results, dailynew, vp, gdp_per = execute_OHEI_model(start_date, time_length, area, popu, epi1, contact,
                                                                    mobility, policy, init_vacc, vacc_out, vacc_pri,
                                                                    gdp)
                death_whole, infected_whole, cLE_loss, cQALY_loss, HC_loss = eval_OHEI(dailynew, vp, gdp_per)
                result_exp[vacc_out][area][vacc_pri] = {'mortality': death_whole,
                                                        'morbidity': infected_whole,
                                                        'cLE': cLE_loss,
                                                        'cQALY': cQALY_loss,
                                                        'HC': HC_loss}

    print(result_exp)
    dump(result_exp, open('OHEI_result.json', 'w', encoding='utf8'))
