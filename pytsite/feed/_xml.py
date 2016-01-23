"""Abstract XML Based Feed.
"""
from typing import Iterable as _Iterable
from abc import abstractmethod as _abstractmethod
from lxml import etree as _etree
from . import _abstract

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Item(_abstract.Serializable):
    """XML Feed Item.
    """
    @_abstractmethod
    def get_content(self) -> _etree.Element:
        """Get object's content ready to serilization.
        """
        pass


class Generator(_abstract.Generator):
    """XML Feed Generator.
    """
    def __init__(self, nsmap: dict=None):
        super().__init__()
        self._nsmap = nsmap or {}

    @_abstractmethod
    def dispense_item(self) -> Item:
        pass

    def append_item(self, item: Item):
        super().append_item(item)

    @property
    def items(self) -> _Iterable[Item]:
        return self._items


class Reader(_abstract.Reader):
    """XML Feed Reader.
    """
    pass
