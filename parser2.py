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

with open ("messages.txt", "r") as myfile:
    data = myfile.read()

result = parse(data)
scores = []
for key in result:
	scores.append((key, len(result[key])))
scores = sorted(scores, key = lambda x: x[1], reverse = True)
print scores



"""
"""

import plotly.plotly as py
from plotly.graph_objs import *

from datetime import datetime
dates = {}
for key in result:
	for date in result[key]:
		if date in dates:
			dates[date] += 1
		else:
			dates[date] = 1
x = sorted(dates.keys())
data = Data([
    Scatter(
        x = x,
        y = [dates[i] for i in x]
    ),
])
plot_url = py.plot(data, filename='python-datetime')
print plot_url