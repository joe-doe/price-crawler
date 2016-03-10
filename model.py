class Model(object):
    db = None
    db_name = None

    def __init__(self, config, db):
        self.db = db
        self.db_name = config['database']

    def add_record(self, record):
        self.db.mongodb[self.db_name].insert(record)

    def get_all(self):
        return self.db.mongodb[self.db_name].find()
