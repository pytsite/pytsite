"""Feed Writer.
"""
from typing import Iterable as _Iterable, Any as _Any
from abc import abstractmethod as _abstractmethod
from lxml import etree as _etree
from pytsite import validation as _validation


__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Serializable:
    def __init__(self):
        self._children = []

    def add_child(self, child):
        """:type child: Serializable"""
        self._children.append(child)

    @_abstractmethod
    def get_content(self) -> _Any:
        pass


class Generator:
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
    def items(self) -> _Iterable[Serializable]:
        return self._items

    def add_item(self, item: Serializable):
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
