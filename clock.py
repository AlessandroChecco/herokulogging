from apscheduler.scheduler import Scheduler
import requests
import os

sched = Scheduler()

@sched.interval_schedule(minutes=1)
def timed_job():
    print 'try'
    r = requests.get(os.environ.get('CURRENTDOMAIN'))
    print 'KEEPING ALIVE: '+os.environ.get('CURRENTDOMAIN')
    print r.status_code

sched.start()

while True:
    pass
