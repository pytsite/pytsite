"""Feed Writer.
"""
from typing import Dict as _Dict, Any as _Any, Tuple as _Tuple, List as _List
from abc import ABC as _ABC, abstractmethod as _abstractmethod
from . import _error

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Serializable:
    def __init__(self):
        """Init.
        """
        self._children = []  # type: _List[Serializable]
        self._children_names = []

    @property
    def name(self) -> str:
        """Gte name of an element.
        """
        raise NotImplementedError()

    @property
    def valid_parents(self) -> _Tuple[str]:
        """Get tuple of valid parents for this element.
        """
        return ()

    @property
    def required_children(self) -> _Tuple[str]:
        """Get tuple of required children for the element.
        """
        return ()

    def append_child(self, child, index: int = None):
        """Append a child to the element.

        :type child: Serializable
        """
        if not isinstance(child, Serializable):
            raise TypeError("Element is not serializable.")

        if child.valid_parents and self.name not in child.valid_parents:
            raise TypeError("Element '{}' cannot be child of '{}'.".format(child.name, self.name))

        if index is not None:
            self._children.insert(index, child)
        else:
            self._children.append(child)

        if child.name not in self._children_names:
            self._children_names.append(child.name)

        return child

    def has_children(self, name: str) -> bool:
        """Check if the item has a child.
        """
        return name in self._children_names

    def get_children(self, name: str = None):
        """Get child element.

        :rtype: _Tuple[Serializable]
        """
        if name:
            if name not in self._children_names:
                raise _error.ElementNotFound("Element '{}' does not contain '{}'.".format(self.name, name))

            return tuple([child for child in self._children if child.name == name])

        else:
            return tuple(self._children)

    @property
    def children(self):
        """Get children.

        :rtype: _Dict[str, Serializable]
        """
        return self._children

    @_abstractmethod
    def get_content(self) -> _Any:
        """Get element's content ready to serialization.
        """
        pass


class Parser(_ABC):
    """Abstract Feed Generator.
    """

    @_abstractmethod
    def load(self, source: _Any):
        """Loads data from source.
        """
        pass

    @_abstractmethod
    def generate(self) -> str:
        """Generate feed.
        """
        pass
