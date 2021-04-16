from pymongo import MongoClient
import re



class Database():
    """
    A class responsible for execute opertions in a Mongo Database 
    Attributes
    ----------
    url: address
        The url for Mongo connector
    url: database
        The database to be connected
    Methods
    -------
    connect(cls, addr, db)
        Receives a database address and name to return a connected instance
    save(cls, addr, db)
        Receives a json data and a collection to be saved, then return the inserted id
    """
    connection = None
    database = None

    def __init__(self, address, database):
        self.address = address
        self.database = database
        Database.connect(address, database)

    @classmethod
    def connect(cls, addr, db):
        client = MongoClient(addr)
        database = db
        cls.connection = client[f'{database}']

    @staticmethod
    def save(data, collection):
        result = Database.connection[f'{collection}'].insert_one(data)
        return result.inserted_id

    @staticmethod
    def update(data, query, collection):
        Database.connection[f'{collection}'].update_one(query, data)

    @staticmethod
    def find(collection):
        return Database.connection[f'{collection}'].find().sort("_id", 1)

    @staticmethod
    def find_multiple_by_key(value, collection, key):
        return Database.connection[f'{collection}'].find({f"{key}": value})

    @staticmethod
    def find_multiple_by_query(query, collection):
        return Database.connection[f'{collection}'].find(query)

    @staticmethod
    def find_item(id, collection):
        return Database.connection[f'{collection}'].find_one(
                {"id": id})

    @staticmethod
    def find_by_key(value, collection, key):
        return Database.connection[f'{collection}'].find_one(
                {f"{key}": value})

    @staticmethod
    def save_data(data, collection):
        return Database.save(data, collection)

    @staticmethod
    def save_not_exists(data, collection):
        exists = Database.connection[f'{collection}'].find_one(
            {"id": data['id']})
        if(exists == None):
            return Database.save(data, collection)
        else:
            return {'error': f"{data['club_id']} already exists"}

    @staticmethod
    def get_team_id():
        item = Database.connection['team_id'].find_one(
            {"status": "created"})

        return item['id']

    @staticmethod
    def find_player(keyword, collection):
        query = {
        "name": {
            "$regex": keyword,
            "$options" :'i' # case-insensitive
            }
        }
        items = Database.connection[f'{collection}'].find(query).sort("hit", -1).limit(10)

        return items

    @staticmethod
    def find_top(collection):
        items = Database.connection[f'{collection}'].find().sort("hit", -1).limit(10)

        return items

    @staticmethod
    def count_collection(collection):
        item = Database.connection[f'{collection}'].find().count()
        return item