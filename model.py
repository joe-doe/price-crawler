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
