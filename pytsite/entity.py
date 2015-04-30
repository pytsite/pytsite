from . import registry
from pymongo import MongoClient
from bson.objectid import ObjectId
from bson.dbref import DBRef


_database = MongoClient().get_database('fakeoff_org')

class Base:
    _name = None

    _value = None

    def __init__(self, name: str=None, value=None):
        self._name = name
        self.set_value(value)

    def set_value(self, value):
        self._value = value

    def get_value(self):
        return self._value


class String(Base):
    _value = ''

    def set_value(self, value):
        if value is not None and not isinstance(value, str):
            raise Exception('String expected')
        super(String, self).set_value(value)

class List(Base):
    _value = []

    def set_value(self, value):
        if value is not None and not isinstance(value, list):
            raise Exception('List expected')
        super(List, self).set_value(value)

class Ref(Base):
    def set_value(self, value):
        if value is not None and not isinstance(value, DBRef):
            raise Exception('DBRef expected')
        super(Ref, self).set_value(value)

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
