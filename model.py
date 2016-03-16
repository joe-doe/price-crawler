class Model(object):
    db = None
    collection_name = None

    def __init__(self, config, db):
        self.db = db
        self.collection_name = config['collection']

    def add_record(self, record):
        self.db.mongodb[self.collection_name].insert(record)

    def get_all(self):
        return self.db.mongodb[self.collection_name].find()

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

        return self.db.mongodb[self.collection_name].find(mongo_filter,
                                                          mongo_projection)

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

        return self.db.mongodb[self.collection_name].find(mongo_filter,
                                                          mongo_projection)

    def get_item_for_store(self, item, store):
        mongo_filter = {
            'store_name': store,
            'item_name': item
        }
        mongo_projection = {
            'price': 1,
            '_id': 0
        }

        return self.db.mongodb[self.collection_name].find(mongo_filter,
                                                          mongo_projection)

    def get_items(self):
        return self.db.mongodb[self.collection_name].distinct('item_name')

    def get_stores(self):
        return self.db.mongodb[self.collection_name].distinct('store_name')

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
        mongo_response = self.db.mongodb[self.collection_name]\
            .find(mongo_filter, mongo_projection)

        for item in mongo_response:
            return_list.append(item['timestamp'])

        return return_list
