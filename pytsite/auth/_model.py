"""Auth Models
"""
from abc import ABC as _ABC, abstractmethod as _abstractmethod
from typing import Union as _Union, Tuple as _Tuple, List as _List
from datetime import datetime as _datetime
from pytsite import geo_ip as _geo_ip, permission as _permission, router as _router, util as _util

ANONYMOUS_USER_LOGIN = 'anonymous@anonymous.anonymous'
SYSTEM_USER_LOGIN = 'system@system.system'


class AuthEntity(_ABC):
    @property
    def uid(self) -> str:
        raise NotImplementedError()

    @property
    def auth_entity_type(self) -> str:
        raise NotImplementedError()


class AbstractRole(AuthEntity):
    """Role.
    """

    @property
    def uid(self) -> str:
        return _util.md5_hex_digest(self.name)

    @property
    def auth_entity_type(self) -> str:
        return 'role'

    @property
    def name(self) -> str:
        raise NotImplementedError()

    @name.setter
    def name(self, value: str):
        raise NotImplementedError()

    @property
    def description(self) -> str:
        raise NotImplementedError()

    @description.setter
    def description(self, value: str):
        raise NotImplementedError()

    @property
    def permissions(self) -> _Union[_List, _Tuple]:
        raise NotImplementedError()

    @permissions.setter
    def permissions(self, value: _Union[_List, _Tuple]):
        raise NotImplementedError()


