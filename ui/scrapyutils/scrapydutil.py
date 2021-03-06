from scrapyd_api import ScrapydAPI
import traceback

class ScrapydJob(object):

    def __init__(self, scrapyd_host="localhost", scrapyd_port="6800", project="default", spider="website_finder", screenshot_dir=""):

        scrapy_url = "http://" + scrapyd_host + ":" + str(scrapyd_port)
        self.scrapi = ScrapydAPI(scrapy_url)
        self.project = project
        self.spider = spider
        self.screenshot_dir = screenshot_dir        

    def schedule(self, seed):

        if not self.screenshot_dir:
            raise Exception("Please set the screenshot path in the config before scheduling")

        self.job_id = self.scrapi.schedule(self.project, self.spider, seed_urls=seed, screenshot_dir = self.screenshot_dir)

        return self.job_id

    def list_jobs(self):
        return self.scrapi.list_jobs(self.project)

    def get_state(self, job_id):

        try:
            for job in self.scrapi.list_jobs(self.project)["running"]:
                print job_id, job["id"]
                if job["id"] == job_id:
                    return "Running"

            for job in self.scrapi.list_jobs(self.project)["pending"]:
                print job_id, job["id"]
                if job["id"] == job_id:
                    return "Pending"

        except:
            print "handled exception:"
            traceback.print_exc()
            return None

        return "Done"

if __name__ == "__main__":

    scrapyd_util = ScrapydJob("localhost", 80, screenshot_dir = "blahblah")
