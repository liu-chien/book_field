import datetime
import argparse
from time import sleep
from account import account
from book_field import book_field

parser = argparse.ArgumentParser()
parser.add_argument('-t', '--time', type=int, help='Start time. e.g. 18 refers to 18:00')
parser.add_argument('-d', '--date', help='Date. e.g. 20191023 refers to 2019/10/23')
parser.add_argument('-o', '--order', help='Not yet be implemented.')
args = parser.parse_args()

# Booking information
time_slot = int(args.time - 6)       # 07:00 refers to time slot 1
date = args.date

# year, month, date, hour, minute, second, microsecond
start_time = datetime.datetime(int(date[:4]), int(date[4:6]), int(date[6:8]), args.time, 0, 0, 0) - datetime.timedelta(days=3, microseconds=1e5)
end_time = start_time + datetime.timedelta(seconds=2)

# field order
field_order = [5,6,7,8,1,2,3,4]

def check_time(time):
    print('target time:\t{}'.format(time))
    now = datetime.datetime.now()
    while now < time - datetime.timedelta(seconds=1, microseconds=5e5):
        now = datetime.datetime.now()
        print('\rNow:\t\t{}'.format(now), end='')
        sleep(1)
    while now < time:
        now = datetime.datetime.now()
        print('\rNow:\t\t{}'.format(now), end='')
    print()

check_time(start_time)

counter = 0     # Number of booked field
stop = False
while datetime.datetime.now() < end_time:
    for field in field_order:
        if book_field(field, time_slot, date, account['account'], account['password']):
            counter += 1
            if counter >= 2:
                stop = True
                break
    if stop:
        break


    

