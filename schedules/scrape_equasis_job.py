import os
import pytz
from tzlocal import get_localzone
import schedule, time, datetime
import dill as pickle
import pandas as pd
import schedules.luigi.build_scrape_equasis
from collections import OrderedDict
from settings import logger
from app.types.job_setting import JobSetting
from constants.job_status import JOB_STATUS
import threading

class ScrapeEquasisJob():
    times = range(24)

    def __init__(
        self,
        name='scrape_equasis_job',
        hours= [
            '00:00',
            '03:00',
            '06:00',
            '09:00',
            '12:00',
            '15:00',
            '18:00',
            '21:00',
        ]
    ):
        self.name = name
        job = self.load()
        if hasattr(job, 'scheduler'):
            self.scheduler = job.scheduler
            self.job_settings = job.job_settings
            self.scheduled_at = job.scheduled_at
            self.thread_shared_event_cease_continuous_run = job.thread_shared_event_cease_continuous_run
        else:
            self.scheduler = schedule.Scheduler()
            self.job_settings = ScrapeEquasisJob.init_job_settings(hours)
            self.scheduled_at = datetime.datetime.now()
            # https://superfastpython.com/kill-a-thread-in-python/#Need_to_Kill_a_Thread
            self.thread_shared_event_cease_continuous_run = threading.Event()

    def init_job_settings(hours):
        job_settings = OrderedDict()
        for time in ScrapeEquasisJob.times:
            starting_at = ('%02d:00' % time)
            job_name = starting_at
            job_settings[job_name] = JobSetting(
                    time=starting_at,
                    is_entried=(starting_at in hours),
                    status='',
                    estimate_time='',
                    actual_time='',
                    queues=0,
                    throughput=0,
                    errors=0,
                )

        return job_settings

    def execute_job(self, job_name):
        self.notify_job_start(job_name=job_name)
        schedules.luigi.build_scrape_equasis.build()
        self.notify_job_end(job_name=job_name)

    def get_name(self):
        return self.name

    def set_all(self, settings=[]):
        job_settings = []
        for setting in settings:
            job_name = setting.time
            job_status_information[job_name] = JobSetting(
                    time=setting.time,
                    is_entried=setting.is_entried,
                )

        self.job_settings = job_settings

    def entry(self):
        for job_name, setting in self.job_settings.items():
            if setting.is_entried:
                """
                Cordinate to OS timezone
                """
                self.scheduler.every().day.at(setting.time, str(get_localzone())).do(self.execute_job, job_name=job_name).tag('hourly-tasks', 'scrape_equasis')
                self.job_settings[job_name].status = JOB_STATUS.WAITING
                self.job_settings[job_name].estimate_time = setting.time
                self.job_settings[job_name].queues = os.getenv('UPPER_LIMIT_SCRAPING_BY_ONE_BATCH')

        self.thread = threading.Thread(target=self.run)
        self.thread.start()

        self.save()

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

            self.reset_status_if_one_day_passed()
            self.scheduler.run_pending()

    def get_job_hours(self):
        hours = []
        for job in self.scheduler.get_jobs():
            hours.append('%2d:00' % job.at_time.hour)

        return hours

    def set_job_hours(self, hours):
        self.job_settings = ScrapeEquasisJob.init_job_settings(hours)

    def clear(self):
        self.thread_shared_event_cease_continuous_run.set()
        self.scheduler.clear()
        self.delete_saved_file()

    def notify_job_start(self, job_name):
        actual_time = datetime.datetime.now().strftime("%H:%M")
        logger.info("Job start: %s at %s" % (job_name, actual_time))
        self.job_settings[job_name].status = JOB_STATUS.RUNNING
        self.job_settings[job_name].actual_time = actual_time
        self.save()

        with open('/tmp/schedule_result.csv', 'w') as f:
            f.write('0,0')

        f.close()

    def notify_job_end(self, job_name):
        logger.info("Job end: %s at %s" %(job_name, datetime.datetime.now().strftime("%H:%M")))

        with open('/tmp/schedule_result.csv', 'r') as f:
            line = f.readline()
            (throughput, errors) = line.split(',')

        f.close()

        self.job_settings[job_name].status = JOB_STATUS.DONE
        self.job_settings[job_name].throughput = throughput
        self.job_settings[job_name].errors = errors
        self.save()

    def save(self):
        pickle_file_name = '/tmp/%s.pkl' % self.name
        with open(pickle_file_name, 'wb') as f:
            pickle.dump(self, f)

    def load(self):
        job = None
        try:
            pickle_file_name = '/tmp/%s.pkl' % self.name
            with open(pickle_file_name, 'rb') as f:
                job = pickle.load(f)

        except FileNotFoundError:
            pass
        except EOFError:
            logger.debug("Recovery pickle file.")
            self.save()

        return job

    def is_scheduled(self):
        pickle_file_name = '/tmp/%s.pkl' % self.name
        return os.path.isfile(pickle_file_name)

    def delete_saved_file(self):
        pickle_file_name = '/tmp/%s.pkl' % self.name
        try:
            os.remove(pickle_file_name)
        except FileNotFoundError:
            pass

    def is_entried(self, job_name):
        if job_name in self.job_settings:
            return self.job_settings[job_name].is_entried

        return False

    def get_status(self, job_name):
        if job_name in self.job_settings:
            return self.job_settings[job_name].status

        return ''

    def get_estimate_time(self, job_name):
        if job_name in self.job_settings:
            return self.job_settings[job_name].estimate_time

        return ''

    def get_actual_time(self, job_name):
        if job_name in self.job_settings:
            return self.job_settings[job_name].actual_time

        return ''

    def get_queues(self, job_name):
        if job_name in self.job_settings:
            return int(self.job_settings[job_name].queues)

        return 0

    def get_throughput(self, job_name):
        if job_name in self.job_settings:
            return int(self.job_settings[job_name].throughput)

        return 0

    def get_errors(self, job_name):
        if job_name in self.job_settings:
            return int(self.job_settings[job_name].errors)

        return 0

    def reset_status_if_one_day_passed(self):
        if datetime.datetime.now() - datetime.timedelta(days=1) > self.scheduled_at:
            for job_name, setting in self.job_settings.items():
                if setting.is_entried:
                    self.job_settings[job_name].status = JOB_STATUS.WAITING
                    self.job_settings[job_name].actual_time = ''
                    self.job_settings[job_name].queues = 0
                    self.job_settings[job_name].throughput = 0
                    self.job_settings[job_name].errors = 0

            self.scheduled_at = datetime.datetime.now()
