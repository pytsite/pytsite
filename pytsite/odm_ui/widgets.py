"""ODM UI Widgets.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from bson.dbref import DBRef
from pytsite.core.widgets.input import TypeaheadTextInputWidget
from pytsite.core.widgets.selectable import CheckboxesWidget, SelectWidget
from pytsite.core.odm import odm_manager, I_ASC
from pytsite.core.odm.models import ODMModel
from pytsite.core.lang import t


class ODMSelectWidget(SelectWidget):
    """Select Entity with Select Widget.
    """
    def __init__(self, **kwargs: dict):
        """Init.
        """
        super().__init__(**kwargs)

        self.set_value(kwargs.get('value'))
        self._model = kwargs.get('model')
        self._caption_field = kwargs.get('caption_field')

        if not self._model:
            raise ValueError('Model is not specified.')
        if not self._caption_field:
            raise ValueError('Caption field is not specified.')

        finder = odm_manager.find(self._model).sort([(self._caption_field, I_ASC)])
        for entity in finder.get():
            k = entity.model + ':' + str(entity.id)
            self._items.append((k, str(entity.get_field(self._caption_field))))

    def set_value(self, value: ODMModel, **kwargs):
        """Set value of the widget.
        """
        if isinstance(value, ODMModel):
            self._selected_item = value.model + ':' + str(value.id)
        elif isinstance(value, str):
            self._selected_item = value
            model, eid = value.split(':')
            value = odm_manager.find(model).where('_id', '=', eid).first()
        elif isinstance(value, DBRef):
            value = odm_manager.get_by_ref(value)
            self._selected_item = value.model + ':' + str(value.id)

        self._value = value
        return self


class ODMCheckboxesWidget(CheckboxesWidget):
    """Select Entities with Checkboxes Widget.
    """

    def __init__(self, **kwargs: dict):
        """Init.
        """
        super().__init__(**kwargs)

        self.set_value(kwargs.get('value'))
        self._model = kwargs.get('model')
        self._caption_field = kwargs.get('caption_field')

        if not self._model:
            raise ValueError('Model is not specified.')
        if not self._caption_field:
            raise ValueError('Caption field is not specified.')

        # Available items
        self._items = []

        finder = odm_manager.find(self._model).sort([(self._caption_field, I_ASC)])
        for entity in finder.get():
            k = entity.model + ':' + str(entity.id)
            self._items.append((k, t(str(entity.get_field(self._caption_field)))))

    def set_value(self, value, **kwargs):
        """Set value of the widget.

        :param value: list[pytsite.core.odm.models.ODMModel] | list[DBRef] | list[str]
        """

        # Single string can be passed from HTML form
        if isinstance(value, str) or value is None:
            value = [value] if value else []

        if not isinstance(value, list):
            raise TypeError('List of entities expected as a value of the widget.')

        self._selected_items = []
        clean_val = []
        for v in value:
            if not v:
                continue
            entity = odm_manager.get_by_ref(odm_manager.resolve_ref(v))
            if entity:
                clean_val.append(entity)
                self._selected_items.append(entity.model + ':' + str(entity.id))

        self._value = clean_val
