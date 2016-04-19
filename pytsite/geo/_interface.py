"""PytSit Geo Interfaces.
"""
from abc import ABC as _ABC, abstractmethod as _abstractmethod

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class GeoCoder(_ABC):
    @_abstractmethod
    def encode(self, address: str, **kwargs):
        pass

    @_abstractmethod
    def decode(self, lng: float, lat: float, **kwargs):
        pass
