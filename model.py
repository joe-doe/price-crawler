class Model(object):
    db = None
    db_name = 'price-crawler'

    def __init__(self, db):
        self.db = db

    def add_record(self, record):
        self.db.mongodb[self.db_name].insert(record)

    def get_all(self):
        return self.db.mongodb[self.db_name].find()
