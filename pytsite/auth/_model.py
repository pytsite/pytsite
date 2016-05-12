"""Auth Models
"""
import hashlib as _hashlib
from frozendict import frozendict as _frozendict
from typing import Iterable as _Iterable
from datetime import datetime as _datetime
from pytsite import image as _image, odm as _odm, util as _util, router as _router, geo_ip as _geo_ip, \
    permission as _permission


ANONYMOUS_USER_LOGIN = 'anonymous@anonymous.anonymous'


class Role(_odm.Entity):
    """Role.
    """
    def _setup_fields(self):
        """Hook.
        """
        self.define_field(_odm.field.String('name'))
        self.define_field(_odm.field.String('description'))
        self.define_field(_odm.field.UniqueList('permissions', allowed_types=(str,)))

    def _setup_indexes(self):
        """Hook.
        """
        self.define_index([('name', _odm.I_ASC)], unique=True)

    @property
    def name(self) -> str:
        return self.f_get('name')

    @property
    def description(self) -> str:
        return self.f_get('description')

    @property
    def permissions(self) -> _Iterable[str]:
        return self.f_get('permissions')

    def _pre_delete(self, **kwargs):
        """Hook.
        """
        from . import _api

        # Check if the role is used by users
        for user in _api.find_users(False).get():
            if user.has_role(self.name):
                raise _odm.error.ForbidEntityDelete(self.t('role_used_by_user', {'user': user.login}))


