"""ODM Validation Rules.
"""
from bson.objectid import ObjectId as _ObjectId
from pytsite import validation as _pytsite_validation
from . import _api, _entity

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class ODMEntitiesList(_pytsite_validation.rule.Base):
    """Check if the value is a list of references.
    """
    def __init__(self, value=None, msg_id: str=None, model: str=None):
        """Init.
        """
        super().__init__(value, msg_id)
        self._model = model

    def _do_validate(self):
        """Do actual validation of the rule.
        """
        if self._value is None:
            return

        if not isinstance(self._value, list):
            raise ValueError('List expected.')

        for v in self._value:
            if not isinstance(v, _entity.Entity):
                raise _pytsite_validation.error.RuleError(self._msg_id, {
                    'detail': 'Instance of ODMModel expected.'})
            if self._model and v.model != self._model:
                raise _pytsite_validation.error.RuleError(self._msg_id, {
                    'detail': "Instance of '{}' model expected, but '{}' given.".format(self._model, v.model)})


class FieldUnique(_pytsite_validation.rule.Base):
    def __init__(self, value=None, msg_id: str=None, model: str=None, field: str=None, exclude_ids=None):
        """Init.

        :param exclude_ids: tuple | _ObjectId | str
        """
        if not msg_id:
            msg_id = 'pytsite.odm@validation_field_unique'

        super().__init__(value, msg_id)
        self._model = model
        self._field = field
        self._exclude_ids = exclude_ids if exclude_ids else ()

        if type(self._exclude_ids) in (str, _ObjectId):
            self._exclude_ids = (self._exclude_ids,)

    def _do_validate(self):
        """Do actual validation of the rule.
        """
        f = _api.find(self._model).where(self._field, '=', self._value)

        if self._exclude_ids:
            f.where('_id', 'nin', self._exclude_ids)

        if f.count():
            raise _pytsite_validation.error.RuleError(self._msg_id, {'field': self._field})
