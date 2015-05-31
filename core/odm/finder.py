"""Description.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


from pymongo.cursor import Cursor, CursorType
from .models import ODMModel
from .fields import *


class Query:
    """Query Representation.
    """

    def __init__(self, model: ODMModel):
        """Init.
        """

        self._model = model
        self._criteria = dict()

    def _resolve_logical_op(self, op: str)->str:
        """Resolve logical operator.
        """

        if op not in ('and', 'or', '$and', '$or'):
            raise TypeError("Invalid logical operator: '{0}'.".format(op))
        if not op.startswith('$'):
            op = '$' + op
        return op

    def _resolve_comparison_op(self, op: str) -> str:
        """Resolve comparison operator.
        """

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
        """Add find criteria.
        """

        field = self._model.get_field(field_name)
        logical_op = self._resolve_logical_op(logical_op)
        comparison_op = self._resolve_comparison_op(comparison_op)

        # Convert str to ObjectId if it's necessary
        if isinstance(field, ObjectIdField):
            if isinstance(arg, str):
                arg = ObjectId(arg)

        # Adding logical operator's dictionary to the criteria
        if logical_op not in self._criteria:
            self._criteria[logical_op] = []

        # Finally adding the criteria itself
        self._criteria[logical_op].append({field_name: {comparison_op: arg}})

    def get_criteria(self) -> list:
        """Get criteria.
        """

        return self._criteria


class Result:
    def __init__(self, model_name: str, cursor: Cursor):
        self._model_name = model_name
        self._cursor = cursor

    def __iter__(self):
        return self

    def __next__(self):

        from .odm_manager import dispense
        doc = next(self._cursor)

        return dispense(self._model_name, doc['_id'])


class Finder:
    def __init__(self, model_name: str):
        """Init.
        """

        from .odm_manager import dispense

        self._model_name = model_name
        self._entity = dispense(model_name)
        self._query = Query(self._entity)
        self._skip = 0
        self._limit = 0
        self._sort = None

    def where(self, field_name: str, comparison_op: str, arg):
        """Add '$and' criteria.
        """

        self._query.add_criteria('$and', field_name, comparison_op, arg)

        return self

    def or_where(self, field_name: str, comparison_op: str, arg):
        """Add '$or' criteria
        """
        self._query.add_criteria('$or', field_name, comparison_op, arg)
        return self

    def skip(self, num: int):
        """Set number of records to skip in result cursor.
        """

        self._skip = num

        return self

    def sort(self, fields=None):
        """Set sort criteria.
        """

        for f in fields:
            if not self._entity.has_field(f[0]):
                raise Exception("Unknown field '{}' in model '{}'".format(f[0], self._model_name))
        self._sort = fields

        return self

    def count(self) -> int:
        """Count documents in collection.
        """

        collection = self._entity.collection
        flt = self._query.get_criteria()
        return collection.count(filter=flt, skip=self._skip, limit=self._limit)

    def get(self, limit: int=0):
        """Execute the query and return a cursor.

        :rtype: list[ODMModel]
        """

        self._limit = limit
        collection = self._entity.collection
        cursor = collection.find(
            self._query.get_criteria(),
            {'_id': True},
            self._skip,
            self._limit,
            False,
            CursorType.NON_TAILABLE,
            self._sort
        )

        return Result(self._model_name, cursor)

    def first(self)->ODMModel:
        """Execute the query and return a first result.
        """
        result = list(self.get(1))
        if not result:
            return None

        return result[0]
