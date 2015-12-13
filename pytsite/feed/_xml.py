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
    @_abstractmethod
    def get_content(self) -> _etree.Element:
        pass


class Generator(_abstract.Generator):
    def __init__(self, nsmap: dict=None):
        super().__init__()
        self._nsmap = nsmap or {}

    @_abstractmethod
    def dispense_item(self) -> Item:
        pass

    def add_item(self, item: Item):
        super().add_item(item)

    @property
    def items(self) -> _Iterable[Item]:
        return self._items