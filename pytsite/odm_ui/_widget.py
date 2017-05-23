"""ODM UI Widgets.
"""
from typing import List as _List
from bson.dbref import DBRef as _DBRef
from pytsite import widget as _widget, odm as _odm, lang as _lang

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class EntitySelect(_widget.select.Select):
    """Select Entity with Select Widget.
    """

    def __init__(self, uid: str, **kwargs):
        """Init.
        """
        super().__init__(uid, **kwargs)

        self._model = kwargs.get('model')
        if not self._model:
            raise ValueError('Model is not specified.')

        self._caption_field = kwargs.get('caption_field')
        if not self._caption_field:
            raise ValueError('Caption field is not specified.')

        self._sort_field = kwargs.get('sort_field', self._caption_field)
        self._finder_adjust = kwargs.get('finder_adjust')
        self._caption_adjust = kwargs.get('caption_adjust')

    @property
    def sort_field(self) -> str:
        return self._sort_field

    @sort_field.setter
    def sort_field(self, value: str):
        self._sort_field = value

    def set_val(self, value, **kwargs):
        """Set value of the widget.
        """
        if isinstance(value, str) and not value:
            value = None
        elif isinstance(value, _odm.model.Entity):
            value = value.model + ':' + str(value.id)
        elif isinstance(value, _DBRef):
            value = _odm.get_by_ref(value)
            value = value.model + ':' + str(value.id)

        return super().set_val(value, **kwargs)

    def _get_finder(self) -> _odm.Finder:
        finder = _odm.find(self._model).sort([(self._sort_field, _odm.I_ASC)])
        if self._finder_adjust:
            self._finder_adjust(finder)

        return finder

    def _get_caption(self, entity: _odm.model.Entity) -> str:
        caption = str(entity.f_get(self._caption_field))
        if self._caption_adjust:
            caption = self._caption_adjust(caption)

        return caption

    def _get_element(self, **kwargs):
        """Render the widget.
        :param **kwargs:
        """
        finder = self._get_finder()

        # Building items list
        for entity in finder.get():
            self._items.append((entity.ref_str, self._get_caption(entity)))

        return super()._get_element()


class EntityCheckboxes(_widget.select.Checkboxes):
    """Select Entities with Checkboxes Widget.
    """

    def __init__(self, uid: str, **kwargs):
        """Init.
        """
        super().__init__(uid, **kwargs)

        self.set_val(kwargs.get('value'))
        self._model = kwargs.get('model')
        self._caption_field = kwargs.get('caption_field')
        self._sort_field = kwargs.get('sort_field', self._caption_field)
        self._translate_captions = kwargs.get('translate_captions', False)

        if not self._model:
            raise ValueError('Model is not specified.')
        if not self._caption_field:
            raise ValueError('Caption field is not specified.')

        self._exclude = []  # type: _List[_odm.model.Entity]
        for e in kwargs.get('exclude', ()):
            entity = _odm.get_by_ref(_odm.resolve_ref(e))
            if entity:
                self._exclude.append(entity)

        # Available items will be set during call to self._get_element()
        self._items = []

    @property
    def sort_field(self) -> str:
        """Get sort field.
        """
        return self._sort_field

    @sort_field.setter
    def sort_field(self, value: str):
        """Set sort field.
        """
        self._sort_field = value

    def set_val(self, value, **kwargs):
        """Set value of the widget.

        :param value: list[pytsite.odm.models.ODMModel] | list[DBRef] | list[str]
        """

        # Single string can be received from HTML form
        if isinstance(value, str) or value is None:
            value = [value] if value else []

        if not isinstance(value, (list, tuple)):
            raise TypeError("List of entities expected as a value of the widget '{}'.".format(self.name))

        clean_val = []
        for v in value:
            if not v:
                continue

            # Check entity for existence
            entity = _odm.get_by_ref(_odm.resolve_ref(v))

            # Append entity reference as string
            if entity:
                clean_val.append(str(entity))

        return super().set_val(clean_val, **kwargs)

    def _get_element(self, **kwargs):
        finder = _odm.find(self._model).sort([(self._sort_field, _odm.I_ASC)])
        for entity in finder.get():
            k = str(entity)
            if k not in self._exclude:
                caption = str(entity.get_field(self._caption_field))
                if self._translate_captions:
                    caption = _lang.t(caption)
                self._items.append((k, caption))

        return super()._get_element()
