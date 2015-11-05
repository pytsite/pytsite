"""Abstract Base Widget.
"""
from abc import ABC as _ABC, abstractmethod as _abstractmethod
from pytsite import util as _util, html as _html, validation as _validation

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Base(_ABC):
    """Abstract Base Widget.
    """
    def __init__(self, **kwargs: dict):
        """Init.
        """
        uid = kwargs.get('uid')
        if not uid:
            uid = 'uid_' + _util.random_str()

        name = kwargs.get('name')
        if not name:
            name = uid

        self._uid = uid
        self._name = name
        self._weight = kwargs.get('weight', 0)
        self._value = None
        self._label = kwargs.get('label')
        self._title = kwargs.get('title')
        self._label_hidden = kwargs.get('label_hidden', False)
        self._label_disabled = kwargs.get('label_disabled', False)
        self._placeholder = kwargs.get('placeholder')
        self._css = kwargs.get('css', '')
        self._data = kwargs.get('data', {})
        self._help = kwargs.get('help')
        self._child_sep = kwargs.get('child_sep', '&nbsp;')
        self._children = []
        self._h_size = kwargs.get('h_size')
        self._hidden = kwargs.get('hidden', False)
        self._form_area = kwargs.get('form_area', 'body')
        self._validator = _validation.Validator()

        # It is important to filter value through the setter-method
        if 'value' in kwargs:
            self.set_value(kwargs.get('value'))

    def append(self, widget):
        """Append a child widget.

        :type widget: Base
        """
        self._children.append(widget)

        return self

    @_abstractmethod
    def get_html_em(self) -> _html.Element:
        """Get an HTML element representation of the widget.
        """
        pass

    def render(self) -> str:
        """Render the widget into a string.
        """
        return self.get_html_em().render()

    def __str__(self) -> str:
        return self.render()

    def get_value(self, **kwargs):
        """Get value of the widget.
        """
        return self._value

    @property
    def value(self):
        """Shortcut for get_value().
        """
        return self.get_value()

    def set_value(self, value, **kwargs):
        """Set value of the widget.
        """
        self._value = value
        if self._validator.has_field(self.uid):
            self._validator.set_value(self.uid, value)

        return self

    @value.setter
    def value(self, val):
        """Shortcut for set_value().
        """
        self.set_value(val)

    def hide(self):
        """Hides the widget.
        """
        self._hidden = True

        return self

    def show(self):
        """Shows the widget.
        """
        self._hidden = True

        return self

    @property
    def children(self):
        """Get children widgets.

        :rtype: list[Base]
        """
        sort = []
        for w in self._children:
            sort.append({'widget': w, 'weight': w.weight})

        r = []
        for w in _util.weight_sort(sort):
            r.append(w['widget'])

        return r

    def get_child(self, uid: str):
        """Get child widget by uid.
        :rtype: pytsite.widget._base.Base
        """
        for w in self._children:
            if w.uid == uid:
                return w

    def remove_child(self, uid: str):
        """Remove child widget.
        :rtype: pytsite.widget._base.Base
        """
        self._children = [w for w in self._children if w.uid != uid]

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

    def validate(self):
        """Validate the widget.
        """
        self._validator.validate()

    def add_rule(self, rule: _validation.rule.Base):
        """Add single validation rule.
        """
        self._validator.add_rule(self._uid, rule)

        return self

    def add_rules(self, rules: list):
        """Add multiple validation rules.
        """
        for rule in rules:
            self.add_rules(rule)

        return self

    def get_rules(self) -> list:
        """Get validation rules.
        """
        return self._validator.get_rules(self.uid)

    def remove_rules(self):
        """Add validation rules.
        """
        self._validator.remove_rules(self.uid)

        return self

    def _group_wrap(self, content) -> _html.Element:
        """Wrap input string into 'form-group' container.

        :type content: pytsite.widget._base.Base | pytsite.html.Element | str
        """
        if isinstance(content, str):
            content = _html.TagLessElement(content)
        elif isinstance(content, Base):
            content = content.get_html_em()

        if self._h_size:
            content = content.wrap(_html.Div(cls=self._h_size))
            content = content.wrap(_html.Div(cls='row'))

        css = 'form-group widget widget-uid-{} {}'.format(self.uid, self._css)

        if self._hidden:
            css += ' hidden'

        group_wrapper = _html.Div(cls=css, data_widget_uid=self.uid, data_widget_weight=self.weight)

        if self._hidden:
            group_wrapper.set_attr('hidden', True)

        if isinstance(self._data, dict):
            for k, v in self._data.items():
                group_wrapper.set_attr('data_' + k, v)

        if not self._label and self._placeholder:
            self._label = self.placeholder

        if self.label and not self._label_disabled:
            label = _html.Label(self.label, label_for=self.uid)
            if self._label_hidden:
                label.set_attr('class', 'sr-only')
            group_wrapper.append(label)

        group_wrapper.append(content)

        if self._help:
            group_wrapper.append(_html.Span(self._help, cls='help-block'))

        return group_wrapper
