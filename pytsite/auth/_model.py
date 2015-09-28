"""Auth Models
"""
import hashlib as _hashlib
from datetime import datetime as _datetime
from pytsite import image as _image, odm as _odm, util as _util, router as _router


ANONYMOUS_LOGIN = '__anonymous@__anonymous.__anonymous'


class User(_odm.Model):
    """User ODM Model.
    """
    def _setup(self):
        """_setup() hook.
        """
        # Fields
        self._define_field(_odm.field.String('login', nonempty=True))
        self._define_field(_odm.field.String('email', nonempty=True))
        self._define_field(_odm.field.String('password', nonempty=True))
        self._define_field(_odm.field.String('nickname', nonempty=True))
        self._define_field(_odm.field.String('token'))
        self._define_field(_odm.field.String('first_name'))
        self._define_field(_odm.field.String('last_name'))
        self._define_field(_odm.field.Virtual('full_name'))
        self._define_field(_odm.field.String('description'))
        self._define_field(_odm.field.DateTime('birth_date'))
        self._define_field(_odm.field.DateTime('last_login'))
        self._define_field(_odm.field.DateTime('last_activity'))
        self._define_field(_odm.field.Integer('login_count'))
        self._define_field(_odm.field.String('status', default='active'))
        self._define_field(_odm.field.RefsList('roles', model='role'))
        self._define_field(_odm.field.Integer('gender'))
        self._define_field(_odm.field.String('phone'))
        self._define_field(_odm.field.Dict('options'))
        self._define_field(_odm.field.Ref('picture', model='image'))
        self._define_field(_odm.field.Virtual('picture_url'))
        self._define_field(_odm.field.StringList('urls', unique=True))
        self._define_field(_odm.field.Virtual('is_online'))
        self._define_field(_odm.field.RefsList('follows', model='user'))
        self._define_field(_odm.field.RefsList('followers', model='user'))

        # Indices
        self._define_index([('login', _odm.I_ASC)], unique=True)
        self._define_index([('nickname', _odm.I_ASC)], unique=True)
        self._define_index([('token', _odm.I_ASC)], unique=True)

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
        return self.f_get('login') == ANONYMOUS_LOGIN

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
    def urls(self) -> list:
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
    def password(self) -> bool:
        return self.f_get('password')

    @property
    def token(self) -> bool:
        return self.f_get('token')

    @property
    def roles(self) -> list:
        return self.f_get('roles')

    @property
    def options(self) -> dict:
        return self.f_get('options')

    @property
    def follows(self) -> list:
        return self.f_get('follows')

    @property
    def followers(self) -> list:
        return self.f_get('followers')

    def _on_f_set(self, field_name: str, value, **kwargs):
        """_on_f_set() hook.
        """
        if field_name == 'password':
            from ._functions import password_hash
            value = password_hash(value)
            self.f_set('token', _util.random_str(32))

        if field_name == 'status':
            from ._functions import get_user_statuses
            if value not in [v[0] for v in get_user_statuses()]:
                raise Exception("Invalid user status: '{}'.".format(value))

        return value

    def _pre_save(self):
        """Hook.
        """
        if self.login == ANONYMOUS_LOGIN:
            raise Exception('Anonymous user cannot be saved.')

        if not self.password:
            self.f_set('password', _util.random_password())

        if not self.token:
            self.f_set('token', _util.random_str(32))

    def _pre_delete(self):
        """Hook.
        """
        from . import _functions

        if _functions.get_current_user() == self and self.is_admin:
            raise _odm.error.ForbidEntityDelete(self.t('you_cannot_delete_yourself'))

        # Search for entities which user owns
        for model in _odm.get_registered_models():
            for e in _odm.find(model).get():
                for f_name in ('author', 'owner'):
                    if e.has_field(f_name) and e.f_get(f_name) == self:
                        # Skip self avatar to avoid  deletion block
                        if model == 'image' and self.picture == e:
                            continue

                        raise _odm.error.ForbidEntityDelete(
                            self.t('account_owns_entity', {'entity': e.model + ':' + str(e.id)}))

    def has_role(self, name: str) -> bool:
        """Checks if the user has a role.
        """
        for role in self.roles:
            if role.f_get('name') == name:
                return True

        return False

    def has_permission(self, name: str) -> bool:
        """Checks if the user has permission.
        """
        from . import _functions
        if not _functions.is_permission_defined(name):
            raise KeyError("Permission '{}' is not defined.".format(name))

        # Admin 'has' any role
        if self.is_admin:
            return True

        for role in self.f_get('roles'):
            if name in role.f_get('permissions'):
                return True

        return False

    def _on_f_get(self, field_name: str, value, **kwargs):
        """Hook.
        """
        if field_name == 'picture_url':
            size = kwargs.get('size', 256)
            """:type: pytsite.image._model.Image"""
            if self.picture:
                value = self.picture.f_get('url', width=size, height=size)
            else:
                email = _hashlib.md5(self.f_get('email').encode('utf-8')).hexdigest()
                value = _router.url('http://gravatar.com/avatar/' + email, query={'s': size})

        if field_name == 'is_online':
            value = (_datetime.now() - self.last_activity).seconds < 180

        if field_name == 'full_name':
            value = self.first_name
            if self.last_name:
                value += ' ' + self.last_name

        return value


class Role(_odm.Model):
    """Role.
    """
    @property
    def name(self) -> str:
        return self.f_get('name')

    @property
    def description(self) -> str:
        return self.f_get('description')

    @property
    def permissions(self) -> list:
        return self.f_get('permissions')

    def _setup(self):
        """_setup() hook.
        """
        self._define_field(_odm.field.String('name'))
        self._define_field(_odm.field.String('description'))
        self._define_field(_odm.field.UniqueList('permissions'))

        self._define_index([('name', _odm.I_ASC)], unique=True)

    def _on_f_add(self, field_name: str, value, **kwargs: dict):
        """_on_f_add() hook.
        """
        if field_name == 'permissions' and not isinstance(value, str):
            raise TypeError("String expected")

        return value

    def _pre_delete(self):
        """Hook.
        """
        from . import _functions

        for user in _functions.find_users(False).get():
            if user.has_role(self.name):
                raise _odm.error.ForbidEntityDelete(self.t('role_user_by_user', {'user': user.login}))
