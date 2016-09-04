"""ODM UI Widgets.
"""
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

    def get_html_em(self, **kwargs):
        """Render the widget.
        :param **kwargs:
        """
        finder = self._get_finder()

        # Building items list
        for entity in finder.get():
            k = entity.model + ':' + str(entity.id)
            self._items.append((k, str(entity.f_get(self._caption_field))))

        return super().get_html_em()


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
        self._exclude = kwargs.get('exclude', ())
        self._sort_field = kwargs.get('sort_field', self._caption_field)

        if not self._model:
            raise ValueError('Model is not specified.')
        if not self._caption_field:
            raise ValueError('Caption field is not specified.')

        # Available items
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

    def get_html_em(self, **kwargs):
        finder = _odm.find(self._model).sort([(self._sort_field, _odm.I_ASC)])
        for entity in finder.get():
            if entity not in self._exclude:
                k = entity.model + ':' + str(entity.id)
                self._items.append((k, _lang.t(str(entity.get_field(self._caption_field)))))

        return super().get_html_em()
