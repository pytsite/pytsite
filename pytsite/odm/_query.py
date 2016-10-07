from typing import Any as _Any, Union as _Union
from bson import ObjectId as _ObjectId
from pytsite import lang as _lang
from . import _model, _geo


class Query:
    """Query Representation.
    """

    def __init__(self, entity_mock: _model.Entity):
        """Init.
        """
        # Mock entity to determine field types, etc
        self._entity_mock = entity_mock

        # 'Compiled' search criteria
        self._criteria = {}

        # To support __len__()
        self._len = 0

    @staticmethod
    def _resolve_logical_op(op: str) -> str:
        """Resolve logical operator.
        """
        if op not in ('and', 'or', '$and', '$or'):
            raise TypeError("Invalid logical operator: '{}'.".format(op))
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
        elif op in ('nearSphere', '$nearSphere'):
            return '$nearSphere'
        elif op in ('minDistance', '$minDistance'):
            return '$minDistance'
        elif op in ('maxDistance', '$maxDistance'):
            return '$maxDistance'
        else:
            raise TypeError("Invalid comparison operator: '{}'.".format(op))

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

    def _sanitize_object_ids(self, ids: _Union[str, list, tuple]) -> _Union[_ObjectId, list]:
        if isinstance(ids, _ObjectId):
            return ids
        elif isinstance(ids, str):
            return _ObjectId(ids)
        elif isinstance(ids, (list, tuple)):
            clean_arg = []
            for i in ids:
                clean_arg.append(self._sanitize_object_ids(i))

            return clean_arg
        else:
            TypeError('{} cannot be converted to object id(s).'.format(type(ids)))

    def add_criteria(self, logical_op: str, field_name: str, comparison_op: str, arg: _Any):
        """Add find criteria.
        """
        logical_op = self._resolve_logical_op(logical_op)
        comparison_op = self._resolve_comparison_op(comparison_op)

        # It is possible to perform checks only for top-level fields
        if field_name.find('.') < 0:
            if field_name == '_id':
                arg = self._sanitize_object_ids(arg)
            else:
                # Get field object to perform check
                field = self._entity_mock.get_field(field_name)

                # Convert arg to searchable form
                arg = field.sanitize_finder_arg(arg)

        # Checking for argument type
        if comparison_op in ('$in', '$nin') and not isinstance(arg, (list, tuple)):
            arg = [arg]
        elif comparison_op == '$near' and not isinstance(arg, (list, tuple)):
            raise TypeError('$near agrument should be specified as a list or a tuple.')
        elif comparison_op == '$nearSphere' and not isinstance(arg, _geo.Point):
            raise TypeError('$near agrument should be specified as a geo point.')

        # Adding logical operator's dictionary to the criteria
        if logical_op not in self._criteria:
            self._criteria[logical_op] = []

        # Finally adding the criteria
        if comparison_op == '$regex_i':
            self._criteria[logical_op].append({field_name: {'$regex': arg, '$options': 'i'}})
        elif comparison_op == '$nearSphere':
            self._criteria[logical_op].append({field_name: {'$nearSphere': arg.as_dict()}})
        else:
            self._criteria[logical_op].append({field_name: {comparison_op: arg}})

        self._len += 1

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

        self._len += 1

    def remove_criteria(self, logical_op: str, field_name: str):
        logical_op = self._resolve_logical_op(logical_op)

        if logical_op not in self._criteria:
            return

        clean = []
        for item in self._criteria[logical_op]:
            if field_name not in item:
                clean.append(item)

        if clean:
            self._criteria[logical_op] = clean
        else:
            del self._criteria[logical_op]

        self._len -= 1

    def compile(self) -> list:
        """Get compiled query.
        """
        return self._criteria

    def __len__(self) -> int:
        return self._len

    def __str__(self):
        return str(self._criteria)
