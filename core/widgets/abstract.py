"""Abstract Widget
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


from abc import ABC, abstractmethod
from pytsite.core.util import random_str, weight_sort
from pytsite.core.html import Div, Label


class AbstractWidget(ABC):
    """Abstract widget.
    """

    def __init__(self, **kwargs: dict):
        """Init.
        """
        uid = kwargs.get('uid')
        if not uid:
            uid = 'uid_' + random_str()

        name = kwargs.get('name')
        if not name:
            name = uid

        self._uid = uid
        self._name = name
        self._value = None
        self._label = kwargs.get('label')
        self._title = kwargs.get('title')
        self._placeholder = kwargs.get('placeholder')
        self._cls = kwargs.get('cls', '')
        self._group_cls = kwargs.get('group_cls', '')
        self._help = kwargs.get('help')
        self._children_sep = '&nbsp;'
        self._children = []
        self._h_size = kwargs.get('h_size')

        # It is important to filter value through the setter-method
        self.set_value(kwargs.get('value'))

    def add_child(self, widget, weight: int=0):
        """Add a child widget.
        """
        self._children.append({'widget': widget, 'weight': weight})
        return self

    @abstractmethod
    def render(self) -> str:
        """Render the widget.
        """
        pass

    def get_value(self, **kwargs: dict):
        """Get value of the widget.
        """
        return self._value

    def set_value(self, value, **kwargs: dict):
        """Set value of the widget.
        """
        self._value = value

        return self

    @property
    def children(self):
        """Get children widgets.
        """
        r = []
        for v in weight_sort(self._children):
            r.append(v['widget'])

        return r

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
    def cls(self) -> str:
        """Get CSS classes of the widget.
        """
        return self._cls

    @property
    def help(self):
        """Get help string of the widget.
        """
        return self._help

    def _group_wrap(self, content, add_data: dict=None, render_label: bool=True) -> str:
        """Wrap input string into 'form-group' container.
        """
        content = str(content)

        if self._h_size:
            content = Div(content, cls=self._h_size).wrap(Div(cls='row')).render()

        cls = 'form-group widget-wrapper widget-uid-{}'.format(self.uid)
        cls = ' '.join((cls, self._group_cls))
        group_wrapper = Div(content, cls=cls, data_widget_uid=self.uid)

        if add_data:
            for k, v in add_data.items():
                group_wrapper.set_attr('data_' + k, v)

        if render_label and self.label:
            group_wrapper.append(Label(self.label, label_for=self.uid))

        return group_wrapper.render()
