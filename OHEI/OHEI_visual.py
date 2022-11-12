from json import load


def visual_table():
    json_result = load(open('OHEI_result.json', encoding='utf8'))
    result_out_eval = {}
    for vacc_out in ['less', 'normal', 'more', 'most']:
        result_out_eval[vacc_out] = {}
        for eval_index in ['mortality', 'morbidity', 'cLE', 'cQALY', 'HC']:
            result_area_pri = {}
            for area in ['United Kingdom', 'France', 'Egypt', 'Belgium', 'Brazil', 'Canada', 'Denmark', 'Afghanistan']:
                result_area_pri[area] = {}
                for vacc_pri in ['V+', 'V20', 'V60', 'V75']:
                    result_area_pri[area][vacc_pri] = json_result[vacc_out][area][vacc_pri][eval_index]

            best_count = {}
            best_figure = 0
            for vacc_pri in ['V+', 'V20', 'V60', 'V75']:
                best_count[vacc_pri] = 0

            for area in result_area_pri.keys():
                min_eval = 2147483647.0
                for vacc_pri in ['V+', 'V20', 'V60', 'V75']:
                    min_eval = min(min_eval, result_area_pri[area][vacc_pri])
                for vacc_pri in ['V+', 'V20', 'V60', 'V75']:
                    if result_area_pri[area][vacc_pri] == min_eval:
                        best_count[vacc_pri] += 1

            for vacc_pri in ['V+', 'V20', 'V60', 'V75']:
                best_figure = max(best_figure, best_count[vacc_pri])
            result_str = ''
            for vacc_pri in ['V+', 'V20', 'V60', 'V75']:
                if best_count[vacc_pri] == best_figure:
                    result_str += vacc_pri
            result_out_eval[vacc_out][eval_index] = result_str
    return result_out_eval


if __name__ == '__main__':
    roe = visual_table()
    tmp = open('tmp.csv', 'w', encoding='utf8')
    tmp.write('Evaluation Index,mortality,morbidity,cLE,cQALY,HC\n')
    index = 1
    for vacc_out in roe.keys():
        tmp.write('R' + str(index))
        for eval_index in roe[vacc_out].keys():
            tmp.write(',' + roe[vacc_out][eval_index])
        index += 1
        tmp.write('\n')
