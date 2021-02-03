import datetime
import argparse
from time import sleep
from account import account
from agent import Agent
from wait_until import wait_until


parser = argparse.ArgumentParser()
parser.add_argument('-t', '--time', type=int,
                    help='Start time. e.g. 18 refers to 18:00')
parser.add_argument('-d', '--date',
                    help='Date. e.g. 20191023 refers to 2019/10/23')
parser.add_argument('-o', '--order', type=str, default='56781234',
                    help='Field order you would like to reserve. Default: 56781234')
args = parser.parse_args()

# Booking information
time_slot = str(int(args.time - 6))  # 07:00 refers to time slot 1
date = str(args.date)

# year, month, date, hour, minute, second, microsecond
start_time = datetime.datetime(int(date[:4]), int(date[4:6]), int(
    date[6:8]), args.time, 0, 0, 0) - datetime.timedelta(days=3)
end_time = start_time + datetime.timedelta(seconds=1.5)

# Log in account
wait_until(start_time - datetime.timedelta(minutes=1))
agent = Agent()
agent.log_in(account['account'], account['password'])

# field order
field_order = [int(item) for item in list(args.order)
               ]      # Default [5,6,7,8,1,2,3,4]
available_field = agent.search_available_field(date, time_slot)
field_order = [str(item) for item in field_order if item in available_field]

# Book
wait_until(start_time - datetime.timedelta(seconds=0.1))
counter = 0     # Number of booked field
stop = False
while datetime.datetime.now() < end_time:
    for field in field_order:
        if agent.book_field(date, time_slot, field):
            counter += 1
            if counter >= 2:
                print(datetime.datetime.now())
                stop = True
                break
    if stop:
        break

if datetime.datetime.now() > end_time:
    for field in field_order:
        if agent.book_field(date, time_slot, field):
            counter += 1
            if counter >= 2:
                print(datetime.datetime.now())
                stop = True
                break
