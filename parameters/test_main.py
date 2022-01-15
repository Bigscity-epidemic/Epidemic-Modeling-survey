from parameters.Oxford_government_response import get_oxford_government_response
from parameters.Mobility_Germany import get_germany_mobility
from parameters.ERA5 import get_ERA_2019
import datetime

r = get_oxford_government_response(datetime.date(2020, 5, 1), 10, 'France')
r = get_germany_mobility('a')
r = get_ERA_2019('tavg', datetime.date(2019, 1, 5), 10, 'Albania')
print(r.data)
