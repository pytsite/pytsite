"""Abstract Auth Driver.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from abc import ABC, abstractmethod
from pytsite.core.router import RedirectResponse
from pytsite.core.forms import BaseForm


class AbstractDriver(ABC):
    @abstractmethod
    def get_login_form(self, uid: str='pytsite-auth-login', cls: str=None) -> BaseForm:
        """Login form get handler.
        """
        raise NotImplementedError()

    @abstractmethod
    def post_login_form(self, args: dict, inp: dict) -> RedirectResponse:
        """Login form post handler.
        """
        raise NotImplementedError()
