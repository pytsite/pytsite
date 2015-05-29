"""Checkboxes Widgets.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

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

        return self._group_wrap(div.render(), render_label=False)


class SelectWidget(InputWidget):
    """Select Widget.
    """

    def __init__(self, **kwargs: dict):
        """Init.
        """

        self._items = kwargs.get('items', [])

        super().__init__(**kwargs)

        if not isinstance(self._items, list):
            raise TypeError('List expected.')

    def render(self):
        """Render the widget.
        """

        select = HtmlSelect(name=self.uid, cls='form-control')
        for item in self._items:
            select.append(HtmlOption(content=item[1], value=item[0]))

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

    def set_value(self, val: list, **kwargs):
        """Set value of the widget.
        """

        if not isinstance(val, list):
            raise TypeError('List expected')

        self._value = val
        self._selected_items = val

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
