from threading import Thread
import schedule
import time
from threading import Thread

class Scheduler:
    def __init__(self):
        print('scheduler initialised')
        self.t1 = Thread(target=self.start_fn)
        self.t1.start()
    
    def schedule_task(self, fn, interval = 60):
        schedule.every(interval).minutes.do(fn)
    
    def start_fn(self):
        while True:
            print('scheduler running')
            schedule.run_pending()
            time.sleep(1)
