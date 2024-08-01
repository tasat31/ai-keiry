import sys
import settings

if __name__ == '__main__':
    if len(sys.argv) == 2:
        (script_name, command) = sys.argv

    if len(sys.argv) == 3:
        (script_name, command, imo_no) = sys.argv

    if command == 'scrape':
        import luigi
        import app.tasks.scrape_equasis as scrape_equasis
        luigi.build([scrape_equasis.ScrapeEquasisTask(imo_no=imo_no)], workers=5, local_scheduler=True)

    if command == 'scrape_batch_process':
        import luigi
        import app.tasks.scrape_equasis as scrape_equasis
        from schedules.scrape_equasis_job import ScrapeEquasisJob
        job = ScrapeEquasisJob()
        job.entry()

    if command == 'vessel_finder':
        from app.scrapers.vessel_finder.scraper import VesselFinderScraper
        from playwright.sync_api import Playwright, sync_playwright, TimeoutError as PlaywrightTimeoutError
        import time
        import random

        if len(sys.argv) == 2:
            # read std in
            with sync_playwright() as playwright:
                print('"%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s"' % ('ユーザー名', 'IMO番号', '備考', '船名', 'ATD', 'ATD_月日', 'ATD_時間', 'ATD_地域', 'ATD_国', 'ETA', 'ETA_月日', 'ETA時間', 'ETA地域', 'ETA_国'))
                for line in sys.stdin:
                    try:
                        vf = VesselFinderScraper(playwright)
                        (user_id, imo_no, remark) = line.rstrip().split(",")

                        sec = random.uniform(3,10)
                        time.sleep(sec)

                        data = vf.get_voyage_data(str(imo_no))

                        (ATD_date, ATD_time) = ('', '')
                        (ATD_area, ATD_country) = ('', '')
                        (ETA_date, ETA_time) = ('', '')
                        (ETA_area, ETA_country) = ('', '')

                        if ',' in data.departure_time:
                            (ATD_date, ATD_time) = data.departure_time.split(',')

                        if ',' in data.departure_port:
                            (ATD_area, ATD_country) = data.departure_port.split(',')

                        if ',' in data.arrival_time:
                            (ETA_date, ETA_time) = data.arrival_time.split(',')

                        if ',' in data.destination_port:
                            (ETA_area, ETA_country) = data.destination_port.split(',')

                        print('"%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s"' % (user_id, data.imo_no, remark, data.ship_name, data.departure_time_type, ATD_date, ATD_time, ATD_area, ATD_country, data.arrival_time_type, ETA_date, ETA_time, ETA_area, ETA_country))
                    except PlaywrightTimeoutError as e:
                        print(e.message)
                        print('"%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s"' % (user_id, imo_no, '', '', '', '', '', '', '', '', '', '', '', ''))
                    finally:
                        vf.close()

        if len(sys.argv) == 3:
            # specify IMO No
            with sync_playwright() as playwright:
                vf = VesselFinderScraper(playwright)
                data = vf.get_voyage_data(str(imo_no))
                vf.close()

            print(data)

    if command == 'vessel_finder_batch_process':
        from schedules.vessel_finder_job import VesselFinderJob

        vf_job = VesselFinderJob()
        vf_job.entry()
        vf_job.run()
