from typing import Any as _Any
from . import _api, _query


class Aggregator:
    """Abstraction of MongoDB Pipeline Aggregation

    https://docs.mongodb.com/manual/reference/operator/aggregation-pipeline/
    """

    def __init__(self, model: str):
        """Init
        """
        self._model = model
        self._mock = _api.dispense(model)
        self._pipeline = []

    def match(self, field_name: str, comparison_op: str, arg: _Any):
        """Add a match stage

        https://docs.mongodb.com/manual/reference/operator/aggregation/match/
        """
        q = _query.Query(self._mock)
        q.add_criteria('$and', field_name, comparison_op, arg)

        self._pipeline.append(('match', q))

        return self

    def group(self, expression: dict):
        """Add a group stage

        https://docs.mongodb.com/manual/reference/operator/aggregation/group/
        """
        self._pipeline.append(('group', expression))

        return self

    def lookup(self, foreign_model: str, local_field: str, foreign_field: str, as_field: str):
        """Add a lookup stage

        https://docs.mongodb.com/manual/reference/operator/aggregation/lookup/
        """
        self._pipeline.append(('lookup', (foreign_model, local_field, foreign_field, as_field)))

        return self

    def _compile(self) -> list:
        """Compile pipeline expression
        """
        r = []

        for stage in self._pipeline:
            if stage[0] == 'match':
                r.append({
                    '$match': stage[1].compile(),
                })

            elif stage[0] == 'group':
                r.append({
                    '$group': stage[1],
                })

            elif stage[0] == 'lookup':
                r.append({
                    '$lookup': {
                        'from': stage[1][0],
                        'localField': stage[1][1],
                        'foreignField': stage[1][2],
                        'as': stage[1][3],
                    }
                })

        return r

    def get(self) -> list:
        """Perform aggregation operation.
        """
        return self._mock.collection.aggregate(self._compile())
