"""Feed Writer.
"""
from typing import List as _List, Any as _Any, Tuple as _Tuple
from abc import ABC as _ABC, abstractmethod as _abstractmethod


__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Serializable:
    def __init__(self):
        """Init.
        """
        self._children = []  # type: _List[Serializable]

    def append_child(self, child):
        """
        :type child: Serializable
        """
        self._children.append(child)

    @property
    def children(self):
        """Get children.
        :rtype _Tuple[Serializable]
        """
        return tuple(self._children)

    @_abstractmethod
    def get_content(self) -> _Any:
        """Get object's content ready to serilization.
        """
        pass


class Generator(_ABC):
    """Feed Writer.
    """
    def __init__(self):
        """Init.
        """
        self._items = []

    @_abstractmethod
    def dispense_item(self) -> Serializable:
        pass

    @property
    def items(self) -> _Tuple[Serializable]:
        return tuple(self._items)

    def append_item(self, item: Serializable):
        """Add a feed entry.
        """
        self._items.append(item)

    @_abstractmethod
    def generate(self) -> str:
        """Generate feed.
        """
        pass

    def __str__(self) -> str:
        return self.generate()


class Reader(_ABC):
    """Abstract Feed Reader.
    """
    def __init__(self, source: _Any):
        """Init.
        """
        self._source = source

    @_abstractmethod
    def load(self):
        """Loads data from source.
        """
        pass
