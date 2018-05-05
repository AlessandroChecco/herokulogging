from apscheduler.scheduler import Scheduler
import requests

sched = Scheduler()

@sched.interval_schedule(minutes=1)
def timed_job():
    r = requests.get('http://www.myapplication.com')
    print 'http://www.myapplication.com'
    print r.status_code

sched.start()

while True:
    pass
