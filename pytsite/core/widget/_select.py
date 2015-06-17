"""Checkboxes Widgets.
"""
from datetime import datetime
from pytsite.core import assetman, client
from pytsite.core.widget._abstract import Widget
from pytsite.core.widget._input import Text

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite.core import lang, html
from ._input import Input as InputWidget


class Checkbox(InputWidget):
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

        em = html.Input(uid=self._uid, name=self._name, type='checkbox', checked=self._value)
        em = em.wrap(html.Label(self._label, label_for=self._uid))
        div = em.wrap(html.Div(cls='checkbox'))

        div.append(html.Input(type='hidden', name=self._name))

        return self._group_wrap(div.render(), False)


class Select(InputWidget):
    """Select Widget.
    """

    def __init__(self, **kwargs: dict):
        """Init.
        """
        self._items = kwargs.get('items', [])
        self._selected_item = None

        super().__init__(**kwargs)
        if not isinstance(self._items, list):
            raise TypeError('List expected.')

    def set_value(self, value, **kwargs: dict):
        """Set value of the widget.
        """
        self._selected_item = value
        return super().set_value(value, **kwargs)

    def render(self):
        """Render the widget.
        """
        select = html.Select(name=self.uid, cls='form-control')
        for item in self._items:
            option = html.Option(item[1], value=item[0])
            if item[0] == self._selected_item:
                option.set_attr('selected', True)
            select.append(option)

        return self._group_wrap(select.render())


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
        div = html.Div()
        div.append(html.Input(type='hidden', name=self.uid))
        for item in self._items:
            checked = True if item[0] in self._selected_items else False
            div.append(
                html.Div(cls='checkbox').append(
                    html.Label(item[1]).append(
                        html.Input(type='checkbox', name=self.uid, value=item[0], checked=checked)
                    )
                )
            )

        return self._group_wrap(div.render())


class LanguageSelect(Select):
    """Select Language Widget
    """

    def __init__(self, **kwargs: dict):
        """Init.
        """
        super().__init__(**kwargs)
        self._items = kwargs.get('items', [])

        for code in lang.get_langs():
            self._items.append((code, lang.get_lang_title(code)))


class TokenSelect(Widget):
    def __init__(self, **kwargs):
        """Init.
        """
        super().__init__(**kwargs)
        self._group_cls = ' '.join((self._group_cls, 'widget-token-input'))
        client.include('tokenfield')
        assetman.add('pytsite.core.widget@css/token.css')
        assetman.add('pytsite.core.widget@js/token.js')

        self._local_source = kwargs.get('local_source')
        self._remote_source = kwargs.get('remote_source')
        self._group_data = {
            'local_source': self._local_source,
            'remote_source': self._remote_source,
        }

    def render(self) -> str:
        """Render the widget.
        """
        html_input = html.Input(
            type='text',
            uid=self._uid,
            name=self._name,
            value=','.join(self.get_value()),
            cls=' '.join(('form-control', self._cls)),
        )

        return self._group_wrap(html_input.render())


class DateTimeSelect(Text):
    def __init__(self, **kwargs):
        """Init.
        """
        super().__init__(**kwargs)
        client.include('datetimepicker')
        assetman.add('pytsite.core.widget@js/datetime.js')
        self._group_cls = self._group_cls.replace('widget-text-input', 'widget-datetime-input')

    def set_value(self, value, **kwargs: dict):
        """Set value of the widget.
        """
        if value and isinstance(value, str):
            value = datetime.strptime(value, '%d.%m.%Y %H:%M')

        return super().set_value(value, **kwargs)

    def get_value(self, **kwargs: dict) -> datetime:
        """Get value of the widget.
        """
        return super().get_value(**kwargs)

    def render(self) -> str:
        """Render the widget
        """
        html_input = html.Input(
            type='text',
            uid=self._uid,
            name=self._name,
            value=self.get_value().strftime('%d.%m.%Y %H:%M'),
            cls=' '.join(('form-control', self._cls)),
        )

        return self._group_wrap(html_input.render())