"""ODM UI Widgets.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from bson.dbref import DBRef as _DBRef
from pytsite.core import widget as _widget, odm as _odm, lang as _lang


class ODMSelect(_widget.select.Select):
    """Select Entity with Select Widget.
    """
    def __init__(self, **kwargs: dict):
        """Init.
        """
        super().__init__(**kwargs)

        if not self._model:
            self._model = kwargs.get('model')
        if not self._caption_field:
            self._caption_field = kwargs.get('caption_field')
        if not self._sort_field:
            self._sort_field = kwargs.get('sort_field', self._caption_field)

        if not self._model:
            raise ValueError('Model is not specified.')
        if not self._caption_field:
            raise ValueError('Caption field is not specified.')

    @property
    def sort_field(self) -> str:
        return self._sort_field

    @sort_field.setter
    def sort_field(self, value: str):
        self._sort_field = value

    def set_value(self, value: _odm.Model, **kwargs):
        """Set value of the widget.
        """
        if isinstance(value, _odm.Model):
            self._selected_item = value.model + ':' + str(value.id)
        elif isinstance(value, str):
            if value.find(':') > 0:
                self._selected_item = value
                model, eid = value.split(':')
                value = _odm.find(model).where('_id', '=', eid).first()
        elif isinstance(value, _DBRef):
            value = _odm.get_by_ref(value)
            self._selected_item = value.model + ':' + str(value.id)

        self._value = value
        return self

    def render(self):
        finder = _odm.find(self._model).sort([(self._sort_field, _odm.I_ASC)])
        for entity in finder.get():
            k = entity.model + ':' + str(entity.id)
            self._items.append((k, str(entity.f_get(self._caption_field))))

        return super().render()


class ODMCheckboxes(_widget.select.Checkboxes):
    """Select Entities with Checkboxes Widget.
    """
    def __init__(self, **kwargs: dict):
        """Init.
        """
        super().__init__(**kwargs)

        self.set_value(kwargs.get('value'))
        self._model = kwargs.get('model')
        self._caption_field = kwargs.get('caption_field')
        self._sort_field = kwargs.get('sort_field', self._caption_field)

        if not self._model:
            raise ValueError('Model is not specified.')
        if not self._caption_field:
            raise ValueError('Caption field is not specified.')

        # Available items
        self._items = []

    @property
    def sort_field(self) -> str:
        return self._sort_field

    @sort_field.setter
    def sort_field(self, value: str):
        self._sort_field = value

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
            entity = _odm.get_by_ref(_odm.resolve_ref(v))
            if entity:
                clean_val.append(entity)
                self._selected_items.append(entity.model + ':' + str(entity.id))

        self._value = clean_val
        return self

    def render(self):
        finder = _odm.find(self._model).sort([(self._sort_field, _odm.I_ASC)])
        for entity in finder.get():
            k = entity.model + ':' + str(entity.id)
            self._items.append((k, _lang.t(str(entity.get_field(self._caption_field)))))

        return super().render()
