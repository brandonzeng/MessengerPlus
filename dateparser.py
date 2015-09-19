import datetime
import calendar

def date_parser(date_string):
    date_list = date_string.split(',')
    date_list = date_list[1:]
    for i in range(len(date_list)):
        date_list[i] = date_list[i].strip()
        date_list[i] = date_list[i].split(' ')

    year = int(date_list[1][0])
    month = int(list(calendar.month_abbr).index(date_list[0][0][:3]))
    day = int(date_list[0][1])

    return datetime.date(year, month, day)
    
