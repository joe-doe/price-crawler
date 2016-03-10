import threading
import time

from crawlers import JsonCrawler
from db import MongoDB
from model import Model
from routes_api import register_routes


def initialize_db(config):
    # establish mongoDB connection
    return MongoDB(config['uri'], config['database'])


def initialize_model(db):
    # available operations
    return Model(db)


def initialize_routes(config, api, model):
    register_routes(config, api, model)


def initialize_mongodb_feed(config, model):

    def worker():
        while True:
            mongo_document = JsonCrawler(config).get_prices()

            for rec in mongo_document:
                model.add_record(rec)
            time.sleep(14400)

    t = threading.Thread(target=worker)
    t.setDaemon(True)
    t.start()
