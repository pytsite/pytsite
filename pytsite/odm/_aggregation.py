from typing import Any as _Any
from . import _api, _query


class Aggregator:
    def __init__(self, model: str):
        self._model = model
        self._entity_mock = _api.dispense(model)
        self._match = _query.Query(self._entity_mock)
        self._group = []

    def match(self, field_name: str, comparison_op: str, arg: _Any):
        """Add a match query.
        """
        self._match.add_criteria('$and', field_name, comparison_op, arg)

        return self

    def group(self, expression):
        """Add a group expression.
        """
        self._group.append(expression)

        return self

    def _compile(self) -> dict:
        """Compile pipeline expression.
        """
        r = []

        if len(self._match):
            r.append({
                '$match': self._match.compile()
            })

        for g in self._group:
            r.append({
                '$group': g
            })

        return r

    def get(self) -> list:
        """Perform aggregation operation.
        """
        return self._entity_mock.collection.aggregate(self._compile())
