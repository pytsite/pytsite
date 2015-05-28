"""ODM UI Widgets.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite.core.widgets.input import CheckboxesWidget
from pytsite.core.odm import odm_manager, I_ASC
from pytsite.core.lang import t


class EntityCheckboxesWidget(CheckboxesWidget):
    """Select Entities with Checkboxes Widget.
    """

    def __init__(self, **kwargs: dict):
        """Init.
        """

        super().__init__(**kwargs)

        self._model = kwargs.get('model')
        self._caption_field = kwargs.get('caption_field')

        if not self._model:
            raise ValueError('Model is not specified.')

        if not self._caption_field:
            raise ValueError('Caption field is not specified.')

        if not odm_manager.is_model_registered(self._model):
            raise Exception("Model '{}' is not registered.")

    def render(self):
        """Render the widget.
        """

        print(self.value)

        finder = odm_manager.find(self._model).sort([(self._caption_field, I_ASC)])
        for entity in finder.get():
            k = entity.model + ':' + str(entity.id)
            self._available_values.append((k, t(str(entity.get_field(self._caption_field)))))

        return super().render()

    @property
    def value(self):
        """Get value of the widget.

        :rtype: list[pytsite.core.odm.models.ODMModel]
        """
        return self._value

    @value.setter
    def value(self, val):
        """Set value of the widget.

        :param val: list[pytsite.core.odm.models.ODMModel] | list[DBRef] | list[str]
        """

        # Single string can be passed from HTML form
        if isinstance(val, str):
            val = [val] if len(val) else []

        if not isinstance(val, list):
            raise TypeError('List of entities expected')

        clean_val = []
        for v in val:
            if not v:
                continue
            entity = odm_manager.dispense_by_ref(odm_manager.resolve_ref(v))
            if entity:
                clean_val.append(entity)

        self._value = clean_val
