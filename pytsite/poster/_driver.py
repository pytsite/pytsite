"""Poster Abstract Driver.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from abc import ABC as _ABC, abstractmethod as _abstractmethod


class Abstract(_ABC):
    @_abstractmethod
    def create_post(self, **kwargs: dict):
        pass
