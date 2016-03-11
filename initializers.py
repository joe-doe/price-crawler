import threading
import time

from crawlers import JsonCrawler
from db import MongoDB
from model import Model
from routes_api import register_routes


def initialize_db(config):
    # establish mongoDB connection
    return MongoDB(config['uri'], config['database'])


def initialize_model(config, db):
    # available operations
    return Model(config, db)


def initialize_routes(config, api, model):
    register_routes(config, api, model)


def initialize_mongodb_feed(config, model):

    def worker():
        time.sleep(5)
        while True:
            mongo_document = JsonCrawler(config).get_prices()

            for rec in mongo_document:
                model.add_record(rec)
            time.sleep(config['sleep_interval'])

    t = threading.Thread(target=worker)
    t.setDaemon(True)
    t.start()
