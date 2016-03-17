import threading
import time
import requests

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


def initialize_routes(config, app, api, model):
    register_api_routes(config, api, model)
    register_non_api_routes(config, app, model)


def initialize_background_threads(config, model):

    def worker():
        while True:
            mongo_document = JsonCrawler(config).get_prices()

            for rec in mongo_document:
                model.add_record(rec)
            time.sleep(config['sleep_interval'])

    def keep_alive():
        while True:
            requests.get('https://price-crawl.herokuapp.com/index')
            time.sleep(config['keep_alive_sleep_interval'])

    mongo_feed = threading.Thread(target=worker)
    mongo_feed.setDaemon(True)
    mongo_feed.start()

    keep_alive = threading.Thread(target=keep_alive)
    keep_alive.setDaemon(True)
    keep_alive.start()
