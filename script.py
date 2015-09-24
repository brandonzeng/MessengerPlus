import parser
import scores
    
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

print "top_X_reconnects"
print top_X_reconnects

def get_individual(result, individual):
    dates = {}
    for date in result[individual]:
        if date in dates:
            dates[date] += 1
        else:
            dates[date] = 1
    return dates

def get_aggregate(result):
    dates = {}
    for key in result:
        for date in result[key]:
            if date in dates:
                dates[date] += 1
            else:
                dates[date] = 1
    return dates
    
import plotly.plotly as py
from plotly.graph_objs import *

from datetime import datetime

dates = get_aggregate(result)
friend = get_individual(result, "Paolo Gentili")
data = Data([
    Scatter(
        x = sorted(dates.keys()),
        y = [dates[i] for i in sorted(dates.keys())]
    ),
    Scatter(
        x = sorted(sicong.keys()),
        y = [sicong[i] for i in sorted(sicong.keys())]
    )
])
layout = Layout(
    title = ", ".join([i[0] for i in top_X_reconnects])
)
plot_url = py.plot(data, filename='python-datetime')
print title
print plot_url