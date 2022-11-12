from OHEI_executor import dataloader_OHEI_model, execute_OHEI_model
from OHEI_Death import get_death
from OHEI_infected import get_infected
from OHEI_cLE import get_cLE
from OHEI_cQALY import get_cQALY
from OHEI_HC import get_HC


def eval_OHEI(dailynew, vp, gdp):
    death_whole, death_array = get_death(dailynew)
    infected_whole, infected_array = get_infected(dailynew)

    cLE_loss, cLE_age = get_cLE(death_array)
    cQALY_loss, cQALY_age = get_cQALY(death_array, infected_array, vp)
    HC_loss, HC_age = get_HC(death_array, gdp)
    return death_whole, infected_whole, cLE_loss, cQALY_loss, HC_loss


if __name__ == '__main__':
    vacc_out_pool = ['less', 'normal', 'more', 'most']
    vacc_pri_pool = ['V+', 'V20', 'V60', 'V75']
    time_length = 30
    start_date = '20200801'
    select_area = 'Egypt'
    vacc_out = vacc_out_pool[2]
    vacc_pri = vacc_pri_pool[2]

    popu, epi1, contact, init_vacc, mobility, policy, gdp = dataloader_OHEI_model()
    results, dailynew, vp, gdp = execute_OHEI_model(start_date, time_length, select_area, popu, epi1, contact, mobility,
                                                    policy, init_vacc, vacc_out, vacc_pri, gdp)
    death_whole, infected_whole, cLE_loss, cQALY_loss, HC_loss = eval_OHEI(dailynew, vp, gdp)
    print(death_whole, infected_whole, cLE_loss, cQALY_loss, HC_loss)
