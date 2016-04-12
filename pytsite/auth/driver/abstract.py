"""Abstract Auth Driver.
"""
from abc import ABC as _ABC, abstractmethod as _abstractmethod
from pytsite import form as _form, http as _http

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class AbstractDriver(_ABC):
    @_abstractmethod
    def get_name(self) -> str:
        """Get name of the driver.
        """
        pass

    @property
    def name(self) -> str:
        return self.get_name()

    @_abstractmethod
    def get_login_form(self, uid: str, **kwargs) -> _form.Form:
        """Login form get handler.
        """
        pass

    @_abstractmethod
    def post_login_form(self, inp: dict) -> _http.response.Redirect:
        """Login form post handler.
        """
        pass
