"""Checkboxes Widgets.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from datetime import datetime as _datetime
from pytsite import assetman as _assetman, browser as _client, html as _html, lang as _lang
from . import _input


class Checkbox(_input.Input):
    """Single Checkbox Widget.
    """

    def __init__(self, **kwargs: dict):
        """Init.
        """
        super().__init__(**kwargs)

    def set_value(self, value, **kwargs):
        """Set value of the widget.
        """
        self._value = bool(value)

    def render(self):
        """Render the widget.
        """

        em = _html.Input(uid=self._entity, name=self._name, type='checkbox', checked=self._value)
        em = em.wrap(_html.Label(self._label, label_for=self._entity))
        div = em.wrap(_html.Div(cls='checkbox'))

        div.append(_html.Input(type='hidden', name=self._name))

        return self._group_wrap(div, False)


class Select(_input.Input):
    """Select Widget.
    """
    def __init__(self, **kwargs: dict):
        """Init.
        """
        self._items = kwargs.get('items', [])
        self._selected_item = None

        super().__init__(**kwargs)
        if not isinstance(self._items, list) and not isinstance(self._items, tuple) :
            raise TypeError('List or tuple expected.')

    def set_value(self, value, **kwargs: dict):
        """Set value of the widget.
        """
        self._selected_item = value
        return super().set_value(value, **kwargs)

    def render(self):
        """Render the widget.
        """
        select = _html.Select(name=self.uid, cls='form-control')
        select.append(_html.Option('--- ' + _lang.t('pytsite.widget@select_none_item') + ' ---', value=''))
        for item in self._items:
            option = _html.Option(item[1], value=item[0])
            if item[0] == self._selected_item:
                option.set_attr('selected', True)
            select.append(option)

        return self._group_wrap(select)


class Checkboxes(Select):
    """Group of Checkboxes Widget.
    """
    def __init__(self, **kwargs: dict):
        """Init.
        """
        super().__init__(**kwargs)

        self.set_value(kwargs.get('value', []))

        if not isinstance(self._value, list):
            raise TypeError("List expected.")

        self._selected_items = kwargs.get('selected_items', self._value)

    def set_value(self, value: list, **kwargs):
        """Set value of the widget.
        """

        if not isinstance(value, list):
            raise TypeError('List expected')

        self._value = value
        self._selected_items = value

    def render(self) -> str:
        """Render the widget.
        """
        div = _html.Div()
        div.append(_html.Input(type='hidden', name=self.uid))
        for item in self._items:
            checked = True if item[0] in self._selected_items else False
            div.append(
                _html.Div(cls='checkbox').append(
                    _html.Label(item[1]).append(
                        _html.Input(type='checkbox', name=self.uid, value=item[0], checked=checked)
                    )
                )
            )

        return self._group_wrap(div)


class Language(Select):
    """Select Language Widget
    """
    def __init__(self, **kwargs: dict):
        """Init.
        """
        super().__init__(**kwargs)
        self._items = kwargs.get('items', [])

        for code in _lang.get_langs():
            self._items.append((code, _lang.get_lang_title(code)))


class DateTime(_input.Text):
    def __init__(self, **kwargs):
        """Init.
        """
        super().__init__(**kwargs)
        _client.include('datetimepicker')
        _assetman.add('pytsite.widget@js/datetime.js')

        self._css = self._css.replace('widget-input-text', 'widget-select-datetime')

    def set_value(self, value, **kwargs: dict):
        """Set value of the widget.
        """
        if value and isinstance(value, str):
            value = _datetime.strptime(value, '%d.%m.%Y %H:%M')

        return super().set_value(value, **kwargs)

    def get_value(self, **kwargs: dict) -> _datetime:
        """Get value of the widget.
        """
        return super().get_value(**kwargs)

    def render(self) -> str:
        """Render the widget
        """
        html_input = _html.Input(
            type='text',
            uid=self._entity,
            name=self._name,
            value=self.get_value().strftime('%d.%m.%Y %H:%M'),
            cls=' '.join(('form-control', self._css)),
        )

        return self._group_wrap(html_input)
