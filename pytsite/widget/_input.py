"""Input Widgets.
"""
from pytsite import browser as _browser, html as _html, util as _util, tpl as _tpl, validation as _validation, \
    router as _router
from . import _base

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Input(_base.Base):
    """Abstract Input Widget.
    """
    def __init__(self, uid: str, **kwargs):
        """Init.
        """
        super().__init__(uid, **kwargs)
        self._max_length = kwargs.get('max_length')

    @property
    def max_length(self, ) -> int:
        return self._max_length

    @max_length.setter
    def max_length(self, value: int):
        self._max_length = value


class Hidden(Input):
    """Hidden Input Widget
    """
    def __init__(self, uid: str, **kwargs):
        super().__init__(uid, **kwargs)
        self._hidden = True

    def get_html_em(self, **kwargs) -> _html.Input:
        """Render the widget.
        :param **kwargs:
        """
        return _html.Input(
            type='hidden',
            uid=self.uid,
            name=self.name,
            value=self.value,
            required=self.required
        )


class TextArea(_base.Base):
    """Text Area Input Widget.
    """
    def __init__(self, uid: str, **kwargs):
        """Init.
        """
        super().__init__(uid, **kwargs)

        self._rows = kwargs.get('rows', 5)
        self._required = kwargs.get('required', False)
        self._max_length = kwargs.get('max_length')
        self._css = ' '.join((self._css, 'widget-textarea-input'))

    def get_html_em(self, **kwargs) -> str:
        """Render the widget.
        :param **kwargs:
        """
        html_input = _html.TextArea(
            content=self.get_val(),
            uid=self._uid,
            name=self._name,
            cls=' '.join(('form-control', self._css)),
            placeholder=self.placeholder,
            rows=self._rows,
            required=self._required
        )

        if self._max_length:
            html_input.set_attr('maxlength', self._max_length)

        return self._group_wrap(html_input)


class Text(Input):
    """Text Input Widget
    """
    def __init__(self, uid: str, **kwargs):
        """Init.
        """
        super().__init__(uid, **kwargs)

        self._prepend = kwargs.get('prepend')
        self._append = kwargs.get('append')
        self._css = ' '.join((self._css, 'widget-input-text'))
        self._type = 'text'
        self.assets.append('pytsite.widget@js/text.js')

    def get_html_em(self, **kwargs) -> _html.Element:
        """Render the widget
        :param **kwargs:
        """
        inp = _html.Input(
            type=self._type,
            uid=self._uid,
            name=self._name,
            value=self.get_val(),
            cls='form-control',
            placeholder=self.placeholder,
            required=self._required
        )

        if self._max_length:
            inp.set_attr('maxlength', self._max_length)

        if self._prepend or self._append:
            group = _html.Div(cls='input-group')
            if self._prepend:
                group.append(_html.Div(self._prepend, cls='input-group-addon'))
            group.append(inp)
            if self._append:
                group.append(_html.Div(self._append, cls='input-group-addon'))
            inp = group

        return self._group_wrap(inp)


class Password(Text):
    def __init__(self, uid: str, **kwargs):
        super().__init__(uid, **kwargs)

        self._type = 'password'


class TypeaheadText(Text):
    def __init__(self, uid: str, **kwargs):
        """Init.
        """
        super().__init__(uid, **kwargs)

        ajax_ep = kwargs.get('ajax_ep')
        if not ajax_ep:
            raise ValueError('AJAX endpoint is not specified.')

        self.assets.extend(_browser.get_assets('typeahead'))
        self.assets.append('pytsite.widget@js/typeahead-text.js')

        self._css = ' '.join((self._css, 'widget-input-typeahead-text'))

        source_url_q = kwargs.get('ajax_ep_args', {})
        source_url_q.update({self.uid: '__QUERY'})
        source_url = _router.ep_url('pytsite.ajax.ep.request', {'ep': ajax_ep})
        source_url = _router.url(source_url, query=source_url_q)

        self._data['source_url'] = source_url


class Email(Text):
    """Email Input Widget.
    """
    def __init__(self, uid: str, **kwargs):
        """Init.
        """
        super().__init__(uid, **kwargs)
        self._type = 'email'
        self.add_rule(_validation.rule.Email())
        self.assets.append('pytsite.widget@js/email.js')


class Number(Text):
    def __init__(self, uid: str, **kwargs):
        """Init.
        """
        super().__init__(uid, **kwargs)

        self._type = 'tel'
        self._allow_minus = kwargs.get('allow_minus', False)
        self._min = kwargs.get('min')
        self._max = kwargs.get('max')
        self._css = ' '.join((self._css, 'widget-input-number'))

        if self._allow_minus:
            self._data['allow_minus'] = 'true'

        # Validation rules
        if self._min is not None:
            self.add_rule(_validation.rule.GreaterOrEqual(than=self._min))
        if self._max is not None:
            self.add_rule(_validation.rule.LessOrEqual(than=self._max))

        self._assets.extend(_browser.get_assets('inputmask'))


