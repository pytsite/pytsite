"""PytSite ODM Finder
"""
from typing import Iterable as _Iterable, Union as _Union
from bson import DBRef as _DBRef
from pymongo.cursor import Cursor as _Cursor, CursorType as _CursorType
from pytsite import util as _util, reg as _reg, cache as _cache, logger as _logger
from . import _model, _api, _query

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

_DBG = _reg.get('odm.debug.finder')
_DEFAULT_CACHE_TTL = _reg.get('odm.cache.ttl', 86400)  # 24 hours


class Result:
    """Finder Result
    """

    def __init__(self, model: str, cursor: _Cursor = None, ids: list = None):
        """Init.
        """
        self._model = model
        self._cursor = cursor
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
        self._cache_ttl = _DEFAULT_CACHE_TTL
        self._cache_key = {'$and': {}, '$or': {}}
        self._mock = _api.dispense(model)
        self._query = _query.Query(self._mock)
        self._skip = 0
        self._limit = 0
        self._sort = None

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
        """Get unique finder's ID to use as a cache key, etc
        """
        return _util.md5_hex_digest(str((self._cache_key, self._skip, self._limit, self._sort)))

    @property
    def cache_ttl(self) -> int:
        """Get query's cache TTL
        """
        return self._cache_ttl

    @cache_ttl.setter
    def cache_ttl(self, value: int):
        """Set query's cache TTL
        """
        self._cache_ttl = value

    def cache(self, ttl: int):
        """Set query's cache TTL
        """
        self._cache_ttl = ttl

        return self

    def _add_query_criteria(self, logical_op: str, field_name: str, comparison_op: str, arg, cache: bool = True):
        self._query.add_criteria(logical_op, field_name, comparison_op, arg)

        if cache:
            if field_name not in self._cache_key[logical_op]:
                self._cache_key[logical_op][field_name] = []

            self._cache_key[logical_op][field_name].append((comparison_op, str(arg)))

        return self

    def _remove_query_field(self, logical_op: str, field_name: str):
        self._query.remove_field(logical_op, field_name)

        if field_name in self._cache_key[logical_op]:
            del self._cache_key[logical_op]

        return self

    def _add_text_search(self, logical_op: str, search: str, language: str = None, cache: bool = True):
        self._query.add_text_search(logical_op, search, language)

        if cache:
            if '$text' not in self._cache_key[logical_op]:
                self._cache_key[logical_op]['$text'] = None

            self._cache_key[logical_op]['$text'] = (search, language)

        return self

    def where(self, field_name: str, comparison_op: str, arg, cache: bool = True):
        """Add an '$and' criteria
        """
        return self._add_query_criteria('$and', field_name, comparison_op, arg, cache)

    def eq(self, field_name: str, arg, cache: bool = True):
        """Add an '$and $eq' criteria
        """
        return self._add_query_criteria('$and', field_name, '$eq', arg, cache)

    def gt(self, field_name: str, arg, cache: bool = True):
        """Add an '$and $gt' criteria.
        """
        return self._add_query_criteria('$and', field_name, '$gt', arg, cache)

    def gte(self, field_name: str, arg, cache: bool = True):
        """Add an '$and $gte' criteria.
        """
        return self._add_query_criteria('$and', field_name, '$gte', arg, cache)

    def lt(self, field_name: str, arg, cache: bool = True):
        """Add an '$and $lt' criteria.
        """
        return self._add_query_criteria('$and', field_name, '$lt', arg, cache)

    def lte(self, field_name: str, arg, cache: bool = True):
        """Add an '$and $lte' criteria.
        """
        return self._add_query_criteria('$and', field_name, '$lte', arg, cache)

    def ne(self, field_name: str, arg, cache: bool = True):
        """Add an '$and $ne' criteria.
        """
        return self._add_query_criteria('$and', field_name, '$ne', arg, cache)

    def inc(self, field_name: str, arg, cache: bool = True):
        """Add an '$and $in' criteria.
        """
        return self._add_query_criteria('$and', field_name, '$in', arg, cache)

    def ninc(self, field_name: str, arg, cache: bool = True):
        """Add an '$and $nin' criteria.
        """
        return self._add_query_criteria('$and', field_name, '$nin', arg, cache)

    def or_where(self, field_name: str, comparison_op: str, arg, cache: bool = True):
        """Add '$or' criteria.
        """
        return self._add_query_criteria('$or', field_name, comparison_op, arg, cache)

    def or_eq(self, field_name: str, arg, cache: bool = True):
        """Add an '$or $eq' criteria.
        """
        return self._add_query_criteria('$or', field_name, '$eq', arg, cache)

    def or_gt(self, field_name: str, arg, cache: bool = True):
        """Add an '$or $gt' criteria.
        """
        return self._add_query_criteria('$or', field_name, '$gt', arg, cache)

    def or_gte(self, field_name: str, arg, cache: bool = True):
        """Add an '$or $gte' criteria.
        """
        return self._add_query_criteria('$or', field_name, '$gte', arg, cache)

    def or_lt(self, field_name: str, arg, cache: bool = True):
        """Add an '$or $lt' criteria.
        """
        return self._add_query_criteria('$or', field_name, '$lt', arg, cache)

    def or_lte(self, field_name: str, arg, cache: bool = True):
        """Add an '$or $lte' criteria.
        """
        return self._add_query_criteria('$or', field_name, '$lte', arg, cache)

    def or_ne(self, field_name: str, arg, cache: bool = True):
        """Add an '$or $ne' criteria.
        """
        return self._add_query_criteria('$or', field_name, '$ne', arg, cache)

    def or_inc(self, field_name: str, arg, cache: bool = True):
        """Add an '$or $in' criteria.
        """
        return self._add_query_criteria('$or', field_name, '$in', arg, cache)

    def or_ninc(self, field_name: str, arg, cache: bool = True):
        """Add an '$or $nin' criteria.
        """
        return self._add_query_criteria('$or', field_name, '$nin', arg, cache)

    def text(self, search: str, language: str = None, cache: bool = True):
        """Add '$text' criteria.
        """
        return self._add_text_search('$and', search, language, cache)

    def or_text(self, search: str, language: str = None, cache: bool = True):
        """Add '$or $text' criteria.
        """
        return self._add_text_search('$or', search, language, cache)

    def remove_field(self, field_name: str):
        """Remove field from query.
        """
        return self._remove_query_field('$and', field_name)

    def remove_or_field(self, field_name: str):
        """Remove field from query.
        """
        return self._remove_query_field('$or', field_name)

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
        if self._cache_ttl:
            try:
                ids = self._cache_pool.get(self.id)
                if _DBG:
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

        # Prepare result
        result = Result(self._model, cursor)

        # Put query result into cache
        if self._cache_ttl:
            if _DBG:
                _logger.debug("STORE query results: query: {}, {}, id: {}, entities: {}, TTL: {}.".
                              format(self.model, self.query.compile(), self.id, result.count(), self._cache_ttl))

            self._cache_pool.put(self.id, result.ids, self._cache_ttl)

        return result

    def first(self) -> _Union[_model.Entity, None]:
        """Execute the query and return a first result
        """
        result = list(self.get(1))

        if not result:
            return None

        return result[0]

    def delete(self):
        """Delete all the entities matching search criteria
        """
        for entity in self.get():
            entity.delete()

        return self

    def distinct(self, field_name: str) -> list:
        """Get a list of distinct values for field_name among all documents in the collection
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
