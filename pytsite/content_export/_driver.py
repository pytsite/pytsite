"""Poster Abstract Driver.
"""
from abc import ABC as _ABC, abstractmethod as _abstractmethod
from pytsite import widget as _widget

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Abstract(_ABC):
    def __init__(self, **kwargs):
        """Init.
        """
        pass

    @_abstractmethod
    def get_settings_widget(self, uid: str, **kwargs) -> _widget.Base:
        """Returns settings widget.
        """
        pass

    @_abstractmethod
    def export(self, entity, exporter):
        """ Performs export.

        :type entity: pytsite.content._model.Content
        :type exporter: pytsite.content_export._model.ContentExport
        """
        pass
