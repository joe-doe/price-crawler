import time
import urllib2

from bs4 import BeautifulSoup


def get_specs(url):
        try:
            html_text = urllib2.urlopen(url).read()
        except urllib2.HTTPError:
            return "specs not available"

        soup = BeautifulSoup(html_text, 'html.parser')
        specs = soup.find_all('div', {'class': 'spec-details'})

        all_specs = list()
        [all_specs.append(spec.encode('utf-8')) for spec in specs]

        return ' '.join(all_specs)


def get_quick_specs(url):
    try:
        html_text = urllib2.urlopen(url).read()
    except urllib2.HTTPError:
        return "quick specs not available"

    soup = BeautifulSoup(html_text, 'html.parser')
    quick_specs = soup.find('p', {'class': 'specs'})

    # replace a tag with b make it bold
    bold = soup.new_tag('b')
    bold.string = quick_specs.a.text
    quick_specs.a.insert_before(bold)

    # remove a tags
    quick_specs.a.extract()

    return str(quick_specs)


class Model(object):
    db = None
    data_collection_name = None
    items_collection_name = None
    results_limit = 10

    def __init__(self, config, db):
        self.db = db
        self.data_collection_name = config['data_collection']
        self.items_collection_name = config['items_collection']
        self.specs_collection_name = config['specs_collection']
        self.config = config

    def add_new_item(self, item):
        for store in item['stores']:
            rec = {
                'item_name': item['item_name'],
            }
            rec.update(store)
            self.db.mongodb[self.items_collection_name].insert(rec)

            if store['store_name'] == 'skroutz':
                skroutz_site_url = store['url']
                specs = {
                    'item_name': item['item_name'],
                    'specs': get_specs(skroutz_site_url),
                    'quick_specs': get_quick_specs(skroutz_site_url)
                }
                self.db.mongodb[self.specs_collection_name].insert(specs)

            # specs = {
            #     'item_name': item['item_name'],
            #     'specs': get_specs('http://www.gsmarena.com/microsoft_lumia_950-7262.php')
            # }
            # self.db.mongodb['specs'].insert(specs)

            from price_crawler import PriceCrawler
            pc = PriceCrawler(self.config, self, item['item_name'])
            rec = {
                'timestamp': time.time(),
                'item_name': item['item_name'],
            }

            try:
                rec.update(pc.get_store_price(store['store_name']))
                self.add_record(rec)
            except TypeError:
                pass  # no price for store

    def add_record(self, record):
        self.db.mongodb[self.data_collection_name].insert(record)

    def get_all(self):
        return self.db.mongodb[self.data_collection_name].find()

    def get_all_items(self):
        return self.db.mongodb[self.items_collection_name]\
            .distinct('item_name')

    def get_all_stores(self):
        return self.db.mongodb[self.items_collection_name]\
            .distinct('store_name')

    def get_all_for_store(self, store):
        mongo_filter = {
            'store_name': store,
        }
        mongo_projection = {
            'store_name': 1,
            'item_name': 1,
            'timestamp': 1,
            'price': 1,
            '_id': 0
        }

        result = self.db.mongodb[self.data_collection_name]\
            .find(mongo_filter, mongo_projection)\
            .sort([('timestamp', -1)])\
            .limit(self.results_limit)

        return_list = list(result)
        return_list.reverse()
        return return_list

    def get_item_for_all_stores(self, item):
        mongo_filter = {
            'item_name': item,
        }
        mongo_projection = {
            'store_name': 1,
            'item_name': 1,
            'timestamp': 1,
            'price': 1,
            '_id': 0
        }

        result = self.db.mongodb[self.data_collection_name]\
            .find(mongo_filter, mongo_projection)\
            .sort([('timestamp', -1)])\
            .limit(self.results_limit)

        return_list = list(result)
        return_list.reverse()
        return return_list

    def get_item_for_store(self, item, store):
        mongo_filter = {
            'store_name': store,
            'item_name': item
        }
        mongo_projection = {
            'price': 1,
            '_id': 0
        }

        result = self.db.mongodb[self.data_collection_name]\
            .find(mongo_filter, mongo_projection)\
            .sort([('timestamp', -1)])\
            .limit(self.results_limit)

        return_list = list(result)
        return_list.reverse()
        return return_list

    def get_timestamps_for_item(self, item):
        mongo_filter = {
            'item_name': item,
            'store_name': 'skroutz',
        }
        mongo_projection = {
            'timestamp': 1,
            '_id': 0
        }
        return_list = list()
        mongo_response = self.db.mongodb[self.data_collection_name]\
            .find(mongo_filter, mongo_projection)\
            .sort([('timestamp', -1)])\
            .limit(self.results_limit)

        for item in mongo_response:
            return_list.append(item['timestamp'])

        return_list.reverse()
        return return_list

    def get_url_for_item(self, item, store):

        mongo_filter = {
            'item_name': item,
            'store_name': store,
        }
        mongo_projection = {
            'url': 1,
            '_id': 0
        }

        return self.db.mongodb[self.items_collection_name]\
            .find(mongo_filter, mongo_projection).next()

    def get_stores_for_item(self, item):
        mongo_filter = {
            'item_name': item
        }
        mongo_projection = {
            'store_name': 1,
            '_id': 0
        }

        result = self.db.mongodb[self.items_collection_name]\
            .find(mongo_filter, mongo_projection)

        return_list = list()

        for item in result:
            return_list.append(item['store_name'])

        return return_list

    def maintenance(self):
        now = time.time()
        delta = self.config['keep_data_for']
        delete_from = now - delta

        mongo_filter = {
            'timestamp': {'$lte': delete_from}
        }

        result = self.db.mongodb[self.data_collection_name]\
            .delete_many(mongo_filter)

        return "deleted {} records".format(result)

    def get_specs(self, item):
        mongo_filter = {
            'item_name': item,
        }
        mongo_projection = {
            'specs': 1,
            '_id': 0
        }

        try:
            res = self.db.mongodb[self.specs_collection_name]\
                .find(mongo_filter, mongo_projection).next()

            return res['specs']
        except Exception:
            return "specs not available"

    def get_quick_specs(self, item):
        mongo_filter = {
            'item_name': item,
        }
        mongo_projection = {
            'quick_specs': 1,
            '_id': 0
        }

        try:
            res = self.db.mongodb[self.specs_collection_name]\
                .find(mongo_filter, mongo_projection).next()

            return res['quick_specs']
        except Exception:
            return "quick specs not available"
