"""Description.
"""
from typing import Iterable as _Iterable
from bson import DBRef as _DBRef, ObjectId as _ObjectId
from pymongo.cursor import Cursor as _Cursor, CursorType as _CursorType
from pytsite import lang as _lang, util as _util, threading as _threading, reg as _reg, logger as _logger
from . import _model, _field, _api, _finder_cache

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


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
                if not isinstance(arg, _Iterable):
                    arg = (arg,)

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
        """Add text search criteria.
        """
        logical_op = self._resolve_logical_op(logical_op)
        if logical_op not in self._criteria:
            self._criteria[logical_op] = []

        self._criteria[logical_op].append({'$text': {
            '$search': search,
            '$language': self._resolve_language(language)}}
        )

    def remove_criteria(self, logical_op: str, field_name: str):
        logical_op = self._resolve_logical_op(logical_op)

        if logical_op not in self._criteria:
            return

        clean = []
        for item in self._criteria[logical_op]:
            if field_name not in item:
                clean.append(item)

        self._criteria[logical_op] = clean

    def compile(self) -> list:
        """Get compiled query.
        """
        return self._criteria


class Result:
    """DB Query Result.
    """
    def __init__(self, model: str, cursor: _Cursor, cache_uid: str, cache_ttl: int=3600):
        """Init.
        """
        self._model = model
        self._cursor = cursor
        self._cache_ttl = cache_ttl
        self._cache_uid = cache_uid

        if self._cache_ttl > 0:
            _finder_cache.create_pool(model, cache_uid, cache_ttl)

    def __iter__(self):
        """Get iterator.
        """
        return self

    def __next__(self):
        """Get next item.
        """
        try:
            doc = next(self._cursor)
            entity = _api.dispense(self._model, doc['_id'])

            if self._cache_ttl > 0:
                _finder_cache.add_entity(self._model, self._cache_uid, entity)

            return entity

        except StopIteration as e:
            if self._cache_ttl > 0:
                _finder_cache.freeze_pool(self._model, self._cache_uid)
            raise e

    def explain(self) -> dict:
        """Explain the cursor.
        """
        return self._cursor.explain()

    def explain_winning_plan(self) -> dict:
        """Explain winning plan of the the cursor.
        """
        return self.explain()['queryPlanner']['winningPlan']

    def explain_parsed_query(self) -> dict:
        """Explain parsed query of the the cursor.
        """
        return self.explain()['queryPlanner']['parsedQuery']

    def explain_execution_stats(self) -> dict:
        """Explain execution stats of the the cursor.
        """
        return self.explain()['executionStats']


class CachedResult:
    def __init__(self, model: str, query_sig: str):
        self._entities = _finder_cache.get_entities(model, query_sig)
        self._total = len(self._entities)
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self) -> _model.Model:
        if self._index >= self._total:
            raise StopIteration

        entity = self._entities[self._index]
        self._index += 1

        return entity


class Finder:
    def __init__(self, model_name: str, cache_ttl: int=60):
        """Init.
        """
        self._model = model_name
        self._mock = _api.dispense(model_name)
        self._query = Query(self._mock)
        self._skip = 0
        self._sort = None
        self._cache_ttl = cache_ttl

    @property
    def mock(self) -> _model.Model:
        """Get entity mock.
        """
        return self._mock

    def cache_ttl(self, ttl: int):
        """Set finder cache TTL.
        """
        self._cache_ttl = ttl

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

    def remove_where(self, field_name: str):
        """Remove field from criteria.
        """
        self._query.remove_criteria('$and', field_name)

        return self

    def remove_or_where(self, field_name: str):
        """Remove field from criteria.
        """
        self._query.remove_criteria('$or', field_name)

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

        return collection.count(filter=flt, skip=self._skip)

    def get(self, limit: int=0) -> Result:
        """Execute the query and return a cursor.
        """
        query = self._query.compile()

        with _threading.get_r_lock():
            cache_pool_uid = _util.md5_hex_digest(str((query, self._skip, limit, self._sort)))
            if self._cache_ttl > 0 and _finder_cache.pool_exists(self._model, cache_pool_uid):
                if _reg.get('odm.debug.enabled'):
                    msg = "Query found in cache '{}, {}', pool '{}'.".format(self._model, query, cache_pool_uid)
                    _logger.debug(msg, __name__)
                return CachedResult(self._model, cache_pool_uid)

        if _reg.get('odm.debug.enabled'):
            msg = "Query not found in cache: '{}, {}'.".format(self._model, query)
            _logger.debug(msg, __name__)

        collection = self._mock.collection
        cursor = collection.find(
            filter=query,
            projection={'_id': True},
            skip=self._skip,
            limit=limit,
            cursor_type=_CursorType.NON_TAILABLE,
            sort=self._sort,
        )

        return Result(self._model, cursor, cache_pool_uid, self._cache_ttl)

    def first(self) -> _model.Model:
        """Execute the query and return a first result.
        """
        result = list(self.get(1))
        if not result:
            return None

        return result[0]

    def distinct(self, field_name: str) -> list:
        from ._api import get_by_ref
        values = self._mock.collection.distinct(field_name, self._query.compile())
        r = []
        for v in values:
            if isinstance(v, _DBRef):
                v = get_by_ref(v)
            r.append(v)

        return r
