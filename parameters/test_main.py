from parameters.Oxford_government_response import get_oxford_government_response, clear_oxford_log
import datetime

r = get_oxford_government_response(datetime.date(2020, 5, 1), 10, 'France')
print(r.data)
