"""Description.
"""
from typing import Iterable as _Iterable, Union as _Union
from bson import DBRef as _DBRef
from pymongo.cursor import Cursor as _Cursor, CursorType as _CursorType
from pytsite import util as _util, reg as _reg, cache as _cache, logger as _logger
from . import _model, _api, _query

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

_pool_prefix = 'pytsite.odm.finder:'
_dbg = _reg.get('odm.debug.finder')


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

    def __next__(self) -> _model.Entity:
        """Get next item.
        """
        if self._current == self._total:
            raise StopIteration()

        entity = _api.dispense(self._model, self._ids[self._current])
        self._current += 1

        return entity

    def __len__(self) -> int:
        return self._total

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
    def __init__(self, model: str, cache_pool: _cache.driver.Abstract):
        """Init.
        """
        self._model = model
        self._cache_pool = cache_pool
        self._mock = _api.dispense(model)
        self._query = _query.Query(self._mock)
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
    def mock(self) -> _model.Entity:
        """Get entity mock.
        """
        return self._mock

    @property
    def query(self) -> _query.Query:
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
        """Add an '$and' criteria.
        """
        self._query.add_criteria('$and', field_name, comparison_op, arg)

        return self

    def eq(self, field_name: str, arg):
        """Add an '$and $eq' criteria.
        """
        self._query.add_criteria('$and', field_name, '$eq', arg)

        return self

    def gt(self, field_name: str, arg):
        """Add an '$and $gt' criteria.
        """
        self._query.add_criteria('$and', field_name, '$gt', arg)

        return self

    def gte(self, field_name: str, arg):
        """Add an '$and $gte' criteria.
        """
        self._query.add_criteria('$and', field_name, '$gte', arg)

        return self

    def lt(self, field_name: str, arg):
        """Add an '$and $lt' criteria.
        """
        self._query.add_criteria('$and', field_name, '$lt', arg)

        return self

    def lte(self, field_name: str, arg):
        """Add an '$and $lte' criteria.
        """
        self._query.add_criteria('$and', field_name, '$lte', arg)

        return self

    def ne(self, field_name: str, arg):
        """Add an '$and $ne' criteria.
        """
        self._query.add_criteria('$and', field_name, '$ne', arg)

        return self

    def inc(self, field_name: str, arg):
        """Add an '$and $in' criteria.
        """
        self._query.add_criteria('$and', field_name, '$in', arg)

        return self

    def ninc(self, field_name: str, arg):
        """Add an '$and $nin' criteria.
        """
        self._query.add_criteria('$and', field_name, '$nin', arg)

        return self

    def or_where(self, field_name: str, comparison_op: str, arg):
        """Add '$or' criteria.
        """
        self._query.add_criteria('$or', field_name, comparison_op, arg)

        return self

    def or_eq(self, field_name: str, arg):
        """Add an '$or $eq' criteria.
        """
        self._query.add_criteria('$or', field_name, '$eq', arg)

        return self

    def or_gt(self, field_name: str, arg):
        """Add an '$or $gt' criteria.
        """
        self._query.add_criteria('$or', field_name, '$gt', arg)

        return self

    def or_gte(self, field_name: str, arg):
        """Add an '$or $gte' criteria.
        """
        self._query.add_criteria('$or', field_name, '$gte', arg)

        return self

    def or_lt(self, field_name: str, arg):
        """Add an '$or $lt' criteria.
        """
        self._query.add_criteria('$or', field_name, '$lt', arg)

        return self

    def or_lte(self, field_name: str, arg):
        """Add an '$or $lte' criteria.
        """
        self._query.add_criteria('$or', field_name, '$lte', arg)

        return self

    def or_ne(self, field_name: str, arg):
        """Add an '$or $ne' criteria.
        """
        self._query.add_criteria('$or', field_name, '$ne', arg)

        return self

    def or_inc(self, field_name: str, arg):
        """Add an '$or $in' criteria.
        """
        self._query.add_criteria('$or', field_name, '$in', arg)

        return self

    def or_ninc(self, field_name: str, arg):
        """Add an '$or $nin' criteria.
        """
        self._query.add_criteria('$or', field_name, '$nin', arg)

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

    def get(self, limit: int = 0) -> _Union[_Iterable[_model.Entity], Result]:
        """Execute the query and return a cursor.
        """
        self._limit = limit
        query = self._query.compile()

        # Search for previous result in cache
        if _reg.get('odm.cache.enabled', True) and self._cache_ttl:
            try:
                ids = self._cache_pool.get(self.id)
                if _dbg:
                    _logger.debug("GET cached query results: query: {}, {}, id: {}, entities: {}.".
                                  format(self.model, self.query.compile(), self.id, len(ids)))
                return Result(self._model, ids=ids)

            except _cache.error.KeyNotExist:
                pass

        cursor = self._mock.collection.find(
            filter=query,
            projection={'_id': True},
            skip=self._skip,
            limit=self._limit,
            cursor_type=_CursorType.NON_TAILABLE,
            sort=self._sort,
        )

        result = Result(self._model, cursor)

        # Put query result into cache
        if _reg.get('odm.cache.enabled', True) and self._cache_ttl:
            if _dbg:
                _logger.debug("STORE query results: query: {}, {}, id: {}, entities: {}, TTL: {}.".
                              format(self.model, self.query.compile(), self.id, result.count(), self._cache_ttl))

            self._cache_pool.put(self.id, result.ids, self._cache_ttl)

        return result

    def first(self) -> _Union[_model.Entity, None]:
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
