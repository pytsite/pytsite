"""Input Widget.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite.core.html import Input as HtmlInput, Div, Label
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

        return HtmlInput(type='hidden', id=self.uid, name=self.name, value=self.value).render()


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
            id=self.uid,
            name=self.name,
            value=self.value,
            cls=self.cls,
            placeholder=self.placeholder
        )

        return self._group_wrap(html_input.render())


class SelectWidget(InputWidget):
    """Select Widget
    """

    def __init__(self, **kwargs: dict):
        """Init.
        """

        super().__init__(**kwargs)
        self._available_values = kwargs.get('values', {})
        self.cls = 'form-control'

        if not isinstance(self._available_values, dict):
            raise TypeError('Dictionary expected')


class CheckboxesWidget(SelectWidget):
    """Group of Checkboxes Widget.
    """

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val: dict):
        if not isinstance(self._available_values, dict):
            raise TypeError('Dictionary expected')

        self._value = val

    def render(self):
        checkboxes = Div()
        for k, v in self._available_values.items():
            checkboxes.append(Div(cls='checkbox').append(
                Label(v).append(HtmlInput(type='checkbox', name=self.uid, value=k))
            ))

        return self._group_wrap(checkboxes.render())
