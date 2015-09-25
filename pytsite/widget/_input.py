"""Input Widgets.
"""
from abc import abstractmethod as _abstractmethod
from pytsite import assetman as _assetman, browser as _client, html as _html, util as _util, tpl as _tpl
from . import _base

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Input(_base.Base):
    """Input Widget.
    """
    def __init__(self, **kwargs):
        """Init.
        """
        super().__init__(**kwargs)
        self._required = kwargs.get('required', False)
        self._max_length = kwargs.get('max_length')

    @property
    def required(self) -> bool:
        return self._required

    @required.setter
    def required(self, value: bool):
        self._required = value

    @_abstractmethod
    def render(self) -> _html.Element:
        pass


class Hidden(Input):
    """Hidden Input Widget
    """
    def render(self) -> str:
        """Render the widget.
        """
        html_input = _html.Input(
            type='hidden',
            uid=self.uid,
            name=self.name,
            value=self.value,
            required=self.required
        )

        return html_input


class TextArea(_base.Base):
    """Text Area Input Widget.
    """
    def __init__(self, **kwargs):
        """Init.
        """
        super().__init__(**kwargs)
        self._rows = kwargs.get('rows', 5)
        self._required = kwargs.get('required', False)
        self._max_length = kwargs.get('max_length')
        self._css = ' '.join((self._css, 'widget-textarea-input'))

    def render(self) -> str:
        """Render the widget.
        """
        html_input = _html.TextArea(
            content=self.get_value(),
            uid=self._entity,
            name=self._name,
            cls=' '.join(('form-control', self._css)),
            placeholder=self.placeholder,
            rows=self._rows,
            required=self._required
        )

        if self._max_length:
            html_input.set_attr('maxlength', int(self._max_length))

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
        self._css = ' '.join((self._css, 'widget-input-text'))
        self._type = 'text'

    def render(self) -> _html.Element:
        """Render the widget
        """
        _assetman.add('pytsite.widget@js/text.js')

        inp = _html.Input(
            type=self._type,
            uid=self._entity,
            name=self._name,
            value=self.get_value(),
            cls='form-control',
            placeholder=self.placeholder,
            required=self._required
        )

        if self._max_length:
            inp.set_attr('maxlength', int(self._max_length))

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
        _assetman.add('pytsite.widget@js/typeahead.js')
        self._css = ' '.join((self._css, 'widget-typeahead-text-input'))
        self._data['source_url'] = source_url


class Integer(Text):
    """Integer Input Widget
    """
    def __init__(self, **kwargs):
        """Init.
        """
        super().__init__(**kwargs)
        self._type = 'tel'
        self._allow_minus = kwargs.get('allow_minus', False)
        self._css = ' '.join((self._css, 'widget-input-integer'))
        self._data['allow_minus'] = self._allow_minus

    def set_value(self, value, **kwargs: dict):
        """Set value of the widget.
        """
        if not value:
            value = 0
        return super().set_value(int(value), **kwargs)

    def render(self):
        _client.include('inputmask')
        _assetman.add('pytsite.widget@js/integer.js')
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
        self._css = ' '.join((self._css, 'widget-input-float'))
        self._data['allow_minus'] = self._allow_minus

    def set_value(self, value, **kwargs: dict):
        """Set value of the widget.
        """
        if not value:
            value = 0.0

        return super().set_value(float(value), **kwargs)

    def render(self):
        _client.include('inputmask')
        _assetman.add('pytsite.widget@js/float.js')
        return super().render()


class StringList(_base.Base):
    """List of strings widget.
    """
    def __init__(self, **kwargs: dict):
        """Init.
        """
        super().__init__(**kwargs)
        self._add_btn_label = kwargs.get('add_btn_label', '')
        self._add_btn_icon = kwargs.get('add_btn_icon', 'fa fa-fw fa-plus')
        self._max_values = kwargs.get('max_values', 10)

        self._css = ' '.join((self._css, 'widget-string-list'))
        self._data['max_values'] = self._max_values

        _assetman.add('pytsite.widget@js/list.js')
        _assetman.add('pytsite.widget@css/list.css')

    @property
    def add_btn_label(self) -> str:
        return self._add_btn_label

    @property
    def add_btn_icon(self) -> str:
        return self._add_btn_icon

    def set_value(self, value, **kwargs: dict):
        """Set value of the widget.
        """
        if value is None:
            value = []

        if not isinstance(value, list):
            raise ValueError('List expected.')

        return super().set_value(_util.list_cleanup(value), **kwargs)

    def render(self) -> _html.Element:
        """Render the widget.
        """
        widget_content = _html.Div(_tpl.render('pytsite.widget@string_list', {'widget': self}))
        return self._group_wrap(widget_content)


class ListList(StringList):
    """List of lists widget.
    """
    def __init__(self, col_titles: tuple, col_format: tuple, **kwargs):
        super().__init__(**kwargs)

        self._col_titles = col_titles
        self._col_format = col_format

        if not col_titles or not col_format:
            raise ValueError("'col_titles' and 'col_format' cannot be empty.")
        if len(col_titles) != len(col_format):
            raise ValueError("'col_titles' and 'col_format' must have same length.")

        self._css = ' '.join((self._css, 'widget-list-list'))

    @property
    def col_titles(self) -> list:
        return self._col_titles

    @property
    def col_format(self) -> list:
        return self._col_format

    def set_value(self, value, **kwargs: dict):
        """Set value of the widget.
        """
        if value is None:
            value = []

        if value:
            if isinstance(value[0], list):
                return self._set_value_from_list_list(value, **kwargs)
            elif isinstance(value[0], str):
                return self._set_value_from_string_list(value, **kwargs)
            else:
                raise ValueError('List of strings ot list of lists of strings expected')

        return self

    def _set_value_from_list_list(self, value: list, **kwargs):
        for sub in value:
            if not isinstance(sub, list):
                raise ValueError('List expected.')
            for item in sub:
                if not isinstance(item, str):
                    raise ValueError('str expected.')

        return super().set_value(value, **kwargs)

    def _set_value_from_string_list(self, value: list, **kwargs):
        new_value = []
        step = len(self.col_format)
        for i in range(0, len(value), step):
            value_to_append = value[i:i+step]
            if _util.list_cleanup(value_to_append):
                new_value.append(value_to_append)

        return super().set_value(new_value, **kwargs)

    def render(self) -> _html.Element:
        """Render the widget.
        """
        widget_content = _html.Div(_tpl.render('pytsite.widget@list_list', {'widget': self}))
        return self._group_wrap(widget_content)


class Tokens(Input):
    """Tokens Text Input Widget.
    """
    def __init__(self, **kwargs):
        """Init.
        """
        super().__init__(**kwargs)
        self._css = ' '.join((self._css, 'widget-token-input'))
        _client.include('tokenfield')
        _assetman.add('pytsite.widget@css/tokens.css')
        _assetman.add('pytsite.widget@js/tokens.js')

        self._local_source = kwargs.get('local_source')
        self._remote_source = kwargs.get('remote_source')
        self._data = {
            'local_source': self._local_source,
            'remote_source': self._remote_source,
        }

    def set_value(self, value, **kwargs: dict):
        """Set value of the widget.
        """
        if isinstance(value, str):
            value = value.split(',')

        return super().set_value(value)

    def render(self) -> str:
        """Render the widget.
        """
        html_input = _html.Input(
            type='text',
            uid=self._entity,
            name=self._name,
            value=','.join(self.get_value()) if self.get_value() else '',
            cls=' '.join(('form-control', self._css)),
        )

        return self._group_wrap(html_input)
