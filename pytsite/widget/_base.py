"""PytSite Base Widget.
"""
from json import dumps as _json_dumps
from typing import Iterable as _Iterable, Tuple as _Tuple, Union as _Union
from abc import ABC as _ABC, abstractmethod as _abstractmethod
from copy import deepcopy as _deepcopy
from pytsite import html as _html, validation as _validation, assetman as _assetman

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Base(_ABC):
    """Abstract Base Widget.
    """
    def __init__(self, uid: str, **kwargs):
        """Init.
        """
        self._uid = uid
        self._name = kwargs.get('name', uid)
        self._weight = kwargs.get('weight', 0)
        self._default = kwargs.get('default')
        self._value = None  # Wil be set later
        self._label = kwargs.get('label')
        self._title = kwargs.get('title')
        self._label_hidden = kwargs.get('label_hidden', False)
        self._label_disabled = kwargs.get('label_disabled', False)
        self._placeholder = kwargs.get('placeholder')
        self._css = kwargs.get('css', '')
        self._data = kwargs.get('data', {})
        self._help = kwargs.get('help')
        self._h_size = kwargs.get('h_size')
        self._hidden = kwargs.get('hidden', False)
        self._rules = kwargs.get('rules', [])
        self._form_area = kwargs.get('form_area', 'body')
        self._form_step = kwargs.get('form_step', 1)
        self._assets = kwargs.get('assets', [])
        self._replaces = kwargs.get('replaces', None)

        # Check validation rules
        if type(self._rules) not in (list, tuple):
            self._rules = [self._rules]
        if isinstance(self._rules, tuple):
            self._rules = list(self._rules)
        for rule in self._rules:
            if not isinstance(rule, _validation.rule.Base):
                raise TypeError('instance of pytsite.validation.rule.Base expected.')

        if 'value' in kwargs:
            # It is important to filter value through the setter-method
            self.set_val(kwargs.get('value'), mode='init')
        else:
            self._value = _deepcopy(self._default)

    @_abstractmethod
    def get_html_em(self) -> _html.Element:
        """Get an HTML element representation of the widget.
        """
        pass

    def render(self) -> str:
        """Render the widget into a string.
        """
        wrap_css = 'pytsite-widget widget-uid-{} {}'.format(self._uid, self._css)
        if self._hidden:
            wrap_css += ' hidden'

        # Wrapper div
        wrap = _html.Div(
            cls=wrap_css,
            data_cid=self.__module__ + '.' + self.__class__.__name__,
            data_uid=self._uid,
            data_weight=self._weight,
            data_form_area=self._form_area,
            data_form_step=self._form_step,
            data_hidden=self._hidden,
        )

        # Assets
        if self._assets:
            assets = []
            for asset in self._assets:
                if isinstance(asset, (list, tuple)):
                    assets.append((asset[0], asset[1]))
                else:
                    assets.append((asset, _assetman.detect_collection(asset)))

            wrap.set_attr('data_assets', _json_dumps(assets))

        # Replaces
        if self._replaces:
            wrap.set_attr('data_replaces', self._replaces)

        # Get widget's HTML element
        html_em = self.get_html_em()

        # Data attributes
        if isinstance(self._data, dict):
            for k, v in self._data.items():
                wrap.set_attr('data_' + k, v)

        # Wrap widget's HTML
        wrap.append(html_em)

        return wrap.render()

    def __str__(self) -> str:
        return self.render()

    def get_val(self, **kwargs):
        """Get value of the widget.
        """
        return self._value

    @property
    def default(self):
        return self._default

    @property
    def value(self):
        """Shortcut for get_value().
        """
        return self.get_val()

    def set_val(self, value, **kwargs):
        """Set value of the widget.
        """
        self._value = value

        return self

    @value.setter
    def value(self, val):
        """Shortcut for set_value().
        """
        self.set_val(val)

    def clr_val(self):
        self._value = _deepcopy(self._default)

    def hide(self):
        """Hides the widget.
        """
        self._hidden = True

        return self

    def show(self):
        """Shows the widget.
        """
        self._hidden = False

        return self

    @property
    def uid(self) -> str:
        """Get UID of the widget.
        """
        return self._uid

    @uid.setter
    def uid(self, value):
        """Set UID of the widget.
        """
        if self.uid == self.name:
            self.name = value
        self._uid = value

    @property
    def name(self) -> str:
        """Get name of the widget.
        """
        return self._name

    @name.setter
    def name(self, value: str):
        self._name = value

    @property
    def weight(self) -> int:
        return self._weight

    @weight.setter
    def weight(self, value: int):
        self._weight = int(value)

    @property
    def label(self) -> str:
        """Get label of the widget.
        """
        return self._label

    @label.setter
    def label(self, value: str):
        """Set label of the widget.
        """
        self._label = value

    @property
    def title(self) -> str:
        """Get title of the widget.
        """
        return self._title

    @property
    def placeholder(self):
        """Get placeholder of the widget.
        """
        return self._placeholder

    @property
    def css(self) -> str:
        """Get CSS classes of the widget.
        """
        return self._css

    @css.setter
    def css(self, value):
        self._css = value

    @property
    def help(self):
        """Get help string of the widget.
        """
        return self._help

    @property
    def form_area(self) -> str:
        return self._form_area

    @form_area.setter
    def form_area(self, area: str):
        self._form_area = area

    @property
    def form_step(self) -> _Union[str, tuple]:
        """Get current form step.
        """
        return self._form_step

    @form_step.setter
    def form_step(self, value: int):
        """Set current form step.
        """
        self._form_step = value

    @property
    def h_size(self) -> str:
        return self._h_size

    @h_size.setter
    def h_size(self, value: str):
        self._h_size = value

    @property
    def assets(self) -> list:
        """Get CSS files list.
        """
        return self._assets

    @property
    def replaces(self) -> str:
        return self._replaces

    @replaces.setter
    def replaces(self, value: str) -> str:
        self._replaces = value

    def add_rule(self, rule: _validation.rule.Base):
        """Add single validation rule.
        """
        self._rules.append(rule)

        return self

    def add_rules(self, rules: _Iterable):
        """Add multiple validation rules.
        """
        for rule in rules:
            self.add_rule(rule)

        return self

    def get_rules(self) -> _Tuple[_validation.rule.Base]:
        """Get validation rules.
        """
        return tuple(self._rules)

    def clr_rules(self):
        """Clear validation rules.
        """
        self._rules = []

        return self

    def validate(self):
        """Validate the widget's rules.
        """
        for rule in self.get_rules():
            rule.validate(self.get_val(mode='validation'))

    def _group_wrap(self, content) -> _html.Element:
        """Wraps a widget, an HTML element or a string into 'form-group' container.

        :type content: pytsite.widget._base.Base | pytsite.html.Element | str
        """
        if isinstance(content, str):
            content = _html.TagLessElement(content)
        elif isinstance(content, Base):
            content = content.get_html_em()

        if self._h_size:
            content = content.wrap(_html.Div(cls=self._h_size))
            content = content.wrap(_html.Div(cls='row'))

        wrap = _html.Div(cls='form-group')

        # Place placeholder instead of label
        if not self._label and self._placeholder:
            self._label = self.placeholder

        # Append label element
        if self.label and not self._label_disabled:
            label = _html.Label(self.label, label_for=self.uid)
            if self._label_hidden:
                label.set_attr('cls', 'sr-only')
            wrap.append(label)

        # Append widget's content
        wrap.append(content)

        # Append help block
        if self._help:
            wrap.append(_html.Span(self._help, cls='help-block'))

        # Append messages placeholder
        wrap.append(_html.Div(cls='widget-messages'))

        return wrap
