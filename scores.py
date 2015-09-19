import datetime
import calendar
import random

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

def parse(html):
    title = "<title>"
    thread = "<div class=\"thread\">"
    user = "<span class=\"user\">"
    date = "<span class=\"meta\">"
    end = "</p></div>"

    user_start = html.find(title) + len(title)
    user_end = user_start
    while html[user_end] != "<":
        user_end += 1
    user = html[user_start:user_end + 1].split(" ")[1]
     
    messages = {}
    html_index = 0
    while html_index != -1:
        thread_start = html.find(thread, html_index)
        thread_end = html.find(end, thread_start)
        name_start = thread_start + len(thread)
        name_end = name_start
        while html[name_end] != "<":
            name_end += 1
        names = html[name_start:name_end + 1].split(",")
        if len(names) == 2 and (user in names[0] or user in names[1]):
            friend = names[1] if user in names[0] else names[0]
            if friend[0] == " ":
                friend = friend[1:-1]       
            if friend not in messages:
                messages[friend] = []
            date_index = thread_start
            while (date_index != -1):
                date_index = html.find(date, date_index + 1, thread_end)
                if date_index == -1:
                    break
                date_start = date_index + len(date)
                date_end = date_start
                while html[date_end] != "<":
                    date_end += 1
                messages[friend].append(date_parser(html[date_start:date_end + 1]))
        html_index = thread_end
        for friend in messages:
            sorted(messages[friend])
    return messages



def contact_within_past_X_days(message_dict, person, days):
    contact_dates = message_dict[person]
    lastest_contact = max(contact_dates)

    if datetime.date.today().toordinal() - lastest_contact.toordinal() <= 30:
        return True
    else:
        return False
                

def message_freq(message_dict):
    freqs = []       
    for person in message_dict:
        freqs.append((person, len(message_dict[person])))
                
    freqs = sorted(freqs, key = lambda x: x[1], reverse = True)
        
    return freqs


    
with open ("messages.txt", "r") as myfile:
    data = myfile.read().replace('\n', '')

result = parse(data)
message_frequencies = message_freq(result)
    
freqs_dict = {}
for person in message_frequencies:
    freqs_dict[person[0]] = person[1]

num_potential_reconnections = len(message_frequencies)/5

potential_reconnections = message_frequencies[:num_potential_reconnections]

reconnections = []

for i in range(len(potential_reconnections)):
    person = potential_reconnections[i][0]
    if not contact_within_past_X_days(result, person, 30):
        reconnections.append((person, freqs_dict[person]))

total = 0
cumul_reconnect = []
for person in reconnections:
    old_total = total
    total += person[1]
    cumul_reconnect.append((person, old_total, total))
    

top_X_reconnects = set([])
NUM_DESIRED_RECONNECTS = 5
while len(top_X_reconnects) < min(potential_reconnections,NUM_DESIRED_RECONNECTS):
    random_num = random.randint(1,total)
    for person in cumul_reconnect:
        if person[1] <= random_num < person[2]:
            desired_person = person[0]
    top_X_reconnects.add(desired_person)

print top_X_reconnects
    
            


    
