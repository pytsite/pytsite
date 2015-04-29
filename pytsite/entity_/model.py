from pymongo import MongoClient
from bson.objectid import ObjectId

_client = MongoClient()
_database = _client.get_database('fakeoff_org')


class Entity:
    _fields = {}

    _collection = None

    def __init__(self, collection_name: str, object_id=None):
        self._collection = _database.get_collection(collection_name)
        self.setup()

        # Loading fields data from collection
        if object_id is not None:
            data = self._collection.find_one({'_id': ObjectId(object_id)})
            if data is not None:
                for field_name, value in data.items():
                    if field_name in self._fields:
                        self._fields[field_name].set_value(value)

    def setup(self):
        pass

    def define_field(self, field_name: str, field_class: type):
        self._fields[field_name] = field_class()

    def get(self, field_name: str)->object:
        if field_name not in self._fields:
            raise Exception("Unknown field " + field_name)
        return self._fields[field_name].get_value()


