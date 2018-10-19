import pymongo


class To_db():
    def __init__(self):
        self.conn=pymongo.MongoClient(host='127.0.0.1',port=27017)
    def create_db(self,DB_NAME):
        self.db=self.conn['wuhan']
        self.collections=self.db['{}'.format(DB_NAME)]
    def insert_db(self,dict_c):
        self.collections.insert_one(dict_c)
    def close_db(self):
        self.conn.close()