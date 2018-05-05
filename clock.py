from apscheduler.scheduler import Scheduler
import requests

sched = Scheduler()

@sched.interval_schedule(minutes=10)
def timed_job():
    r = requests.get('https://fast-logging.herokuapp.com/')
    print 'KEEPING ALIVE'
    print r.status_code

sched.start()

while True:
    pass
