"""
"""
from pytsite import auth as _auth, widget as _widget


__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class UserSelect(_widget.select.Select):
    """User Select Widget.
    """
    def __init__(self, uid: str, **kwargs):
        super().__init__(uid, **kwargs)

        c_user = _auth.current_user()
        if not c_user.has_permission('pytsite.odm_perm.view.user'):
            self._items.append((c_user.login, '{} ({})'.format(c_user.full_name, c_user.login)))
        else:
            for user in _auth.get_users({'status': 'active'}, sort_field='first_name'):
                self._items.append((user.login, '{} ({})'.format(user.full_name, user.login)))

    def set_val(self, value, **kwargs):
        if isinstance(value, _auth.model.AbstractUser):
            value = value.login
        elif isinstance(value, str):
            # Check user existence
            _auth.get_user(value)

        return super().set_val(value, **kwargs)

    def get_val(self, **kwargs) -> _auth.model.AbstractUser:
        value = super().get_val(**kwargs)
        if value:
            value = _auth.get_user(value)

        return value
