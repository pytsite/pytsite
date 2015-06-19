"""Input Widgets
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from abc import abstractmethod as _abstractmethod
from pytsite.core import assetman as _assetman, client as _client, html as _html
from . import _base


class Input(_base.Widget):
    """Input Widget.
    """
    @_abstractmethod
    def render(self) -> _html.Element:
        pass


class Hidden(Input):
    """Hidden Input Widget
    """
    def render(self) -> str:
        """Render the widget.
        """
        return _html.Input(type='hidden', uid=self._uid, name=self.name, value=self.get_value()).render()


class TextArea(_base.Widget):
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
        html_input = _html.TextArea(
            content=self.get_value(),
            uid=self._uid,
            name=self._name,
            cls=' '.join(('form-control', self._cls)),
            placeholder=self.placeholder
        )

        return self._group_wrap(html_input)


class Text(Input):
    """Text Input Widget
    """
    def __init__(self, prepend: str=None, append: str=None, **kwargs):
        """Init.
        """
        super().__init__(**kwargs)
        self._prepend = prepend
        self._append = append
        self._group_cls = ' '.join((self._group_cls, 'widget-text-input'))
        self._type = 'text'

    def render(self) -> _html.Element:
        """Render the widget
        """
        inp = _html.Input(
            type=self._type,
            uid=self._uid,
            name=self._name,
            value=self.get_value(),
            cls=' '.join(('form-control', self._cls)),
            placeholder=self.placeholder
        )

        if self._prepend or self._append:
            group = _html.Div(cls='input-group')
            if self._prepend:
                group.append(_html.Div(self._prepend, cls='input-group-addon'))
            group.append(inp)
            if self._append:
                group.append(_html.Div(self._append, cls='input-group-addon'))
            inp = group

        return self._group_wrap(inp)


class TypeaheadText(Text):
    def __init__(self, source_url: str, **kwargs):
        """Init.
        """
        super().__init__(**kwargs)
        _client.include('typeahead')
        _assetman.add('pytsite.core.widget@js/typeahead.js')
        self._group_cls = ' '.join((self._group_cls, 'widget-typeahead-text-input'))
        self._group_data['source_url'] = source_url


class Integer(Text):
    """Integer Input Widget
    """
    def __init__(self, **kwargs):
        """Init.
        """
        super().__init__(**kwargs)
        self._type = 'number'
        self._group_cls = self._group_cls.replace('widget-text-input', 'widget-input-integer')

    def set_value(self, value, **kwargs: dict):
        """Set value of the widget.
        """
        if not value:
            value = 0
        return super().set_value(int(value), **kwargs)

    def render(self):
        _client.include('inputmask')
        _assetman.add('pytsite.core.widget@js/integer.js')
        return super().render()

class Float(Text):
    """Float Input Widget
    """
    def __init__(self, **kwargs):
        """Init.
        """
        super().__init__(**kwargs)
        self._type = 'tel'
        self._group_cls = self._group_cls.replace('widget-text-input', 'widget-input-float')

    def set_value(self, value, **kwargs: dict):
        """Set value of the widget.
        """
        if not value:
            value = 0.0
        return super().set_value(float(value), **kwargs)

    def render(self):
        _client.include('inputmask')
        _assetman.add('pytsite.core.widget@js/float.js')
        return super().render()
