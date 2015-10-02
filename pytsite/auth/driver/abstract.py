"""Abstract Auth Driver.
"""
from abc import ABC as _ABC, abstractmethod as _abstractmethod
from pytsite import form as _form, http as _http

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class AbstractDriver(_ABC):
    @_abstractmethod
    def get_login_form(self, uid='', css='', title='') -> _form.Base:
        """Login form get handler.
        """
        raise NotImplementedError()

    @_abstractmethod
    def post_login_form(self, args: dict, inp: dict) -> _http.response.Redirect:
        """Login form post handler.
        """
        raise NotImplementedError()
