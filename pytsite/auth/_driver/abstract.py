"""Abstract Auth Driver.
"""
from abc import ABC as _ABC, abstractmethod as _abstractmethod
from pytsite import form as _form
from .. import _model

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Abstract(_ABC):
    @_abstractmethod
    def get_name(self) -> str:
        """Get name of the driver.
        """
        pass

    @property
    def name(self) -> str:
        return self.get_name()

    @_abstractmethod
    def get_sign_up_form(self, form_uid: str, **kwargs) -> _form.Form:
        """Get sign in form.
        """
        pass

    @_abstractmethod
    def get_sign_in_form(self, form_uid: str, **kwargs) -> _form.Form:
        """Get sign in form.
        """
        pass

    @_abstractmethod
    def sign_up(self, data: dict) -> _model.User:
        """Register new user.
        """
        pass

    @_abstractmethod
    def sign_in(self, data: dict) -> _model.User:
        """Authenticate user.
        """
        pass

    @_abstractmethod
    def sign_out(self):
        """End user's session.
        """
        pass
