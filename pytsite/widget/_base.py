"""Abstract Widget.
"""
from abc import ABC as _ABC, abstractmethod as _abstractmethod
from pytsite import util as _util, html as _html

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Base(_ABC):
    """Abstract widget.
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

        self._entity = uid
        self._name = name
        self._weight = kwargs.get('weight', 0)
        self._value = None
        self._label = kwargs.get('label')
        self._title = kwargs.get('title')
        self._placeholder = kwargs.get('placeholder')
        self._css = kwargs.get('css', '')
        self._data = kwargs.get('data', {})
        self._help = kwargs.get('help')
        self._children_sep = '&nbsp;'
        self._children = []
        self._h_size = kwargs.get('h_size')
        self._hidden = kwargs.get('hidden', False)

        # It is important to filter value through the setter-method
        self.set_value(kwargs.get('value'))

    def add_child(self, widget):
        """Add a child widget.
        """
        self._children.append(widget)
        return self

    @_abstractmethod
    def render(self) -> _html.Element:
        """Render the widget.
        """
        pass

    def get_value(self, **kwargs: dict):
        """Get value of the widget.
        """
        return self._value

    @property
    def value(self):
        """Shortcut for get_value().
        """
        return self.get_value()

    def set_value(self, value, **kwargs: dict):
        """Set value of the widget.
        """
        self._value = value

        return self

    @value.setter
    def value(self, val):
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
    def children(self) -> list:
        """Get children widgets.
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
        return self._entity

    @uid.setter
    def uid(self, value):
        """Set UID of the widget.
        """
        if self.uid == self.name:
            self.name = value
        self._entity = value

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

    def _group_wrap(self, content, render_label: bool=True) -> _html.Element:
        """Wrap input string into 'form-group' container.

        :type content: pytsite.html.Element | str
        """
        if isinstance(content, str):
            content = _html.TagLessElement(content)

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

        if render_label and self.label:
            group_wrapper.append(_html.Label(self.label, label_for=self.uid))

        group_wrapper.append(content)

        return group_wrapper

    def __str__(self) -> str:
        return str(self.render())
