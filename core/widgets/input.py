"""Input Widget.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite.core.html import Input as HtmlInput, Select as HtmlSelect, Option as HtmlOption, Div, Label
from .abstract import AbstractWidget


class InputWidget(AbstractWidget):
    """Input Widget.
    """

    def render(self)->str:
        """Render the widget.
        """

        raise NotImplementedError()


class HiddenInputWidget(InputWidget):
    """Hidden Input Widget
    """

    def render(self) -> str:
        """Render the widget.
        """

        return HtmlInput(type='hidden', uid=self._uid, name=self.name, value=self.value).render()


class TextInputWidget(InputWidget):
    """Text Input Widget
    """

    def __init__(self, **kwargs: dict):
        """Init.
        """

        super().__init__(**kwargs)
        self.cls = 'form-control'

    def render(self) -> str:
        """Render the widget
        """

        html_input = HtmlInput(
            type='text',
            uid=self._uid,
            name=self._name,
            value=self._value,
            cls=self._cls,
            placeholder=self.placeholder
        )

        return self._group_wrap(html_input.render())


class CheckboxWidget(InputWidget):
    """Single Checkbox Widget.
    """

    def __init__(self, **kwargs: dict):
        """Init.
        """
        super().__init__(**kwargs)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
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
    """Select Widget
    """

    def __init__(self, **kwargs: dict):
        """Init.
        """

        super().__init__(**kwargs)
        self._available_values = kwargs.get('available_values', [])
        self._selected_values = kwargs.get('selected_values', self._value)
        self.cls = 'form-control'

        if not isinstance(self._available_values, list):
            raise TypeError('List expected as available_values argument.')

    def render(self):
        """Render the widget.
        """

        select = HtmlSelect(cls=self.cls)
        for item in self._available_values:
            select.append(HtmlOption(content=item[1], value=item[0]))

        return self._group_wrap(select.render())


class CheckboxesWidget(SelectWidget):
    """Group of Checkboxes Widget.
    """

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val: dict):
        if not isinstance(val, dict):
            raise TypeError('Dictionary expected')

        self._value = val

    def render(self):
        if not isinstance(self._selected_values, list):
            raise TypeError('List expected as selected_values argument.')

        div = Div()
        div.append(HtmlInput(type='hidden', name=self.uid))
        for item in self._available_values:
            checked = True if item[0] in self._selected_values else False
            div.append(
                Div(cls='checkbox').append(
                    Label(item[1]).append(
                        HtmlInput(type='checkbox', name=self.uid, value=item[0], checked=checked)
                    )
                )
            )

        return self._group_wrap(div.render())
