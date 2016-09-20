"""ODM Validation Rules.
"""
from bson.objectid import ObjectId as _ObjectId
from pytsite import validation as _pytsite_validation
from . import _api, _model

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class ODMEntitiesList(_pytsite_validation.rule.Base):
    """Check if the value is a list of references to entities.
    """

    def __init__(self, value=None, msg_id: str = None, msg_args: dict = None, **kwargs):
        """Init.
        """
        super().__init__(value, msg_id, msg_args)
        self._model = kwargs.get('model')

    def _do_validate(self):
        """Do actual validation of the rule.
        """
        if self._value is None:
            return

        if not isinstance(self._value, list):
            raise TypeError('List expected.')

        for v in self._value:
            if not isinstance(v, _model.Entity):
                m_args = dict(self._msg_args, detail='Instance of ODMModel expected.')
                raise _pytsite_validation.error.RuleError(self._msg_id, m_args)
            if self._model and v.model != self._model:
                m_args = dict(self._msg_args, detail="Instance of '{}' model expected, but '{}' given.".
                              format(self._model, v.model))
                raise _pytsite_validation.error.RuleError(self._msg_id, m_args)


class FieldUnique(_pytsite_validation.rule.Base):
    def __init__(self, value=None, msg_id: str = None, msg_args: dict = None, **kwargs):
        """Init.

        :param exclude_ids: tuple | _ObjectId | str
        """
        if not msg_id:
            msg_id = 'pytsite.odm@validation_field_unique'

        super().__init__(value, msg_id, msg_args)

        self._model = kwargs.get('model')
        if not self._model:
            raise RuntimeError("'model' argument is required")

        self._field = kwargs.get('field')
        if not self._field:
            raise RuntimeError("'field' argument is required")

        self._exclude_ids = kwargs.get('exclude_ids', ())
        if type(self._exclude_ids) in (str, _ObjectId):
            self._exclude_ids = (self._exclude_ids,)

        self._msg_args.update({'field': self._field})

    def _do_validate(self):
        """Do actual validation of the rule.
        """
        # Empty values should be checked by 'NonEmpty' rule, if necessary
        if not self.value:
            return

        f = _api.find(self._model).eq(self._field, self.value)

        if self._exclude_ids:
            f.ninc('_id', self._exclude_ids)

        if f.count():
            raise _pytsite_validation.error.RuleError(self._msg_id, self._msg_args)
