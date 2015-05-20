"""ODM UI Model.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite.core.lang import t
from pytsite.core.form import AbstractForm
from pytsite.core.odm import odm
from pytsite.core.odm.model import ODMModel


class UIModelMixin:
    def get_browser_title(self) -> str:
        pass

    def get_browser_columns(self) -> tuple:
        return t('pytsite.core@id'),

    def get_browser_row(self) -> tuple:
        pass

    def get_form(self) -> AbstractForm:
        pass

    def submit_form(self):
        pass
