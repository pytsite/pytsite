__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from abc import ABC, abstractmethod


class AbstractWidget(ABC):
    def __init__(self, uid: str, name: str=None, value: str=None, label: str=None, placeholder: str=None,
                 classes: list=None, help_msg: str=None):
        """Init.
        """
        self._uid = uid
        self._name = name if name else uid
        self._value = value
        self._label = label
        self._placeholder = placeholder
        self._classes = classes if classes else []
        self._help = help_msg

        self._children = []

    def add_child(self, widget, weight: int=0):
        """Add a child widget.
        """
        self._children.append((widget, weight))
        return self

    @property
    def children(self):
        """Get children widgets.
        """
        return self._children

    @abstractmethod
    def render(self)->str:
        """Render the widget.
        """
        pass

    @property
    def uid(self):
        return self._uid

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, val):
        self._value = val

    @property
    def label(self):
        return self._label

    @label.setter
    def label(self, label: str):
        self._label = label

    @property
    def placeholder(self):
        return self._placeholder

    @placeholder.setter
    def placeholder(self, placeholder):
        self._placeholder = placeholder

    @property
    def classes(self):
        return self._classes

    @classes.setter
    def classes(self, classes: tuple):
        if not isinstance(classes, tuple):
            raise TypeError('Tuple expected')
        self._classes = classes

    @property
    def help(self):
        return self._help

    @help.setter
    def help(self, help_str: str):
        self._help = help_str

    def _group_wrap(self, str_to_wrap: str, classes: tuple=())->str:
        """Wrap input string into 'form-group' container.
        """
        classes_str = 'form-group'
        for cls in classes:
            classes_str = ' ' + cls

        label_str = '<label for="{0}">{1}</label>'.format(self._uid, self._label) if self._label else ''

        return '<div class="{0}">{1}{2}</div>'.format(classes_str, label_str, str_to_wrap)


class Input(AbstractWidget):
    @abstractmethod
    def render(self)->str:
        """Render the widget.
        """
        pass


class HiddenInput(Input):
    def render(self)->str:
        """Render the widget.
        """
        return '<input type="hidden" id="{0}" name="{1}">'.format(self._uid, self._name)


class TextInput(Input):
    def render(self)->str:
        """Render the widget.
        """
        placeholder = 'placeholder="{0}"'.format(self._placeholder) if self._placeholder else ''
        r = '<input type="text" id="{0}" name="{1}" {2}>'.format(self._uid, self._name, placeholder)
        return self._group_wrap(r)
