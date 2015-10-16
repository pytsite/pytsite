"""Poster Abstract Driver.
"""
from abc import ABC as _ABC, abstractmethod as _abstractmethod
from pytsite import widget as _widget

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Abstract(_ABC):
    @_abstractmethod
    def get_widget(self, uid: str, **kwargs: dict) -> _widget.Base:
        pass

    @_abstractmethod
    def export(self, entity, exporter):
        """
        :param entity: pytsite.content._model.Content
        :param exporter: pytsite.content_export._model.ContentExport
        :return:
        """
        pass
