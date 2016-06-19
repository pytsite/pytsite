"""PytSite Auth Base Drivers.
"""
from typing import Iterable as _Iterable
from abc import ABC as _ABC, abstractmethod as _abstractmethod
from pytsite import form as _form
from . import _model

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Authentication(_ABC):
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
    def sign_up(self, data: dict) -> _model.UserInterface:
        """Register new user.
        """
        pass

    @_abstractmethod
    def sign_in(self, data: dict) -> _model.UserInterface:
        """Authenticate user.
        """
        pass

    def sign_out(self, user: _model.UserInterface):
        """End user's session.
        """
        pass


class Storage(_ABC):
    @_abstractmethod
    def get_name(self) -> str:
        pass

    @_abstractmethod
    def create_role(self, name: str, description: str = '') -> _model.RoleInterface:
        pass

    @_abstractmethod
    def get_role(self, name: str) -> _model.RoleInterface:
        pass

    @_abstractmethod
    def get_roles(self) -> _Iterable[_model.RoleInterface]:
        pass

    @_abstractmethod
    def create_user(self, login: str, password: str = None) -> _model.UserInterface:
        pass

    @_abstractmethod
    def get_user(self, login: str = None, nickname: str = None, access_token: str = None) -> _model.UserInterface:
        pass

    @_abstractmethod
    def get_users(self, active_only: bool = True, sort_field: str = None, sort_order: int = 1, limit: int = None,
                  skip: int = None) -> _Iterable[_model.UserInterface]:
        pass
