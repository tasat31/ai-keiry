import luigi
from settings import logger
import app.tasks.scrape_equasis as scrape_equasis
import app.tasks.dummy as dummy_task
import services.queue as queue
from settings import UPPER_LIMIT_SCRAPING_BY_ONE_BATCH

def __get_imo_no_list():
    imo_no_list = []
    for imo_no, priority, last_updated_at in queue.task_list(limit=UPPER_LIMIT_SCRAPING_BY_ONE_BATCH):
        imo_no_list.append(imo_no)

    return imo_no_list

def build():
    imo_no_list = __get_imo_no_list()

    tasks = []
    for imo_no in imo_no_list:
        tasks.append(scrape_equasis.ScrapeEquasisTask(imo_no=imo_no))

    if len(tasks) != 0:
        luigi.build(tasks, workers=1, local_scheduler=True)
    else:
        luigi.build([dummy_task.DummyTask()], workers=1, local_scheduler=True)
