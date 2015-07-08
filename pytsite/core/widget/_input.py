"""Input Widgets.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from abc import abstractmethod as _abstractmethod
from pytsite.core import assetman as _assetman, client as _client, html as _html, tpl as _tpl, util as _util
from . import _base


class Input(_base.Base):
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


class TextArea(_base.Base):
    """Text Area Input Widget.
    """
    def __init__(self, **kwargs):
        """Init.
        """
        super().__init__(**kwargs)
        self._rows = kwargs.get('rows', 5)
        self._group_cls = ' '.join((self._group_cls, 'widget-textarea-input'))

    def render(self) -> str:
        """Render the widget.
        """
        html_input = _html.TextArea(
            content=self.get_value(),
            uid=self._uid,
            name=self._name,
            cls=' '.join(('form-control', self._cls)),
            placeholder=self.placeholder,
            rows=self._rows
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
        self._group_cls = ' '.join((self._group_cls, 'widget-input-text'))
        self._type = 'text'

    def render(self) -> _html.Element:
        """Render the widget
        """
        _assetman.add('core.widget@js/text.js')

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
        _assetman.add('core.widget@js/typeahead.js')
        self._group_cls = ' '.join((self._group_cls, 'widget-typeahead-text-input'))
        self._group_data['source_url'] = source_url


class Integer(Text):
    """Integer Input Widget
    """
    def __init__(self, **kwargs):
        """Init.
        """
        super().__init__(**kwargs)
        self._type = 'tel'
        self._allow_minus = kwargs.get('allow_minus', False)
        self._group_cls = ' '.join((self._group_cls, 'widget-input-integer'))
        self._group_data['allow_minus'] = self._allow_minus

    def set_value(self, value, **kwargs: dict):
        """Set value of the widget.
        """
        if not value:
            value = 0
        return super().set_value(int(value), **kwargs)

    def render(self):
        _client.include('inputmask')
        _assetman.add('core.widget@js/integer.js')
        return super().render()


class Float(Text):
    """Float Input Widget
    """
    def __init__(self, **kwargs):
        """Init.
        """
        super().__init__(**kwargs)
        self._type = 'tel'
        self._allow_minus = kwargs.get('allow_minus', False)
        self._group_cls = ' '.join((self._group_cls, 'widget-input-float'))
        self._group_data['allow_minus'] = self._allow_minus

    def set_value(self, value, **kwargs: dict):
        """Set value of the widget.
        """
        if not value:
            value = 0.0
        return super().set_value(float(value), **kwargs)

    def render(self):
        _client.include('inputmask')
        _assetman.add('core.widget@js/float.js')
        return super().render()


class CKEditor(_base.Base):
    """CKEditor Widget.
    """
    def __init__(self, **kwargs: dict):
        """Init.
        """
        super().__init__(**kwargs)
        self._group_cls = ' '.join((self._group_cls, 'widget-ckeditor'))
        _assetman.add('core.widget@ckeditor/skins/moono/editor.css')
        _assetman.add('core.widget@ckeditor/ckeditor.js')
        _assetman.add('core.widget@ckeditor/adapters/jquery.js')
        _assetman.add('core.widget@js/ckeditor.js')

    def render(self) -> str:
        """Render the widget.
        """
        return self._group_wrap(_html.TextArea(self.get_value(), name=self._uid))


class StringList(_base.Base):
    """List of strings widget.
    """
    def __init__(self, **kwargs: dict):
        """Init.
        """
        super().__init__(**kwargs)
        self._add_btn_label = kwargs.get('add_btn_label', '')
        self._add_btn_icon = kwargs.get('add_btn_icon', 'fa fa-fw fa-plus')
        self._max_values = kwargs.get('max_values', 3)

        self._group_cls = ' '.join((self._group_cls, 'widget-string-list'))
        self._group_data['max_values'] = self._max_values

        _assetman.add('core.widget@js/string-list.js')
        _assetman.add('core.widget@css/string-list.css')

    @property
    def add_btn_label(self) -> str:
        return self._add_btn_label

    @property
    def add_btn_icon(self) -> str:
        return self._add_btn_icon

    def set_value(self, value, **kwargs: dict):
        """Set value of the widget.
        """
        if not isinstance(value, list):
            raise ValueError('List expected.')

        return super().set_value(_util.list_cleanup(value), **kwargs)

    def render(self) -> _html.Element:
        """Render the widget.
        """
        widget_content = _html.Div(_tpl.render('core.widget@string_list', {'widget': self}))
        return self._group_wrap(widget_content)