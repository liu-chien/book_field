import datetime
import argparse
from time import sleep
from account import account
from book_field import Agent
from wait_until import wait_until
from send_email.send_book_result import send_book_result

parser = argparse.ArgumentParser()
parser.add_argument('-t', '--time', type=int, help='Start time. e.g. 18 refers to 18:00')
parser.add_argument('-d', '--date', help='Date. e.g. 20191023 refers to 2019/10/23')
parser.add_argument('-o', '--order', help='Not yet be implemented.')
parser.add_argument('-s', '--email', action='store_true', help='Activate sending email automatically.')
args = parser.parse_args()

# Booking information
time_slot = int(args.time - 6)  # 07:00 refers to time slot 1
date = args.date

# year, month, date, hour, minute, second, microsecond
start_time = datetime.datetime(int(date[:4]), int(date[4:6]), int(date[6:8]), args.time, 0, 0, 0) - datetime.timedelta(days=3)
end_time = start_time + datetime.timedelta(seconds=1.5)

# field order
field_order = [5,6,7,8,1,2,3,4]

# Log in account
wait_until(start_time - datetime.timedelta(minutes=1))
agent = Agent(time_slot, date, account['account'], account['password'])

# Book
wait_until(start_time - datetime.timedelta(seconds=0.1))
counter = 0     # Number of booked field
stop = False
while datetime.datetime.now() < end_time:
    for field in field_order:
        if agent.book_field(field):
            counter += 1
            if counter >= 2:
                print(datetime.datetime.now())
                stop = True
                break
    if stop:
        break

# Send email notification
if args.email:
    send_book_result(args.date, args.time, counter)