"""PytSite Base Widget.
"""
from collections import OrderedDict as _OrderedDict
from json import dumps as _json_dumps
from typing import Iterable as _Iterable, Tuple as _Tuple, Union as _Union, Dict as _Dict
from abc import ABC as _ABC, abstractmethod as _abstractmethod
from copy import deepcopy as _deepcopy
from pytsite import html as _html, validation as _validation, assetman as _assetman, lang as _lang

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Abstract(_ABC):
    """Abstract Base Widget.
    """
    def __init__(self, uid: str, **kwargs):
        """Init.
        """
        self._uid = uid
        self._wrap_em = _html.Div()
        self._name = kwargs.get('name', uid)
        self._language = kwargs.get('language', _lang.get_current())
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
        self._has_success = kwargs.get('has_success', False)
        self._has_warning = kwargs.get('has_warning', False)
        self._has_error = kwargs.get('has_error', False)
        self._help = kwargs.get('help')
        self._h_size = kwargs.get('h_size')
        self._hidden = kwargs.get('hidden', False)
        self._rules = kwargs.get('rules', [])
        self._form_area = kwargs.get('form_area', 'body')
        self._form_step = kwargs.get('form_step', 1)
        self._assets = kwargs.get('assets', [])
        self._replaces = kwargs.get('replaces', None)
        self._required = kwargs.get('required', False)
        self._enabled = kwargs.get('enabled', True)
        self._parent = kwargs.get('parent')

        # Check validation rules
        if not isinstance(self._rules, (list, tuple)):
            self._rules = [self._rules]
        if isinstance(self._rules, tuple):
            self._rules = list(self._rules)
        for rule in self._rules:
            if not isinstance(rule, _validation.rule.Base):
                raise TypeError('Instance of pytsite.validation.rule.Base expected.')

        if self.required:
            self.add_rule(_validation.rule.NonEmpty())

        if 'value' in kwargs:
            # It is important to filter value through the setter-method
            self.set_val(kwargs.get('value'), mode='init')
        else:
            self._value = _deepcopy(self._default)

    @_abstractmethod
    def get_html_em(self, **kwargs) -> _html.Element:
        """Get an HTML element representation of the widget.
        """
        pass

    def render(self, **kwargs) -> str:
        """Render the widget into a string.
        """
        # Wrapper div
        self._wrap_em.set_attr('data_cid', self.__module__ + '.' + self.__class__.__name__)
        self._wrap_em.set_attr('data_uid', self._uid)
        self._wrap_em.set_attr('data_weight', self._weight)
        self._wrap_em.set_attr('data_form_area', self._form_area)
        self._wrap_em.set_attr('data_form_step', self._form_step)
        self._wrap_em.set_attr('data_hidden', self._hidden)
        self._wrap_em.set_attr('data_enabled', self._enabled)
        self._wrap_em.set_attr('data_parent_uid', self._parent.uid if self._parent else None)

        # Assets
        if self._assets:
            assets = []
            for asset in self._assets:
                if isinstance(asset, (list, tuple)):
                    assets.append((asset[0], asset[1]))
                else:
                    assets.append((asset, _assetman.detect_collection(asset)))

            self._wrap_em.set_attr('data_assets', _json_dumps(assets))

        # Replaces
        if self._replaces:
            self._wrap_em.set_attr('data_replaces', self._replaces)

        # Get widget's HTML element
        html_em = self.get_html_em(**kwargs)

        # Wrapper CSS
        wrap_css = 'pytsite-widget widget-uid-{} {}'.format(self._uid, self._css)
        if self._hidden:
            wrap_css += ' hidden'
        if isinstance(html_em, _html.TagLessElement) and not html_em.content:
            wrap_css += ' empty'
        self._wrap_em.set_attr('cls', wrap_css)

        # Data attributes
        if isinstance(self._data, dict):
            for k, v in self._data.items():
                self._wrap_em.set_attr('data_' + k, v)

        # Wrap widget's HTML
        self._wrap_em.append(html_em)

        return self._wrap_em.render()

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
        if value is not None:
            self._value = value
        else:
            self._value = _deepcopy(self._default)

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
    def language(self) -> str:
        return self._language

    @language.setter
    def language(self, value: str):
        self._language = value

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

    @title.setter
    def title(self, value: str) -> str:
        """Set title of the widget.
        """
        self._title = value

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
    def has_success(self):
        """Get has_success property of the widget.
        """
        return self._has_success

    @has_success.setter
    def has_success(self, value: str):
        """Set has_success property of the widget.
        """
        self._has_success = value
    
    @property
    def has_warning(self):
        """Get has_warning property of the widget.
        """
        return self._has_warning

    @has_warning.setter
    def has_warning(self, value: str):
        """Set has_warning property of the widget.
        """
        self._has_warning = value

    @property
    def has_error(self):
        """Get has_error property of the widget.
        """
        return self._has_error

    @has_error.setter
    def has_error(self, value: str):
        """Set has_error property of the widget.
        """
        self._has_error = value

    @property
    def help(self):
        """Get help string of the widget.
        """
        return self._help

    @help.setter
    def help(self, value: str):
        """Set help string of the widget.
        """
        self._help = value

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
    def replaces(self, value: str):
        self._replaces = value

    @property
    def required(self) -> bool:
        return self._required

    @required.setter
    def required(self, value: bool):
        if value:
            self.add_rule(_validation.rule.NonEmpty())
        else:
            # Clear all added NonEmpty rules
            self.clr_rules().add_rules([r for r in self.get_rules() if not isinstance(r, _validation.rule.NonEmpty)])

        self._required = value

    @property
    def parent(self):
        """
        :rtype: pytsite.widget.Container
        """
        return self._parent

    @parent.setter
    def parent(self, value):
        """
        :type value: pytsite.widget.Container
        """
        self._parent = value

    @property
    def enabled(self) -> bool:
        return self._enabled

    @enabled.setter
    def enabled(self, value: bool):
        self._enabled = value

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

        :type content: pytsite.widget._base.Abstract | pytsite.html.Element | str
        """
        if isinstance(content, str):
            content = _html.TagLessElement(content)
        elif isinstance(content, Abstract):
            content = content.get_html_em()

        if self._h_size:
            content = content.wrap(_html.Div(cls='h-sizer ' + self._h_size))
            content = content.wrap(_html.Div(cls='row'))

        wrap_css = 'form-group'
        if self._has_success:
            wrap_css += ' has-success'
        if self._has_warning:
            wrap_css += ' has-warning'
        if self._has_error:
            wrap_css += ' has-error'
        wrap = _html.Div(cls=wrap_css)

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


class Container(Abstract):
    """Container Widget.
    """

    def __init__(self, uid: str, **kwargs):
        super().__init__(uid, **kwargs)

        self._child_sep = kwargs.get('child_sep', '')
        self._children = {}
        self._css += ' widget-container'
        self._data['container'] = True

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
        for w in self.get_widgets().values():
            w.form_step = value

    def get_widgets(self) -> _Dict[str, Abstract]:
        """Get children widgets.
        """
        return _OrderedDict([(w.uid, w) for w in sorted(self._children.values(), key=lambda x: x.weight)])

    def has_widget(self, uid: str) -> bool:
        return uid in self._children

    def add_widget(self, widget: Abstract):
        """Append a child widget.
        """
        if self.has_widget(widget.uid):
            raise RuntimeError("Container '{}' already contains widget '{}'.".format(self.uid, widget.uid))

        widget.form_step = self.form_step
        widget.form_area = self.form_area
        widget.parent = self
        self._children[widget.uid] = widget

        return self

    def get_widget(self, uid: str) -> Abstract:
        """Get child widget by uid.
        """
        if not self.has_widget(uid):
            raise RuntimeError("Container '{}' doesn't contain widget '{}'.".format(self.uid, uid))

        return self._children[uid]

    def remove_widget(self, uid: str):
        """Remove child widget.
        """
        if not self.has_widget(uid):
            raise RuntimeError("Container '{}' doesn't contain widget '{}'.".format(self.uid, uid))

        del self._children[uid]

        return self

    def get_html_em(self, **kwargs) -> _html.Element:
        cont = _html.TagLessElement(child_sep=self._child_sep)

        if not kwargs.get('skip_children'):
            for w in self.get_widgets().values():
                cont.append(_html.TagLessElement(w.render()))

        return cont
