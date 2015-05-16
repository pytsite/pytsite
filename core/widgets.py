"""Widgets.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


from abc import ABC, abstractmethod


class AbstractWidget(ABC):
    """Abstract widget.
    """
    def __init__(self, uid: str, **kwargs):
        """Init.
        """
        self._uid = uid
        self._name = kwargs.get('name')
        self._value = kwargs.get('value', '')
        self._label = kwargs.get('label')
        self._placeholder = kwargs.get('placeholders')
        self._classes = kwargs.get('classes', {})
        self._help = kwargs.get('help')

        if not self._name:
            self._name = uid

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
        return '<input type="hidden" id="{0}" name="{1}" value="{2}">'.format(self._uid, self._name, self._value)


class TextInput(Input):
    def render(self)->str:
        """Render the widget.
        """
        placeholder = 'placeholder="{0}"'.format(self._placeholder) if self._placeholder else ''
        r = '<input type="text" id="{0}" name="{1}" {2} value="{3}">'.format(
            self._uid, self._name, placeholder, self._value)

        return self._group_wrap(r)
