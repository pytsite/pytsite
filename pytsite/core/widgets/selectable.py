"""Checkboxes Widgets.
"""
from datetime import datetime
from pytsite.core import assetman, client
from pytsite.core.widgets.abstract import AbstractWidget
from pytsite.core.widgets.input import TextInputWidget

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite.core.lang import get_langs, get_lang_title
from pytsite.core.html import Input as HtmlInput, Select as HtmlSelect, Option as HtmlOption, Label, Div
from .input import InputWidget


class CheckboxWidget(InputWidget):
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

        em = HtmlInput(uid=self._uid, name=self._name, type='checkbox', checked=self._value)
        em = em.wrap(Label(self._label, label_for=self._uid))
        div = em.wrap(Div(cls='checkbox'))

        div.append(HtmlInput(type='hidden', name=self._name))

        return self._group_wrap(div.render(), False)


class SelectWidget(InputWidget):
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
        select = HtmlSelect(name=self.uid, cls='form-control')
        for item in self._items:
            option = HtmlOption(item[1], value=item[0])
            if item[0] == self._selected_item:
                option.set_attr('selected', True)
            select.append(option)

        return self._group_wrap(select.render())


class CheckboxesWidget(SelectWidget):
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
        div = Div()
        div.append(HtmlInput(type='hidden', name=self.uid))
        for item in self._items:
            checked = True if item[0] in self._selected_items else False
            div.append(
                Div(cls='checkbox').append(
                    Label(item[1]).append(
                        HtmlInput(type='checkbox', name=self.uid, value=item[0], checked=checked)
                    )
                )
            )

        return self._group_wrap(div.render())


class LanguageSelectWidget(SelectWidget):
    """Select Language Widget
    """

    def __init__(self, **kwargs: dict):
        """Init.
        """
        super().__init__(**kwargs)
        self._items = kwargs.get('items', [])

        for code in get_langs():
            self._items.append((code, get_lang_title(code)))


class TokenSelectWidget(AbstractWidget):
    def __init__(self, **kwargs):
        """Init.
        """
        super().__init__(**kwargs)
        self._group_cls = ' '.join((self._group_cls, 'widget-token-input'))
        client.include('tokenfield')
        assetman.add('pytsite.core.widgets@css/token.css')
        assetman.add('pytsite.core.widgets@js/token.js')

        self._local_source = kwargs.get('local_source')
        self._remote_source = kwargs.get('remote_source')
        self._group_data = {
            'local_source': self._local_source,
            'remote_source': self._remote_source,
        }

    def render(self) -> str:
        """Render the widget.
        """
        html_input = HtmlInput(
            type='text',
            uid=self._uid,
            name=self._name,
            value=','.join(self.get_value()),
            cls=' '.join(('form-control', self._cls)),
        )

        return self._group_wrap(html_input.render())


class DateTimeWidget(TextInputWidget):
    def __init__(self, **kwargs):
        """Init.
        """
        super().__init__(**kwargs)
        client.include('datetimepicker')
        assetman.add('pytsite.core.widgets@js/datetime.js')
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
        html_input = HtmlInput(
            type='text',
            uid=self._uid,
            name=self._name,
            value=self.get_value().strftime('%d.%m.%Y %H:%M'),
            cls=' '.join(('form-control', self._cls)),
        )

        return self._group_wrap(html_input.render())