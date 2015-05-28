"""ODM Validation Rules.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


from pytsite.core.validation.rules import BaseRule
from pytsite.core.validation.errors import ValidationError
from . import odm_manager
from .models import ODMModel


class ODMEntitiesListRule(BaseRule):
    """Check if the value is a list of references.
    """

    def __init__(self, msg_id: str=None, value=None, model: str=None):
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
            raise ValidationError('List expected.')

        for v in self._value:
            if not isinstance(v, ODMModel):
                raise ValidationError('Instance of ODMModel expected.')
            if self._model and v.model != self._model:
                raise ValidationError("Instance of '{}' model expected, but '{}' given.".format(self._model, v.model))
