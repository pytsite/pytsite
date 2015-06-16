"""Input Widgets.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from abc import abstractmethod

from pytsite.core import assetman, client
from pytsite.core.html import Input as HtmlInput, TextArea as HtmlTextArea
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


class TextAreaInputWidget(AbstractWidget):
    """Text Area Input Widget.
    """
    def __init__(self, **kwargs):
        """Init.
        """
        super().__init__(**kwargs)
        self._group_cls = ' '.join((self._group_cls, 'widget-textarea-input'))

    def render(self) -> str:
        """Render the widget.
        """
        html_input = HtmlTextArea(
            content=self.get_value(),
            uid=self._uid,
            name=self._name,
            cls=' '.join(('form-control', self._cls)),
            placeholder=self.placeholder
        )

        return self._group_wrap(html_input.render())

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


class TypeaheadTextInputWidget(TextInputWidget):
    def __init__(self, source_url: str, **kwargs):
        """Init.
        """
        super().__init__(**kwargs)
        self._group_cls = ' '.join((self._group_cls, 'widget-typeahead-text-input'))
        client.include('typeahead')
        assetman.add('pytsite.core.widgets@js/typeahead.js')
        self._group_data['source_url'] = source_url


class IntegerInputWidget(TextInputWidget):
    """Integer Input Widget.
    """

    def __init__(self, **kwargs):
        """Init.
        """
        super().__init__(**kwargs)
        assetman.add('pytsite.core.widgets@js/jquery.inputmask.bundle.min.js')
        assetman.add('pytsite.core.widgets@js/integer.js')
        self._group_cls = self._group_cls.replace('widget-text-input', 'widget-integer-input')

    def set_value(self, value, **kwargs: dict):
        """Set value of the widget.
        """
        if not value:
            value = 0
        return super().set_value(int(value), **kwargs)
