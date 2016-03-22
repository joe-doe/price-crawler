import schedule
import requests
import time
import threading

from crawlers import JsonCrawler
from db import MongoDB
from model import Model
from routes_api import register_api_routes
from routes_non_api import register_non_api_routes


def initialize_db(config):
    # establish mongoDB connection
    return MongoDB(config['uri'], config['database'])


def initialize_model(config, db):
    # available operations
    return Model(config, db)


def initialize_routes(app, api, model):
    register_api_routes(api, model)
    register_non_api_routes(app, model)


def initialize_schedule_jobs(config, model):

    class SchedulerThread(threading.Thread):

        interval = config['keep_alive_sleep_interval']
        feed_mongo_at = ["06:00", "10:00", "15:00", "19:00"]

        def __init__(self):
            super(SchedulerThread, self).__init__()

            for scheduled_time in self.feed_mongo_at:
                schedule.every().day.at(scheduled_time).do(self.mongo_feed)

            schedule.every(self.interval).seconds.do(self.keep_alive)

            self.setDaemon(True)

        def run(self):
            self.mongo_feed()

            if config['DEBUG']:
                return

            while True:
                schedule.run_pending()
                time.sleep(self.interval/2)

        def mongo_feed(self):
            mongo_document = JsonCrawler(config, model).get_prices()

            for rec in mongo_document:
                model.add_record(rec)

        def keep_alive(self):
            requests.get('https://price-crawl.herokuapp.com/ping')

    scheduler_thread = SchedulerThread()
    scheduler_thread.start()

