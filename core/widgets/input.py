"""Input Widgets.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from abc import abstractmethod
from datetime import datetime
from pytsite.core import assetman
from pytsite.core.html import Input as HtmlInput
from .abstract import AbstractWidget


class InputWidget(AbstractWidget):
    """Input Widget.
    """

    @abstractmethod
    def render(self) -> str:
        pass


class HiddenInputWidget(InputWidget):
    """Hidden Input Widget
    """

    def render(self) -> str:
        """Render the widget.
        """
        return HtmlInput(type='hidden', uid=self._uid, name=self.name, value=self.get_value()).render()


class TextInputWidget(InputWidget):
    """Text Input Widget
    """

    def __init__(self, **kwargs):
        """Init.
        """
        super().__init__(**kwargs)
        self._group_cls = ' '.join((self._group_cls, 'widget-text-input'))

    def render(self) -> str:
        """Render the widget
        """
        html_input = HtmlInput(
            type='text',
            uid=self._uid,
            name=self._name,
            value=self.get_value(),
            cls=' '.join(('form-control', self._cls)),
            placeholder=self.placeholder
        )

        return self._group_wrap(html_input.render())


class IntegerInputWidget(TextInputWidget):
    def __init__(self, **kwargs):
        """Init.
        """
        super().__init__(**kwargs)
        assetman.add('pytsite.core.widgets@js/jquery.inputmask.bundle.min.js')
        assetman.add('pytsite.core.widgets@js/integer.js')
        self._group_cls = self._group_cls.replace('widget-text-input', 'widget-integer-input')


class DateTimeInputWidget(TextInputWidget):
    def __init__(self, **kwargs):
        """Init.
        """
        super().__init__(**kwargs)
        assetman.add('pytsite.core.widgets@css/jquery.datetimepicker.css')
        assetman.add('pytsite.core.widgets@js/jquery.datetimepicker.js')
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