class Integer(Number):
    """Integer Input Widget
    """
    def __init__(self, uid: str, **kwargs):
        """Init.
        """
        if 'default' not in kwargs:
            kwargs['default'] = 0

        super().__init__(uid, **kwargs)

        self._css = ' '.join((self._css, 'widget-input-integer'))
        self.add_rule(_validation.rule.Integer())
        self._assets.append('pytsite.widget@js/integer.js')

    def set_val(self, value, **kwargs):
        """Set value of the widget.
        """
        if isinstance(value, str):
            value = value.strip()
            if not value:
                value = self._default

        return super().set_val(int(value), **kwargs)


class Decimal(Number):
    """Decimal Input Widget
    """
    def __init__(self, uid: str, **kwargs):
        """Init.
        """
        if 'default' not in kwargs:
            kwargs['default'] = 0

        super().__init__(uid, **kwargs)

        self._css = ' '.join((self._css, 'widget-input-decimal'))
        self.add_rule(_validation.rule.Decimal())
        self._assets.append('pytsite.widget@js/decimal.js')

    def set_val(self, value, **kwargs):
        """Set value of the widget.
        """
        if isinstance(value, str):
            value = value.strip()
            if not value:
                value = self._default

        return super().set_val(float(value), **kwargs)


class StringList(_base.Base):
    """List of strings widget.
    """
    def __init__(self, uid: str, **kwargs):
        """Init.
        """
        super().__init__(uid, **kwargs)
        self._add_btn_label = kwargs.get('add_btn_label', '')
        self._add_btn_icon = kwargs.get('add_btn_icon', 'fa fa-fw fa-plus')
        self._max_values = kwargs.get('max_values', 10)

        self._css = ' '.join((self._css, 'widget-string-list'))
        self._data['max_values'] = self._max_values

        self._assets.extend([
            'pytsite.widget@css/string-list.css',
            'pytsite.widget@js/string-list.js',
        ])

    @property
    def add_btn_label(self) -> str:
        return self._add_btn_label

    @property
    def add_btn_icon(self) -> str:
        return self._add_btn_icon

    def set_val(self, value, **kwargs):
        """Set value of the widget.
        """
        if not value:
            value = []

        if type(value) not in (list, tuple):
            raise ValueError('List or tuple expected.')

        return super().set_val(_util.cleanup_list(value), **kwargs)

    def get_html_em(self, **kwargs) -> _html.Element:
        """Render the widget.
        :param **kwargs:
        """
        return self._group_wrap(_html.Div(_tpl.render('pytsite.widget@string_list', {'widget': self})))


class ListList(StringList):
    """List of lists widget.
    """
    def __init__(self, uid: str, **kwargs):
        super().__init__(uid, **kwargs)

        self._col_titles = kwargs.get('col_titles', ())
        self._col_format = kwargs.get('col_format', ())

        if not self._col_titles or not self._col_format:
            raise ValueError("'col_titles' and 'col_format' cannot be empty.")
        if len(self._col_titles) != len(self._col_format):
            raise ValueError("'col_titles' and 'col_format' must have same length.")

        self._css = self._css.replace('widget-string-list', 'widget-list-list')

        self.assets.extend([
            'pytsite.widget@css/list-list.css',
            'pytsite.widget@js/list-list.js',
        ])

    @property
    def col_titles(self) -> tuple:
        return self._col_titles

    @property
    def col_format(self) -> tuple:
        return self._col_format

    def set_val(self, value, **kwargs):
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

        return super().set_val(value, **kwargs)

    def _set_value_from_string_list(self, value: list, **kwargs):
        new_value = []
        step = len(self.col_format)
        for i in range(0, len(value), step):
            value_to_append = value[i:i+step]
            if _util.cleanup_list(value_to_append):
                new_value.append(value_to_append)

        return super().set_val(new_value, **kwargs)

    def get_html_em(self, **kwargs) -> _html.Element:
        """Render the widget.
        :param **kwargs:
        """
        return self._group_wrap(_html.Div(_tpl.render('pytsite.widget@list_list', {'widget': self})))


class Tokens(Input):
    """Tokens Text Input Widget.
    """
    def __init__(self, uid: str, **kwargs):
        """Init.
        """
        super().__init__(uid, **kwargs)

        self._css = ' '.join((self._css, 'widget-token-input'))

        self.assets.extend(_browser.get_assets('tokenfield'))
        self.assets.extend([
            'pytsite.widget@css/tokens.css',
            'pytsite.widget@js/tokens.js',
        ])

        self._local_source = kwargs.get('local_source')
        self._remote_source = kwargs.get('remote_source')
        self._data = {
            'local_source': self._local_source,
            'remote_source': self._remote_source,
        }

    def set_val(self, value, **kwargs):
        """Set value of the widget.
        """
        if isinstance(value, str):
            value = value.split(',')

        return super().set_val(value)

    def get_html_em(self, **kwargs) -> str:
        """Render the widget.
        :param **kwargs:
        """
        html_input = _html.Input(
            type='text',
            uid=self._uid,
            name=self._name,
            value=','.join(self.get_val()) if self.get_val() else '',
            cls=' '.join(('form-control', self._css)),
        )

        return self._group_wrap(html_input)
