"""ODM Validation Rules.
"""
from bson.objectid import ObjectId as _ObjectId
from pytsite import validation as _core_validation
from . import _functions, _model

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class ODMEntitiesList(_core_validation.rule.Base):
    """Check if the value is a list of references.
    """
    def __init__(self, model: str, msg_id: str=None, value=None):
        """Init.
        """
        super().__init__(msg_id, value)
        self._model = model

    def _do_validate(self, validator=None, field_name: str=None):
        """Do actual validation of the rule.
        """
        if self._value is None:
            return

        if not isinstance(self._value, list):
            raise ValueError('List expected.')

        for v in self._value:
            if not isinstance(v, _model.Model):
                raise _core_validation.error.ValidationError({
                    'detail': 'Instance of ODMModel expected.'})
            if self._model and v.model != self._model:
                raise _core_validation.error.ValidationError({
                    'detail': "Instance of '{}' model expected, but '{}' given.".format(self._model, v.model)})


class FieldUnique(_core_validation.rule.Base):
    def __init__(self, model: str, field: str, msg_id: str=None, value=None, **kwargs):
        """Init.
        :param exclude_ids: tuple | _ObjectId | str
        """
        if not msg_id:
            msg_id = 'pytsite.odm@validation_field_unique'

        super().__init__(msg_id, value)
        self._model = model
        self._field = field
        self._exclude_ids = kwargs.get('exclude_ids')

        if type(self._exclude_ids) in (str, _ObjectId):
            self._exclude_ids = (self._exclude_ids,)

    def _do_validate(self, validator=None, field_name: str=None):
        """Do actual validation of the rule.
        """
        f = _functions.find(self._model).where(self._field, '=', self._value)

        if self._exclude_ids:
            f.where('_id', 'nin', self._exclude_ids)

        if f.count():
            raise _core_validation.error.ValidationError({'field': self._field})