class User(_odm.Entity):
    """User ODM Model.
    """
    def _setup_fields(self):
        """_setup() hook.
        """
        # Fields
        self.define_field(_odm.field.String('login', nonempty=True))
        self.define_field(_odm.field.String('email', nonempty=True))
        self.define_field(_odm.field.String('password', nonempty=True))
        self.define_field(_odm.field.String('nickname', nonempty=True))
        self.define_field(_odm.field.String('token', nonempty=True))
        self.define_field(_odm.field.String('first_name'))
        self.define_field(_odm.field.String('last_name'))
        self.define_field(_odm.field.Virtual('full_name'))
        self.define_field(_odm.field.String('description'))
        self.define_field(_odm.field.DateTime('birth_date'))
        self.define_field(_odm.field.DateTime('last_login'))
        self.define_field(_odm.field.DateTime('last_activity'))
        self.define_field(_odm.field.Integer('login_count'))
        self.define_field(_odm.field.String('status', default='active'))
        self.define_field(_odm.field.RefsList('roles', model='role'))
        self.define_field(_odm.field.Integer('gender'))
        self.define_field(_odm.field.String('phone'))
        self.define_field(_odm.field.Dict('options'))
        self.define_field(_odm.field.Ref('picture', model='image'))
        self.define_field(_odm.field.Virtual('picture_url'))
        self.define_field(_odm.field.StringList('urls', unique=True))
        self.define_field(_odm.field.Virtual('is_online'))
        self.define_field(_odm.field.RefsList('follows', model='user'))
        self.define_field(_odm.field.RefsList('followers', model='user'))
        self.define_field(_odm.field.String('last_ip'))
        self.define_field(_odm.field.Virtual('geo_ip'))
        self.define_field(_odm.field.String('country'))
        self.define_field(_odm.field.String('city'))

    def _setup_indexes(self):
        """Hook.
        """
        self.define_index([('login', _odm.I_ASC)], unique=True)
        self.define_index([('nickname', _odm.I_ASC)], unique=True)
        self.define_index([('token', _odm.I_ASC)], unique=True)
        self.define_index([('last_login', _odm.I_DESC)])

    @property
    def login(self) -> str:
        return self.f_get('login')

    @property
    def email(self) -> str:
        return self.f_get('email')

    @property
    def nickname(self) -> str:
        return self.f_get('nickname')

    @property
    def is_anonymous(self) -> bool:
        """Check if the user is anonymous.
        """
        return self.f_get('login') == ANONYMOUS_USER_LOGIN

    @property
    def is_admin(self) -> bool:
        """Check if the user has the 'admin' role.
        """
        return self.has_role('admin')

    @property
    def first_name(self) -> str:
        return self.f_get('first_name')

    @property
    def last_name(self) -> str:
        return self.f_get('last_name')

    @property
    def full_name(self) -> str:
        return self.f_get('full_name')

    @property
    def description(self) -> str:
        return self.f_get('description')

    @property
    def picture_url(self) -> str:
        return self.f_get('picture_url')

    @property
    def login_count(self) -> int:
        return self.f_get('login_count')

    @property
    def last_login(self) -> _datetime:
        return self.f_get('last_login')

    @property
    def last_activity(self) -> _datetime:
        return self.f_get('last_activity')

    @property
    def gender(self) -> int:
        return self.f_get('gender')

    @property
    def picture(self) -> _image.model.Image:
        return self.f_get('picture')

    @property
    def urls(self) -> tuple:
        return self.f_get('urls')

    @property
    def is_online(self) -> bool:
        return self.f_get('is_online')

    @property
    def status(self) -> bool:
        return self.f_get('status')

    @property
    def profile_is_public(self) -> bool:
        return self.f_get('profile_is_public')

    @property
    def password(self) -> str:
        return self.f_get('password')

    @property
    def token(self) -> str:
        return self.f_get('token')

    @property
    def roles(self) -> _Iterable[Role]:
        return self.f_get('roles')

    @property
    def options(self) -> _frozendict:
        return self.f_get('options')

    @property
    def follows(self):
        """
        :return: _Iterable[User]
        """
        return self.f_get('follows')

    @property
    def followers(self):
        """
        :return: _Iterable[User]
        """
        return self.f_get('followers')

    @property
    def last_ip(self) -> str:
        return self.f_get('last_ip')

    @property
    def geo_ip(self) -> _geo_ip.model.GeoIP:
        return self.f_get('geo_ip')

    @property
    def country(self) -> str:
        return self.f_get('country')

    @property
    def city(self) -> str:
        return self.f_get('city')

    def _on_f_set(self, field_name: str, value, **kwargs):
        """_on_f_set() hook.
        """
        if field_name == 'password':
            from ._api import password_hash
            if value:
                value = password_hash(value)
                self.f_set('token', _util.random_str(32))
            else:
                if self.is_new:
                    # Set random password
                    value = password_hash(_util.random_password())
                    self.f_set('token', _util.random_str(32))
                else:
                    # Keep old password
                    value = self.password

        if field_name == 'status':
            from ._api import get_user_statuses
            if value not in [v[0] for v in get_user_statuses()]:
                raise Exception("Invalid user status: '{}'.".format(value))

        if field_name == 'nickname':
            from ._api import user_nickname_rule
            value = value[:24]
            user_nickname_rule.value = value
            user_nickname_rule.validate()

        return value

    def _pre_save(self):
        """Hook.
        """
        if self.login == ANONYMOUS_USER_LOGIN:
            raise Exception('Anonymous user cannot be saved.')

        if not self.password:
            self.f_set('password', '')

        if not self.token:
            self.f_set('token', _util.random_str(32))

        if not self.nickname:
            m = _hashlib.md5()
            m.update(self.login.encode('UTF-8'))
            self.f_set('nickname', m.hexdigest())

    def _pre_delete(self, **kwargs):
        """Hook.
        """
        from . import _api

        # Users cannot delete themselves
        if _api.get_current_user() == self and self.is_admin:
            raise _odm.error.ForbidEntityDelete(self.t('you_cannot_delete_yourself'))

        # Search for entities which user owns
        for model in _odm.get_registered_models():
            for entity in _odm.find(model).get():
                for f_name in ('author', 'owner'):
                    if entity.has_field(f_name) and entity.f_get(f_name) == self:
                        # Skip user's avatar to avoid  deletion block
                        if model == 'image' and self.picture == entity:
                            continue

                        raise _odm.error.ForbidEntityDelete(
                            self.t('account_owns_entity', {'entity': entity.model + ':' + str(entity.id)}))

    def has_role(self, name: str) -> bool:
        """Checks if the user has a role.
        """
        return name in [role.name for role in self.roles]

    def has_permission(self, name: str) -> bool:
        """Checks if the user has permission.
        """
        # Checking for permission existence
        _permission.get_permission(name)

        # Admin 'has' any role
        if self.is_admin:
            return True

        for role in self.roles:
            if name in role.permissions:
                return True

        return False

    def _on_f_get(self, field_name: str, value, **kwargs):
        """Hook.
        """
        if field_name == 'picture_url':
            size = kwargs.get('size', 256)
            if self.picture:
                value = self.picture.f_get('url', width=size, height=size)
            else:
                email = _hashlib.md5(self.f_get('email').encode('utf-8')).hexdigest()
                value = _router.url('http://gravatar.com/avatar/' + email, query={'s': size})

        elif field_name == 'is_online':
            value = (_datetime.now() - self.last_activity).seconds < 180

        elif field_name == 'full_name':
            value = self.first_name
            if self.last_name:
                value += ' ' + self.last_name

        elif field_name == 'geo_ip':
            try:
                value = _geo_ip.resolve(self.last_ip)
            except _geo_ip.error.ResolveError:
                value = _geo_ip.resolve('0.0.0.0')

        return value
