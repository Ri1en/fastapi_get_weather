from pymongo import MongoClient


class MongoDb:
    def __init__(self, settings, collection: str):
        self.settings = settings
        self.collection: str = collection
        self.db = self.connect_db()

    def connect_db(self):
        client = MongoClient(
            f"mongodb://{self.settings.user}:{self.settings.password}@{self.settings.host}:{self.settings.port}/"
        )
        return client[self.settings.db_name]

    def connect_collection(self):
        return self.db[self.collection]

    def __enter__(self):
        return self.connect_collection()

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
