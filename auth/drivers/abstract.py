"""Abstract auth driver.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from abc import ABC, abstractmethod
from pytsite.core.router import RedirectResponse
from pytsite.core.form import AbstractForm


class AbstractDriver(ABC):
    @abstractmethod
    def get_login_form(self, uid: str) -> AbstractForm:
        """Login form get handler.
        """
        pass

    @abstractmethod
    def post_login_form(self, args: dict, inp: dict) -> RedirectResponse:
        """Login form post handler.
        """
        pass