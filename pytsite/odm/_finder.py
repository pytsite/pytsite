"""Description.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from bson import DBRef as _DBRef, ObjectId as _ObjectId
from pymongo.cursor import Cursor as _Cursor, CursorType as _CursorType

from pytsite import lang as _lang
from . import _model, _field


class Query:
    """Query Representation.
    """
    def __init__(self, model: _model.Model):
        """Init.
        """
        self._model = model
        self._criteria = {}

    @staticmethod
    def _resolve_logical_op(op: str) -> str:
        """Resolve logical operator.
        """
        if op not in ('and', 'or', '$and', '$or'):
            raise TypeError("Invalid logical operator: '{0}'.".format(op))
        if not op.startswith('$'):
            op = '$' + op

        return op

    @staticmethod
    def _resolve_comparison_op(op: str) -> str:
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
        elif op in ('regex_i', '$regex_i'):
            return '$regex_i'
        else:
            raise TypeError("Invalid comparison operator: '{0}'.".format(op))

    @staticmethod
    def _resolve_language(code: str=None):
        if not code:
            code = _lang.get_current()

        if code == 'en':
            return 'english'
        elif code == 'ru':
            return 'russian'
        else:
            return 'none'

    def add_criteria(self, logical_op: str, field_name: str, comparison_op: str, arg):
        """Add find criteria.
        """
        logical_op = self._resolve_logical_op(logical_op)
        comparison_op = self._resolve_comparison_op(comparison_op)

        if field_name.find('.') < 0:
            field = self._model.get_field(field_name)

            # Convert str to ObjectId
            if isinstance(field, _field.ObjectId) and isinstance(arg, str):
                arg = _ObjectId(arg)

            # Convert instance to DBRef
            if isinstance(field, _field.Ref) and isinstance(arg, _model.Model):
                arg = arg.ref

            # Convert list of instances to list of DBRefs
            if isinstance(field, _field.RefsList):
                if not isinstance(arg, list):
                    raise ValueError('List expected.')

                clean_arg = []
                for v in arg:
                    if isinstance(v, _model.Model):
                        v = v.ref
                    clean_arg.append(v)
                arg = clean_arg

        # Adding logical operator's dictionary to the criteria
        if logical_op not in self._criteria:
            self._criteria[logical_op] = []

        # Finally adding the criteria itself
        if comparison_op == '$regex_i':
            self._criteria[logical_op].append({field_name: {'$regex': arg, '$options': 'i'}})
        else:
            self._criteria[logical_op].append({field_name: {comparison_op: arg}})

    def add_text_search(self, logical_op: str, search: str, language: str=None):
        logical_op = self._resolve_logical_op(logical_op)
        if logical_op not in self._criteria:
            self._criteria[logical_op] = []

        self._criteria[logical_op].append({'$text': {
            '$search': search,
            '$language': self._resolve_language(language)}}
        )

    def compile(self) -> list:
        """Get criteria.
        """
        return self._criteria


class Result:
    def __init__(self, model_name: str, cursor: _Cursor):
        self._model_name = model_name
        self._cursor = cursor

    def __iter__(self):
        return self

    def __next__(self):
        from ._functions import dispense
        doc = next(self._cursor)

        return dispense(self._model_name, doc['_id'])


class Finder:
    def __init__(self, model_name: str):
        """Init.
        """
        from ._functions import dispense

        self._model = model_name
        self._mock = dispense(model_name)
        self._query = Query(self._mock)
        self._skip = 0
        self._limit = 0
        self._sort = None

    @property
    def mock(self) -> _model.Model:
        """Get entity mock.
        """
        return self._mock

    def where(self, field_name: str, comparison_op: str, arg):
        """Add '$and' criteria.
        """
        self._query.add_criteria('$and', field_name, comparison_op, arg)

        return self

    def or_where(self, field_name: str, comparison_op: str, arg):
        """Add '$or' criteria.
        """
        self._query.add_criteria('$or', field_name, comparison_op, arg)

        return self

    def where_text(self, search: str):
        """Add '$text' criteria.
        """
        self._query.add_text_search('$and', search)

        return self

    def or_where_text(self, search: str):
        """Add '$or $text' criteria.
        """
        self._query.add_text_search('$or', search)

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
            if not self._mock.has_field(f[0]):
                raise Exception("Unknown field '{}' in model '{}'".format(f[0], self._model))
        self._sort = fields

        return self

    def count(self) -> int:
        """Count documents in collection.
        """
        collection = self._mock.collection
        flt = self._query.compile()
        return collection.count(filter=flt, skip=self._skip, limit=self._limit)

    def get(self, limit: int=0) -> Result:
        """Execute the query and return a cursor.
        """
        self._limit = limit
        collection = self._mock.collection
        cursor = collection.find(
            self._query.compile(),
            {'_id': True},
            self._skip,
            self._limit,
            False,
            _CursorType.NON_TAILABLE,
            self._sort
        )

        return Result(self._model, cursor)

    def first(self) -> _model.Model:
        """Execute the query and return a first result.
        """
        result = list(self.get(1))
        if not result:
            return None

        return result[0]

    def distinct(self, field_name: str) -> list:
        from ._functions import get_by_ref
        values = self._mock.collection.distinct(field_name, self._query.compile())
        r = []
        for v in values:
            if isinstance(v, _DBRef):
                v = get_by_ref(v)
            r.append(v)

        return r
