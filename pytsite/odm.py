from . import db
from inspect import isclass
from bson.objectid import ObjectId
from bson.dbref import DBRef
from datetime import datetime
from pymongo.collection import Collection


class Field:
    def __init__(self):
        self.__modified = False
        self.__value = None

    def set_val(self, value, reset_modified: bool=True):
        self.__value = value
        if reset_modified and not self.__modified:
            self.__modified = True

    def get_val(self, *args):
        return self.__value

    def is_modified(self)->bool:
        return self.__modified


class ObjectIdField(Field):
    def set_val(self, value, reset_modified: bool=True):
        if not isinstance(value, ObjectId):
            raise TypeError("ObjectId expected")
        super().set_val(value, reset_modified)


class List(Field):
    def set_val(self, value: list, reset_modified: bool=True):
        if not isinstance(value, list):
            raise TypeError("List expected")
        super().set_val(value, reset_modified)


class RefField(Field):
    def set_val(self, value, reset_modified: bool=True):
        if not isinstance(value, DBRef) and value is not None:
            raise TypeError("DBRef or None expected")
        super().set_val(value, reset_modified)


class RefsListField(Field):
    def set_val(self, value: list, reset_modified: bool=True):
        if not isinstance(value, list):
            raise TypeError("List of DBRefs expected")

        for item in value:
            if not isinstance(item, DBRef):
                raise TypeError("List of DBRefs expected")

        super().set_val(value, reset_modified)


class DateTimeField(Field):
    def set_val(self, value: list, reset_modified: bool=True):
        if not isinstance(value, datetime) and value is not None:
            raise TypeError("DateTime or None expected")
        super().set_val(value, reset_modified)


class StringField(Field):
    def set_val(self, value: str, reset_modified: bool=True):
        if not isinstance(value, str):
            raise TypeError("Str expected")
        super().set_val(value, reset_modified)


class Model:
    def __init__(self, model_name: str, obj_id=None):
        if not hasattr(self, 'collection_name'):
            self.__collection_name = None

        if self.__collection_name is None:
            self.__collection_name = model_name + 's'

        self.__collection = db.get_collection(self.__collection_name)

        self._id = ObjectIdField()
        self._model = StringField()
        self._parent = RefField()
        self._children = RefsListField()
        self._created = DateTimeField()
        self._modified = DateTimeField()

        self._model.set_val(model_name)

        self.setup()

        # Loading fields data from collection
        if obj_id is not None:
            if isinstance(obj_id, str):
                obj_id = ObjectId(obj_id)
            data = self.__collection.find_one({'_id': obj_id})
            if data is not None:
                for field_name, value in data.items():
                    if self.has_field(field_name):
                        self.get_field(field_name).set_val(value)

    def define_field(self, name: str, obj: Field):
        setattr(self, name, obj)
        return self

    def setup(self):
        pass

    def collection(self)->Collection:
        """Get collection."""
        return self.__collection

    def has_field(self, name)->bool:
        if not hasattr(self, name) or not isinstance(getattr(self, name), Field):
            return False
        return True

    def get_field(self, field)->Field:
        if not self.has_field(field):
            raise Exception("Unknown field '{0}'".format(field))
        return getattr(self, field)

    def id(self):
        return self.f_get('_id')

    def model(self):
        return self.f_get('_model')

    def parent(self):
        return self.f_get('_parent')

    def children(self):
        return self.f_get('_children')

    def created(self):
        return self.f_get('_created')

    def modified(self):
        return self.f_get('_modified')

    def f_set(self, field: str, value):
        """Set field's value"""
        self.get_field(field).set_val(value)
        return self

    def f_get(self, field: str):
        """Get field's value"""
        return self.get_field(field).get_val()


class Query:
    def __init__(self, model: Model):
        self.__model = model
        self.__criteria = dict()

    def resolve_logical_op(self, op: str)->str:
        if op not in ('and', 'or', '$and', '$or'):
            raise TypeError("Invalid logical operator: '{0}'.".format(op))
        if not op.startswith('$'):
            op = '$' + op
        return op

    def resolve_comparison_op(self, op: str)->str:
        if op in ('=', 'eq', '$eq'):
            return '$eq'
        elif op in ('>', 'gt', '$gt'):
            return '$gt'
        elif op in ('>=', 'gte', '$gte'):
            return '$gte'
        elif op in ('in', '$in'):
            return '$in'
        elif op in ('<', 'lt', '$lt'):
            return '$lt'
        elif op in ('<=', 'lte', '$lte'):
            return '$lte'
        elif op in ('!=', 'ne', '$ne'):
            return '$ne'
        elif op in ('nin', '$nin'):
            return '$nin'
        elif op in ('regex', '$regex'):
            return '$regex'
        else:
            raise TypeError("Invalid comparison operator: '{0}'.".format(op))

    def add_criteria(self, logical_op: str, field_name: str, comparison_op: str, arg):
        """Add find criteria"""
        field = self.__model.get_field(field_name)
        logical_op = self.resolve_logical_op(logical_op)
        comparison_op = self.resolve_comparison_op(comparison_op)

        if isinstance(field, ObjectIdField):
            if isinstance(arg, str):
                arg = ObjectId(arg)

        if logical_op not in self.__criteria:
            self.__criteria[logical_op] = []

        self.__criteria[logical_op].append({field_name: {comparison_op: arg}})

    def get_criteria(self)->list:
        """Get criteria"""
        return self.__criteria


class Finder:
    def __init__(self, model_name):
        self.__model_name = model_name
        self.__model = dispense(model_name)
        self.__query = Query(self.__model)
        self.__skip = 0
        self.__sort = None

    def where(self, field_name: str, comparison_op: str, arg):
        self.__query.add_criteria('$and', field_name, comparison_op, arg)
        return self

    def or_where(self, field_name: str, comparison_op: str, arg):
        self.__query.add_criteria('$or', field_name, comparison_op, arg)
        return self

    def skip(self, num: int):
        self.__skip = num
        return self

    def sort(self, fields: dict=None):
        self.__sort = fields
        return self

    def get(self, limit: int=0)->list:
        cursor = self.__model.collection().find(self.__query.get_criteria(), {'_id': True}, self.__skip)
        if self.__sort is not None:
            cursor.sort(self.__sort)

        left = self.__skip
        if limit:
            right = left + limit
        else:
            right = cursor.count()

        r = []
        for doc in cursor[left:right]:
            r.append(dispense(self.__model_name, doc['_id']))

        return r

__registered_models = dict()


def register_model(model_name: str, model_class: type):
    if model_name in __registered_models:
        raise Exception("Model '{0}' already registered.".format(model_name))

    if not isclass(model_class):
        raise Exception("Class expected as second argument.")

    if not issubclass(model_class, Model):
        raise Exception("Subclassing of Model expected.")

    __registered_models[model_name] = model_class


def dispense(model_name: str, doc_id=None)->Model:
    if model_name not in __registered_models:
        raise Exception("Model '{0}' is not registered".format(model_name))

    return __registered_models[model_name](model_name, doc_id)


def find(model_name: str)->Finder:
    return Finder(model_name)