"""Description.
"""
from typing import Iterable as _Iterable, Union as _Union
from bson import DBRef as _DBRef, ObjectId as _ObjectId
from pymongo.cursor import Cursor as _Cursor, CursorType as _CursorType
from pytsite import lang as _lang, util as _util, reg as _reg, cache as _cache, logger as _logger
from . import _entity, _field, _api

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

_pool_prefix = 'pytsite.odm.finder:'
_dbg = _reg.get('odm.debug')


class Query:
    """Query Representation.
    """

    def __init__(self, model: _entity.Entity):
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
        elif op in ('near', '$near'):
            return '$near'
        else:
            raise TypeError("Invalid comparison operator: '{0}'.".format(op))

    @staticmethod
    def _resolve_language(code: str = None):
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

        # If not sub document
        if field_name.find('.') < 0:
            if field_name == '_id':
                # Convert str to ObjectId
                if isinstance(arg, str):
                    arg = _ObjectId(arg)
            else:
                field = self._model.get_field(field_name)

                # Convert instance to DBRef
                if isinstance(field, _field.Ref) and isinstance(arg, _entity.Entity):
                    arg = arg.ref

                # Convert list of instances to list of DBRefs
                if isinstance(field, _field.RefsList):
                    if not isinstance(arg, _Iterable):
                        arg = (arg,)

                    clean_arg = []
                    for v in arg:
                        if isinstance(v, _entity.Entity):
                            v = v.ref
                        clean_arg.append(v)
                    arg = clean_arg

        # Checking for argument type
        if comparison_op == '$near':
            if type(arg) not in (list, tuple):
                raise TypeError('Geo coordinates should be specified as a list or a tuple.')

        # Adding logical operator's dictionary to the criteria
        if logical_op not in self._criteria:
            self._criteria[logical_op] = []

        # Finally adding the criteria itself
        if comparison_op == '$regex_i':
            self._criteria[logical_op].append({field_name: {'$regex': arg, '$options': 'i'}})
        else:
            self._criteria[logical_op].append({field_name: {comparison_op: arg}})

    def add_text_search(self, logical_op: str, search: str, language: str = None):
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

    def __init__(self, model: str, cursor: _Cursor = None, ids: list = None):
        """Init.
        """
        self._model = model
        self._cursor = cursor
        self._cached = ids is not None
        self._ids = [doc['_id'] for doc in list(cursor)] if cursor else ids
        self._total = len(self._ids)
        self._current = 0

    @property
    def model(self) -> str:
        return self._model

    @property
    def ids(self) -> list:
        return self._ids

    def __iter__(self):
        """Get iterator.
        """
        return self

    def __next__(self) -> _entity.Entity:
        """Get next item.
        """
        if self._current == self._total:
            raise StopIteration()

        entity = _api.dispense(self._model, self._ids[self._current])
        self._current += 1

        return entity

    def count(self) -> int:
        return self._total

    def explain(self) -> dict:
        """Explain the cursor.
        """
        if not self._cursor:
            raise RuntimeError('Cannot explain cached results.')

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


class Finder:
    def __init__(self, model: str):
        """Init.
        """
        self._model = model
        self._mock = _api.dispense(model)
        self._query = Query(self._mock)
        self._skip = 0
        self._limit = 0
        self._sort = None
        self._cache_ttl = _reg.get('odm.cache.ttl', 3600)

    @property
    def model(self) -> str:
        """Get entity mock.
        """
        return self._model

    @property
    def mock(self) -> _entity.Entity:
        """Get entity mock.
        """
        return self._mock

    @property
    def query(self) -> Query:
        return self._query

    @property
    def id(self) -> str:
        return _util.md5_hex_digest(str((self._query.compile(), self._skip, self._limit, self._sort)))

    @property
    def cache_ttl(self) -> int:
        return self._cache_ttl

    def cache(self, ttl: int):
        """Set query cache TTL.
        """
        self._cache_ttl = ttl

        return self

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
        if fields:
            for f in fields:
                if f[0] != '_id' and not self._mock.has_field(f[0]):
                    raise RuntimeError("Unknown field '{}' in model '{}'".format(f[0], self._model))
            self._sort = fields
        else:
            self._sort = None

        return self

    def count(self) -> int:
        """Count documents in collection.
        """
        collection = self._mock.collection
        flt = self._query.compile()

        return collection.count(filter=flt, skip=self._skip)

    def get(self, limit: int = 0) -> _Union[_Iterable[_entity.Entity], Result]:
        """Execute the query and return a cursor.
        """
        self._limit = limit
        query = self._query.compile()

        # Search for previous result in cache
        if _reg.get('odm.cache.enabled', True) and self._cache_ttl and _cache_has(self):
            ids = _cache_get(self)
            if _dbg:
                _logger.debug("GET cached query results: query: {}, {}, id: {}, entities: {}.".
                              format(self.model, self.query.compile(), self.id, len(ids)), __name__)

            return Result(self._model, ids=ids)

        cursor = self._mock.collection.find(
            filter=query,
            projection={'_id': True},
            skip=self._skip,
            limit=self._limit,
            cursor_type=_CursorType.NON_TAILABLE,
            sort=self._sort,
        )

        result = Result(self._model, cursor)

        if _reg.get('odm.cache.enabled', True) and self._cache_ttl:
            if _dbg:
                _logger.debug("STORE query results: query: {}, {}, id: {}, entities: {}, TTL: {}.".
                              format(self.model, self.query.compile(), self.id, result.count(), self._cache_ttl),
                              __name__)

            _cache_put(self, result)

        return result

    def first(self) -> _Union[_entity.Entity, None]:
        """Execute the query and return a first result.
        """
        result = list(self.get(1))

        if not result:
            return None

        return result[0]

    def distinct(self, field_name: str) -> list:
        """Get a list of distinct values for field_name among all documents in the collection.
        """
        from ._api import get_by_ref
        values = self._mock.collection.distinct(field_name, self._query.compile())

        r = []
        for v in values:
            # Transform references to entities
            if isinstance(v, _DBRef):
                v = get_by_ref(v)
            r.append(v)

        return r


def _cache_put(finder: Finder, result: Result):
    """Put query result into cache.
    """
    _cache.get_pool(_pool_prefix + finder.model).put(finder.id, result.ids, finder.cache_ttl)


def _cache_has(finder: Finder) -> bool:
    """Check if cache has stored result for query.
    """
    return _cache.get_pool(_pool_prefix + finder.model).has(finder.id)


def _cache_get(finder: Finder) -> _Union[list, None]:
    """Get stored query result from cache.
    """
    return _cache.get_pool(_pool_prefix + finder.model).get(finder.id)


def cache_create_pool(model: str):
    """Create cache pool to tore query results of particular model.
    """
    _cache.create_pool(_pool_prefix + model, _reg.get('odm.cache.driver', 'redis'))


def cache_clear(model: str):
    """Clear cached query results of particular model,
    """
    if _dbg:
        _logger.debug("CLEAR query cache for model: '{}'.".format(model))

    _cache.clear_pool(_pool_prefix + model)