class AbstractUser(AuthEntity):
    """User ODM Model.
    """
    @property
    def uid(self) -> str:
        return _util.md5_hex_digest(self.login)

    @property
    def auth_entity_type(self) -> str:
        return 'user'

    @property
    def is_anonymous(self) -> bool:
        """Check if the user is anonymous.
        """
        return self.login == ANONYMOUS_USER_LOGIN

    @property
    def is_system(self) -> bool:
        """Check if the user is anonymous.
        """
        return self.login == SYSTEM_USER_LOGIN

    @property
    def is_admin(self) -> bool:
        """Check if the user has the 'admin' role.
        """
        return self.has_role('admin')

    @property
    def is_online(self) -> bool:
        return (_datetime.now() - self.last_activity).seconds < 180

    @property
    def geo_ip(self) -> _geo_ip.model.GeoIP:
        try:
            return _geo_ip.resolve(self.last_ip)
        except _geo_ip.error.ResolveError:
            return _geo_ip.resolve('0.0.0.0')

    @property
    def is_new(self) -> bool:
        raise NotImplementedError()

    @property
    def created(self) -> _datetime:
        raise NotImplementedError()

    @property
    def login(self) -> str:
        raise NotImplementedError()

    @login.setter
    def login(self, value: str):
        raise NotImplementedError()

    @property
    def email(self) -> str:
        raise NotImplementedError()

    @email.setter
    def email(self, value: str):
        raise NotImplementedError()

    @property
    def password(self) -> str:
        raise NotImplementedError()

    @password.setter
    def password(self, value: str):
        raise NotImplementedError()

    @property
    def nickname(self) -> str:
        raise NotImplementedError()

    @nickname.setter
    def nickname(self, value: str):
        raise NotImplementedError()

    @property
    def access_token(self) -> str:
        raise NotImplementedError()

    @access_token.setter
    def access_token(self, value: str):
        raise NotImplementedError()

    @property
    def first_name(self) -> str:
        raise NotImplementedError()

    @first_name.setter
    def first_name(self, value: str):
        raise NotImplementedError()

    @property
    def last_name(self) -> str:
        raise NotImplementedError()

    @last_name.setter
    def last_name(self, value: str):
        raise NotImplementedError()

    @property
    def full_name(self) -> str:
        return self.first_name + ' ' + self.last_name

    @property
    def description(self) -> str:
        raise NotImplementedError()

    @description.setter
    def description(self, value: str):
        raise NotImplementedError()

    @property
    def birth_date(self) -> _datetime:
        raise NotImplementedError()

    @birth_date.setter
    def birth_date(self, value: _datetime):
        raise NotImplementedError()

    @property
    def last_sign_in(self) -> _datetime:
        raise NotImplementedError()

    @last_sign_in.setter
    def last_sign_in(self, value: _datetime):
        raise NotImplementedError()

    @property
    def last_activity(self) -> _datetime:
        raise NotImplementedError()

    @last_activity.setter
    def last_activity(self, value: _datetime):
        raise NotImplementedError()

    @property
    def sign_in_count(self) -> int:
        raise NotImplementedError()

    @sign_in_count.setter
    def sign_in_count(self, value: int):
        raise NotImplementedError()

    @property
    def status(self) -> str:
        raise NotImplementedError()

    @status.setter
    def status(self, value: str):
        raise NotImplementedError()

    @property
    def roles(self) -> _Tuple[AbstractRole]:
        from ._api import get_role
        if self.is_anonymous:
            return get_role('anonymous'),
        elif self.is_system:
            return get_role('admin'),
        else:
            raise NotImplementedError()

    @roles.setter
    def roles(self, value: tuple):
        raise NotImplementedError()

    @property
    def gender(self) -> str:
        raise NotImplementedError()

    @gender.setter
    def gender(self, value: str):
        raise NotImplementedError()

    @property
    def phone(self) -> int:
        raise NotImplementedError()

    @phone.setter
    def phone(self, value: int):
        raise NotImplementedError()

    @property
    def options(self) -> dict:
        raise NotImplementedError()

    @options.setter
    def options(self, value: dict):
        raise NotImplementedError()

    @property
    def picture(self):
        """
        :rtype: pytsite.image.model.Image
        """
        raise NotImplementedError()

    @picture.setter
    def picture(self, value):
        raise NotImplementedError()

    @property
    def urls(self) -> tuple:
        raise NotImplementedError()

    @urls.setter
    def urls(self, value: tuple):
        raise NotImplementedError()

    @property
    def profile_is_public(self) -> bool:
        raise NotImplementedError()

    @profile_is_public.setter
    def profile_is_public(self, value: bool):
        raise NotImplementedError()

    @property
    def follows(self):
        """
        :return: _Iterable[User]
        """
        raise NotImplementedError()

    @follows.setter
    def follows(self, value):
        raise NotImplementedError()

    @property
    def followers(self):
        """
        :return: _Iterable[User]
        """
        raise NotImplementedError()

    @followers.setter
    def followers(self, value):
        raise NotImplementedError()

    @property
    def last_ip(self) -> str:
        raise NotImplementedError()

    @last_ip.setter
    def last_ip(self, value: str):
        raise NotImplementedError()

    @property
    def country(self) -> str:
        raise NotImplementedError()

    @country.setter
    def country(self, value: str):
        raise NotImplementedError()

    @property
    def city(self) -> str:
        raise NotImplementedError()

    @city.setter
    def city(self, value: str):
        raise NotImplementedError()

    @property
    def profile_view_url(self) -> str:
        return _router.ep_url('pytsite.auth@profile_view', {'nickname': self.nickname})

    @property
    def profile_edit_url(self) -> str:
        return _router.ep_url('pytsite.auth@profile_edit', {'nickname': self.nickname})

    @_abstractmethod
    def add_follower(self, follower):
        pass

    @_abstractmethod
    def remove_follower(self, follower):
        pass

    @_abstractmethod
    def add_follows(self, user):
        pass

    @_abstractmethod
    def remove_follows(self, user):
        pass

    def has_role(self, name: str) -> bool:
        """Checks if the user has a role.
        """
        return name in [role.name for role in self.roles]

    def has_permission(self, name: str) -> bool:
        """Checks if the user has permission.
        """
        # Checking for permission existence
        _permission.get_permission(name)

        # System and admin users
        if self.is_system or self.is_admin:
            return True

        for role in self.roles:
            if name in role.permissions:
                return True

        return False
