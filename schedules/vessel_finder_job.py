import time
import schedule
from tzlocal import get_localzone
import threading
from app.tasks.scrape_vessel_finder import ScrapeVesselFinderTask 

class VesselFinderJob():
    def __init__(self):
        self.scheduler = schedule.Scheduler()
        # https://superfastpython.com/kill-a-thread-in-python/#Need_to_Kill_a_Thread
        self.thread_shared_event_cease_continuous_run = threading.Event()

    def entry(self):
        job = ScrapeVesselFinderTask()
        
        self.scheduler.every().monday.at("04:35", str(get_localzone())).do(job.execute)
        self.scheduler.every().tuesday.at("04:32", str(get_localzone())).do(job.execute)
        self.scheduler.every().wednesday.at("04:28", str(get_localzone())).do(job.execute)
        self.scheduler.every().thursday.at("04:31", str(get_localzone())).do(job.execute)
        self.scheduler.every().friday.at("04:32", str(get_localzone())).do(job.execute)

        self.thread = threading.Thread(target=self.run)
        self.thread.start()

    def run(self):
        while True:
            n = self.scheduler.idle_seconds
            if n is None:
                # no more jobs
                break
            elif n > 0:
                # sleep exactly the right amount of time
                time.sleep(n)

            if self.thread_shared_event_cease_continuous_run.is_set():
                self.thread.join()
                break

            self.scheduler.run_pending()
