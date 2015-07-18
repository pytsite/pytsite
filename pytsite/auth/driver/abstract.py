"""Abstract Auth Driver.
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from abc import ABC as _ABC, abstractmethod as _abstractmethod
from pytsite.core import http as _http, form as _form


class AbstractDriver(_ABC):
    @_abstractmethod
    def get_login_form(self, uid: str=None, cls: str=None, legend: str=None) -> _form.Base:
        """Login form get handler.
        """
        raise NotImplementedError()

    @_abstractmethod
    def post_login_form(self, args: dict, inp: dict) -> _http.response.Redirect:
        """Login form post handler.
        """
        raise NotImplementedError()
