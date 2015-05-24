"""Abstract Widget
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


from abc import ABC, abstractmethod
from pytsite.core.util import random_str, dict_sort
from pytsite.core.html import Div, Label


class AbstractWidget(ABC):
    """Abstract widget.
    """

    def __init__(self, **kwargs: dict):
        """Init.
        """

        uid = kwargs.get('uid')
        name = kwargs.get('name')
        if not uid:
            uid = 'uid_' + random_str()
        if not name:
            name = uid

        self._uid = uid
        self._name = name
        self._value = kwargs.get('value', '')
        self._label = kwargs.get('label')
        self._title = kwargs.get('title')
        self._placeholder = kwargs.get('placeholder')
        self._cls = kwargs.get('cls', '')
        self._help = kwargs.get('help')
        self._children_sep = '&nbsp;'
        self._children = {}

    def add_child(self, widget, weight: int=0):
        """Add a child widget.
        """

        self._children[widget.name] = {'widget': widget, 'weight': weight}

        return self

    @property
    def children(self):
        """Get children widgets.
        """

        r = []
        for k, v in dict_sort(self._children):
            r.append(v['widget'])

        return r

    @abstractmethod
    def render(self) -> str:
        """Render the widget.
        """

        raise NotImplementedError()

    @property
    def uid(self) -> str:
        """Get UID of the widget.
        """

        return self._uid

    @property
    def name(self) -> str:
        """Get name of the widget.
        """

        return self._name

    @property
    def value(self):
        """Get value of the widget.
        """

        return self._value

    @value.setter
    def value(self, val):
        """Set value of the widget.
        """

        self._value = val

    @property
    def label(self) -> str:
        """Get label of the widget.
        """

        return self._label

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
    def cls(self):
        """Get CSS classes of the widget.
        """
        return self._cls

    @cls.setter
    def cls(self, value: str):
        """Set CSS classes of the widget.
        """
        self._cls = value

    @property
    def help(self):
        """Get help string of the widget.
        """
        return self._help

    @help.setter
    def help(self, help_str: str):
        """Set help string of the widget.
        """

        self._help = help_str

    def _group_wrap(self, str_to_wrap: str, add_cls: str=None, add_data: dict=None) -> str:
        """Wrap input string into 'form-group' container.
        """

        cls = 'form-group widget-wrapper widget-uid-{}'.format(self.uid)
        if add_cls:
            cls += ' ' + add_cls

        wrapper = Div(str_to_wrap, cls=cls, data_widget_uid=self.uid)

        if add_data:
            for k, v in add_data.items():
                wrapper.set_attr('data_' + k, v)

        if self.label:
            wrapper.append(Label(self.label, label_for=self.uid))

        return wrapper.render()
