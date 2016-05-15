from typing import Iterable as _Iterable, Any as _Any
from bson import ObjectId as _ObjectId
from pytsite import lang as _lang
from . import _entity, _geo, _field


class Query:
    """Query Representation.
    """

    def __init__(self, entity_mock: _entity.Entity):
        """Init.
        """
        self._entity_mock = entity_mock
        self._criteria = {}
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

    def add_criteria(self, logical_op: str, field_name: str, comparison_op: str, arg: _Any):
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
                field = self._entity_mock.get_field(field_name)

                # Convert instance(s) to DBRef(s)
                if isinstance(field, _field.Ref):
                    if isinstance(arg, _entity.Entity):
                        arg = arg.ref
                    elif isinstance(arg, (list, tuple)):
                        clean_arg = []
                        for v in arg:
                            if isinstance(v, _entity.Entity):
                                clean_arg.append(v.ref)
                            else:
                                clean_arg.append(v)
                        arg = clean_arg

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
            if not isinstance(arg, (list, tuple)):
                raise TypeError('$near agrument should be specified as a list or a tuple.')
        if comparison_op == '$nearSphere':
            if not isinstance(arg, _geo.Point):
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

        self._criteria[logical_op] = clean

        self._len -= 1

    def compile(self) -> list:
        """Get compiled query.
        """
        return self._criteria

    def __len__(self) -> int:
        return self._len
