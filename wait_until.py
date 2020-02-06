import datetime
from time import sleep

def wait_until(time):   # wait until given time
    print('target time:\t{}'.format(time))
    now = datetime.datetime.now()
    while now < time - datetime.timedelta(seconds=2):
        # slow count down (to save computing power)
        now = datetime.datetime.now()
        print('\rNow:\t\t{}'.format(now), end='')
        sleep(1)
    while now < time:
        # quick coubt down
        now = datetime.datetime.now()
        print('\rNow:\t\t{}'.format(now), end='')
    print()